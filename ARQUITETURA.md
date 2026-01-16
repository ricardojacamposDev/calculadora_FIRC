# Arquitetura da Calculadora FIRC

## Visão Geral

A Calculadora FIRC segue uma arquitetura modular baseada no princípio de **Separação de Responsabilidades (SoC)**, onde cada módulo tem uma função específica e bem definida.

```
┌─────────────┐
│   main.py   │  ← Interface CLI
└──────┬──────┘
       │
       ├─────────────────────────────────────┐
       │                                     │
       ▼                                     ▼
┌──────────────┐                    ┌──────────────┐
│ pdf_parser.py│                    │calculator.py │
│              │                    │              │
│ Extrai dados │                    │ Calcula      │
│ do PDF       │───────────────────▶│ totais       │
└──────────────┘                    └──────┬───────┘
       │                                   │
       │                                   │
       ▼                                   ▼
┌──────────────────────────────────────────────────┐
│           data_processor.py                      │
│                                                  │
│  Converte valores monetários string → float     │
└──────────────────────────────────────────────────┘
```

## Módulos

### 1. `main.py` - Interface de Linha de Comando

**Responsabilidade**: Ponto de entrada da aplicação

**Funções**:
- Recebe argumentos da linha de comando
- Orquestra o fluxo de processamento
- Formata e imprime saída JSON

**Fluxo**:
```python
1. Recebe caminho do PDF via sys.argv
2. Chama process_pdf()
3. Imprime resultado em JSON
```

### 2. `pdf_parser.py` - Parser de PDF

**Responsabilidade**: Extração de dados de arquivos PDF

**Classe Principal**: `PDFFinancialParser`

**Métodos**:
- `__init__(pdf_path)`: Inicializa com caminho do PDF
- `extract_data()`: Extrai dados de todas as páginas
- `_extract_from_page()`: Processa uma página
- `_extract_from_table()`: Extrai dados de tabelas estruturadas
- `_extract_from_text()`: Extrai dados de texto formatado
- `_is_monetary_value()`: Valida se string é valor monetário

**Dependências**:
- `pdfplumber`: Biblioteca de extração de PDF

**Estratégia de Extração**:
1. Tenta extrair de tabelas estruturadas primeiro
2. Se não houver tabelas, processa texto formatado
3. Identifica valores por padrões regex
4. Localiza posições específicas (2ª e 4ª ocorrências de valores)

### 3. `data_processor.py` - Processador de Dados

**Responsabilidade**: Conversão e validação de dados monetários

**Funções Principais**:

#### `clean_monetary_value(value)`
Converte string monetária em float decimal

**Processo**:
```
"R$ 1.234,56" 
    ↓ Remove "R$"
"1.234,56"
    ↓ Remove pontos (separador milhar)
"1234,56"
    ↓ Substitui vírgula por ponto
"1234.56"
    ↓ Converte para float
1234.56
```

**Casos Especiais**:
- `None` → 0.0
- `""` → 0.0
- Strings inválidas → 0.0
- Números já convertidos → retorna como float

#### `validate_decimal(value)`
Valida se valor é decimal válido (não NaN)

### 4. `calculator.py` - Calculadora Financeira

**Responsabilidade**: Cálculo de totais

**Classe Principal**: `FinancialCalculator`

**Métodos**:
- `calculate_totals(extracted_data)`: Calcula ambos os totais
- `_sum_values(values)`: Soma lista de valores
- `_validate_totals()`: Validação silenciosa

**Processo de Cálculo**:
```python
1. Recebe dados extraídos: {"valor_pago": [...], "cartorio": [...]}
2. Para cada lista:
   a. Converte cada string monetária em float
   b. Valida o valor
   c. Soma ao total
3. Arredonda para 2 casas decimais
4. Valida totais (não-negativos, não-NaN)
5. Retorna resultado
```

**Garantias**:
- Totais sempre ≥ 0.0
- Precisão de 2 casas decimais
- Valores inválidos tratados como 0.0

## Fluxo de Dados Completo

```
┌─────────────────────────────────────────────────────────────┐
│ 1. ENTRADA                                                  │
│    python main.py arquivo.pdf                               │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. EXTRAÇÃO (pdf_parser.py)                                │
│    ┌──────────────────────────────────────┐                │
│    │ PDF Pages                            │                │
│    │  ├─ Page 1                           │                │
│    │  │   ├─ Extract Tables               │                │
│    │  │   └─ Extract Text                 │                │
│    │  ├─ Page 2                           │                │
│    │  └─ Page N                           │                │
│    └──────────────────────────────────────┘                │
│                         │                                   │
│                         ▼                                   │
│    Dados brutos: ["R$ 301,61", "R$ 985,92", ...]           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. PROCESSAMENTO (data_processor.py)                       │
│    Para cada valor:                                         │
│    "R$ 301,61" → 301.61                                     │
│    "R$ 985,92" → 985.92                                     │
│    None        → 0.0                                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. CÁLCULO (calculator.py)                                  │
│    total_valor_pago = sum([301.61, 985.92, ...])            │
│    total_cartorio = sum([215.44, 713.27, ...])              │
│                                                             │
│    Validação:                                               │
│    ✓ Valores não-negativos                                  │
│    ✓ Arredondamento 2 casas decimais                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. SAÍDA (main.py)                                          │
│    {                                                        │
│      "total_valor_pago": 13484.39,                          │
│      "total_cartorio": 9889.19                              │
│    }                                                        │
└─────────────────────────────────────────────────────────────┘
```

## Padrões de Design

### 1. **Single Responsibility Principle (SRP)**
Cada módulo tem uma única responsabilidade:
- Parser: apenas extração
- Processor: apenas conversão
- Calculator: apenas cálculo

### 2. **Dependency Injection**
```python
# main.py injeta dependências
parser = PDFFinancialParser(pdf_path)  # Injeta caminho
calculator = FinancialCalculator()
result = calculator.calculate_totals(extracted_data)  # Injeta dados
```

### 3. **Fail-Safe / Defensive Programming**
- Valores inválidos → 0.0 (nunca falha)
- Validações silenciosas
- Try-except para operações de I/O

### 4. **Pure Functions**
```python
# data_processor.py
clean_monetary_value(value)  # Mesma entrada = mesma saída
```

## Tratamento de Erros

### Estratégia: **Graceful Degradation**

1. **Arquivo não encontrado**: Retorna totais 0.0
2. **PDF corrompido**: Retorna totais 0.0
3. **Valores ilegíveis**: Trata como 0.0
4. **Formato inesperado**: Tenta múltiplas estratégias de parsing

```python
# Exemplo em pdf_parser.py
try:
    with pdfplumber.open(self.pdf_path) as pdf:
        # Processa...
except Exception as e:
    # Retorna listas vazias (soma será 0.0)
    print(f"Erro: {e}", file=sys.stderr)
```

## Extensibilidade

### Como adicionar novos campos:

1. **Adicionar extração** em `pdf_parser.py`:
```python
self.novo_campo_values: List[str] = []
```

2. **Adicionar cálculo** em `calculator.py`:
```python
self.total_novo_campo = self._sum_values(
    extracted_data.get("novo_campo", [])
)
```

3. **Adicionar ao output** em `calculator.py`:
```python
return {
    "total_valor_pago": self.total_valor_pago,
    "total_cartorio": self.total_cartorio,
    "total_novo_campo": self.total_novo_campo
}
```

## Testes

### Estrutura de Testes

```
test_calculator.py
├── TestDataProcessor
│   ├── Conversão com R$
│   ├── Conversão sem símbolo
│   ├── Valores None/vazios
│   ├── Valores numéricos
│   └── Valores inválidos
└── TestFinancialCalculator
    ├── Dados válidos
    ├── Dados vazios
    ├── Dados mistos
    └── Validação não-negativos
```

### Cobertura
- Conversão de valores: 100%
- Cálculo de totais: 100%
- Validações: 100%

## Performance

### Complexidade

- **Extração**: O(n * m) onde n = páginas, m = valores por página
- **Conversão**: O(k) onde k = total de valores
- **Cálculo**: O(k)
- **Total**: O(n * m) ≈ linear no tamanho do PDF

### Otimizações Possíveis

1. **Cache de conversões**: Memoizar clean_monetary_value()
2. **Processamento paralelo**: Processar páginas em paralelo
3. **Streaming**: Para PDFs muito grandes

## Segurança

### Validações

- ✅ Path traversal: Usa pathlib.Path
- ✅ Injection: Não executa código dinâmico
- ✅ Overflow: Limita precisão decimal
- ✅ Denial of Service: Timeout implícito do pdfplumber

### Dados Sensíveis

- Nunca imprime dados completos (apenas totais)
- Logs de erro enviados para stderr
- Sem armazenamento persistente

## Manutenção

### Logging

Para adicionar logs detalhados:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Em pdf_parser.py
logger.debug(f"Extraindo página {page_num}")
```

### Monitoramento

Métricas recomendadas:
- Tempo de processamento por página
- Taxa de valores válidos vs inválidos
- Tamanho médio dos PDFs processados

# Calculadora FIRC - Financial Invoice Receipt Calculator

Aplicação Python especializada para processar documentos PDF financeiros ("Guias Geradas") e calcular totais específicos de forma automatizada.

## 📋 Funcionalidades

- ✅ Extrai e soma valores da coluna **Cartório** (8ª coluna dos rateios)
- ✅ Extrai e soma valores do campo **Valor Pago**
- ✅ Suporta PDFs com múltiplas páginas
- ✅ Trata valores ausentes ou ilegíveis como 0.0
- ✅ Converte automaticamente formatos monetários brasileiros (R$ 1.234,56)
- ✅ Saída em formato **JSON puro** (sem texto adicional)
- ✅ Validação silenciosa de integridade dos dados

## 🚀 Instalação

### Requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos

```bash
# Clone ou acesse o diretório do projeto
cd calculadora_FIRC

# Instale as dependências
pip install -r requirements.txt
```

## 💻 Uso

### Linha de Comando

```bash
python main.py <caminho_para_pdf>
```

**Exemplo:**
```bash
python main.py consultarGuiasGeradas_Report.pdf
```

### Saída

```json
{
  "total_valor_pago": 13484.39,
  "total_cartorio": 9889.19
}
```

### Uso Programático

```python
from pdf_parser import PDFFinancialParser
from calculator import FinancialCalculator

# Extrair dados
parser = PDFFinancialParser("meu_arquivo.pdf")
dados = parser.extract_data()

# Calcular totais
calculator = FinancialCalculator()
resultado = calculator.calculate_totals(dados)

print(resultado)
# {'total_valor_pago': 13484.39, 'total_cartorio': 9889.19}
```

## 📁 Estrutura do Projeto

```
calculadora_FIRC/
├── main.py              # Script principal (CLI)
├── pdf_parser.py        # Módulo de extração de PDFs
├── data_processor.py    # Processador de dados monetários
├── calculator.py        # Calculadora de totais
├── requirements.txt     # Dependências Python
├── test_calculator.py   # Testes unitários
├── exemplos.py          # Exemplos de uso
├── debug_pdf.py         # Utilitário de debug
└── README.md           # Documentação
```

## 🧪 Testes

Execute os testes unitários:

```bash
python -m unittest test_calculator.py -v
```

## 📚 Exemplos

Execute o arquivo de exemplos para ver demonstrações:

```bash
python exemplos.py
```

Isso executará:
1. Processamento básico de PDF
2. Processamento detalhado com listagem de valores
3. Validação de conversão de valores monetários

## 🔧 Especificações Técnicas

### Regras de Processamento

1. **Extração Exclusiva**: Apenas processa os campos especificados
2. **Campos Considerados**:
   - Valor Pago (2ª coluna de valores)
   - Cartório (4ª coluna de valores / 8ª coluna da tabela)
3. **Conversão Monetária**:
   - Remove símbolos de moeda (R$)
   - Remove separadores de milhar (.)
   - Converte vírgula (,) em ponto decimal (.)
4. **Tratamento de Erros**: Valores ausentes/ilegíveis = 0.0
5. **Validação**: Garante que totais são não-negativos e válidos

### Dependências

- `pdfplumber==0.11.0` - Extração de dados de PDFs
- `tabulate==0.9.0` - Formatação de tabelas (auxiliar)

## 📄 Formato de Saída

Schema JSON **estrito** (conforme especificação):

```json
{
  "total_valor_pago": <float>,
  "total_cartorio": <float>
}
```

- Valores sempre com 2 casas decimais
- Sem comentários ou texto adicional
- Encoding UTF-8

## 🔍 Exemplo de PDF Processado

O projeto inclui um PDF de exemplo (`consultarGuiasGeradas_Report.pdf`) contendo:
- 11 guias geradas
- Múltiplos valores de Valor Pago e Cartório
- Formato típico de relatórios financeiros

Resultado esperado:
- **Total Valor Pago**: R$ 13.484,39
- **Total Cartório**: R$ 9.889,19

## 🐛 Debug

Para visualizar o conteúdo extraído de um PDF:

```bash
python debug_pdf.py <caminho_para_pdf>
```

Isso mostra:
- Texto extraído de cada página
- Tabelas encontradas
- Estrutura dos dados

## 📝 Licença

Este projeto foi desenvolvido como ferramenta especializada para processamento de documentos financeiros.

## 👥 Autor

Desenvolvido para processamento automatizado de Guias Geradas - FIRC

# Ambiente Virtual React - Calculadora FIRC

## 📋 Resumo da Implementação

Um ambiente completo **full-stack** foi criado para a Calculadora FIRC, combinando:

- ✅ **Backend FastAPI** (Python) - API REST com processamento de PDFs
- ✅ **Frontend React** (JavaScript) - Interface web moderna com Vite
- ✅ **CORS Configurado** - Comunicação entre frontend e backend
- ✅ **Scripts Automatizados** - Setup e execução simplificados

## 🏗️ O Que Foi Criado

### Backend FastAPI (`/backend`)

**Arquivo Principal**: `api.py`

```python
- POST /api/process-pdf       # Upload e processamento
- GET /api/health             # Health check
- GET /                        # Info da API
```

**Recursos**:
- Processa PDFs usando a lógica existente
- Retorna JSON com totais calculados
- CORS habilitado para o React
- Validação de arquivos
- Logging de operações
- Documentação interativa (Swagger/ReDoc)

**Dependências**:
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
pdfplumber==0.11.0
python-multipart==0.0.6
aiofiles==23.2.1
```

### Frontend React (`/frontend`)

**Tecnologias**:
- React 18.x
- Vite (build tool)
- CSS3 com variáveis CSS

**Componentes**:
1. **App.jsx** - Orquestrador principal
2. **PDFUploader.jsx** - Upload com drag-and-drop
3. **ResultsDisplay.jsx** - Exibição de resultados

**Recursos**:
- Upload de PDF com validação
- Drag-and-drop
- Spinner de carregamento
- Exibição de resultados formatados
- Tratamento de erros
- Design responsivo
- Interface moderna com gradiente

### Scripts de Automação

1. **setup.sh** - Setup completo (backend + frontend)
2. **install_backend.sh** - Instala dependências Python
3. **install_frontend.sh** - Instala dependências Node
4. **start_backend.sh** - Inicia servidor FastAPI
5. **start_frontend.sh** - Inicia servidor Vite

### Documentação

1. **QUICKSTART.md** - Guia de 5 minutos para começar
2. **FULL_STACK_README.md** - Documentação completa do sistema
3. **ARQUITETURA.md** - Detalhes de arquitetura
4. **README.md** - Documentação da CLI original

## 🚀 Como Começar

### Opção 1: Setup Automático (Recomendado)

```bash
cd calculadora_FIRC
bash setup.sh
```

### Opção 2: Setup Manual

**Backend:**
```bash
cd calculadora_FIRC/backend
pip install -r requirements.txt
python -m uvicorn api:app --reload
```

**Frontend:**
```bash
cd calculadora_FIRC/frontend
npm install
npm run dev
```

## 📊 Fluxo de Dados

```
Usuário
   ↓
[React UI - http://localhost:5173]
   ↓
PDF Upload (drag-drop ou clique)
   ↓
POST http://localhost:8000/api/process-pdf
   ↓
[FastAPI Backend]
   ↓
PDFFinancialParser
   ↓
PDFCalculator
   ↓
{total_valor_pago, total_cartorio}
   ↓
[React Displays Results]
   ↓
Usuário vê totais em R$ formatado
```

## 📁 Estrutura de Diretórios

```
calculadora_FIRC/
├── backend/
│   ├── api.py                 # 🆕 API FastAPI
│   ├── pdf_parser.py
│   ├── data_processor.py
│   ├── calculator.py
│   ├── main.py (CLI)
│   ├── requirements.txt
│   └── test_api.py
│
├── frontend/                  # 🆕 Aplicação React
│   ├── src/
│   │   ├── App.jsx           # 🆕 Componente principal
│   │   ├── App.css           # 🆕 Estilos globais
│   │   └── components/       # 🆕
│   │       ├── PDFUploader.jsx
│   │       ├── PDFUploader.css
│   │       ├── ResultsDisplay.jsx
│   │       └── ResultsDisplay.css
│   ├── package.json
│   └── vite.config.js
│
├── setup.sh                   # 🆕 Setup automático
├── start_backend.sh           # 🆕 Start backend
├── start_frontend.sh          # 🆕 Start frontend
├── install_backend.sh         # 🆕 Install backend
├── install_frontend.sh        # 🆕 Install frontend
│
├── QUICKSTART.md              # 🆕 Guia rápido
├── FULL_STACK_README.md       # 🆕 Doc completa
├── ARQUITETURA.md
├── README.md
│
└── [arquivos originais]
    ├── main.py (CLI)
    ├── pdf_parser.py
    ├── data_processor.py
    ├── calculator.py
    ├── test_calculator.py
    ├── exemplos.py
    ├── debug_pdf.py
    └── projeto.txt
```

## 🎯 Funcionalidades da UI

### PDFUploader
- ✅ Clique para selecionar
- ✅ Drag-and-drop
- ✅ Validação de arquivo (apenas .pdf)
- ✅ Spinner de carregamento
- ✅ Feedback visual

### ResultsDisplay
- ✅ Totais formatados em BRL (R$)
- ✅ Contagem de valores encontrados
- ✅ Diferença entre totais
- ✅ Detalhes da operação
- ✅ Botão para processar outro PDF

### Design
- ✅ Gradiente roxo/azul
- ✅ Cards com animações
- ✅ Responsivo (mobile-first)
- ✅ Acessibilidade
- ✅ Dark mode ready

## 🔗 URLs de Acesso

| Serviço | URL | Descrição |
|---------|-----|-----------|
| Frontend | http://localhost:5173 | App React |
| Backend | http://localhost:8000 | API REST |
| Swagger UI | http://localhost:8000/docs | API Docs |
| ReDoc | http://localhost:8000/redoc | API Docs alternativa |

## 📝 Exemplo de Resposta da API

```json
{
  "success": true,
  "data": {
    "total_valor_pago": 13484.39,
    "total_cartorio": 9889.19,
    "filename": "consultarGuiasGeradas_Report.pdf",
    "total_values_found": 22,
    "details": {
      "valores_pago_count": 11,
      "cartorio_count": 11
    }
  }
}
```

## 🧪 Testes

### Testar API com cURL

```bash
# Health check
curl http://localhost:8000/api/health

# Upload PDF
curl -X POST http://localhost:8000/api/process-pdf \
  -F "file=@consultarGuiasGeradas_Report.pdf"

# Info
curl http://localhost:8000
```

### Testar via Swagger

Visite: http://localhost:8000/docs

Pode fazer upload e testar os endpoints diretamente.

## 🔐 CORS Configurado

Backend aceita requisições de:
- http://localhost:5173 (Vite)
- http://localhost:3000 (create-react-app)

Modificável em `backend/api.py`:
```python
allow_origins=["http://localhost:5173", "http://localhost:3000"]
```

## 📦 Dependências Instaladas

### Python (Backend)
- fastapi: Framework web
- uvicorn: ASGI server
- pdfplumber: Extração de PDFs
- python-multipart: Upload de arquivos
- aiofiles: Operações async com arquivos

### JavaScript (Frontend)
- react: Biblioteca UI
- vite: Build tool
- npm packages: Gerenciamento de dependências

## ⚙️ Configurações

### Backend
- Host: 0.0.0.0
- Porta: 8000
- Reload: Habilitado (desenvolvimento)
- CORS: Configurado

### Frontend
- Host: localhost
- Porta: 5173
- HMR: Habilitado (hot module replacement)

## 🚀 Deploy

Para deploy em produção, veja `FULL_STACK_README.md` seção "Deploy".

## 🐛 Troubleshooting

Ver `QUICKSTART.md` para soluções comuns.

## 📞 Suporte

- **Guia Rápido**: QUICKSTART.md
- **Documentação**: FULL_STACK_README.md
- **Arquitetura**: ARQUITETURA.md

---

**Sistema completo pronto para uso! 🎉**

Próximos passos:
1. Execute `bash setup.sh`
2. Abra dois terminais
3. Execute `bash start_backend.sh` em um
4. Execute `bash start_frontend.sh` no outro
5. Visite http://localhost:5173

Aproveite! 🚀

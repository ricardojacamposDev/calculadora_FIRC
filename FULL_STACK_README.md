# Calculadora FIRC - Sistema Web Completo

## 🏗️ Arquitetura

O sistema agora possui uma arquitetura completa com:

- **Backend**: FastAPI (Python) na porta 8000
- **Frontend**: React com Vite na porta 5173
- **Comunicação**: API REST via HTTP

```
┌─────────────────────────────────────────┐
│         React Web Interface             │
│      (http://localhost:5173)            │
│                                         │
│  ✓ Upload de PDF                        │
│  ✓ Exibição de Resultados               │
│  ✓ Interface Responsiva                 │
└────────────────┬────────────────────────┘
                 │
                 │ HTTP Request/Response
                 ▼
┌─────────────────────────────────────────┐
│      FastAPI Backend (Python)           │
│     (http://localhost:8000)             │
│                                         │
│  ✓ Processamento de PDF                 │
│  ✓ Cálculo de Totais                    │
│  ✓ CORS Habilitado                      │
└─────────────────────────────────────────┘
```

## 📁 Estrutura de Diretórios

```
calculadora_FIRC/
├── backend/                    # Backend FastAPI
│   ├── api.py                 # API REST principal
│   ├── pdf_parser.py          # Parser de PDF
│   ├── data_processor.py      # Processador de dados
│   ├── calculator.py          # Calculadora
│   ├── main.py                # CLI (legado)
│   └── requirements.txt       # Dependências Python
│
├── frontend/                  # Frontend React + Vite
│   ├── src/
│   │   ├── App.jsx           # Componente principal
│   │   ├── App.css           # Estilos globais
│   │   └── components/
│   │       ├── PDFUploader.jsx      # Componente upload
│   │       ├── PDFUploader.css
│   │       ├── ResultsDisplay.jsx   # Componente resultados
│   │       └── ResultsDisplay.css
│   ├── package.json
│   └── vite.config.js
│
├── start_backend.sh           # Script iniciar backend
├── start_frontend.sh          # Script iniciar frontend
├── install_backend.sh         # Script instalar backend
├── install_frontend.sh        # Script instalar frontend
│
└── [arquivos originais do projeto...]
```

## 🚀 Como Usar

### Instalação Inicial

#### 1. Backend

```bash
# Instalar dependências do backend
bash install_backend.sh

# Ou manualmente:
cd backend
pip install -r requirements.txt
```

#### 2. Frontend

```bash
# Instalar dependências do frontend
bash install_frontend.sh

# Ou manualmente:
cd frontend
npm install
```

### Executando o Sistema

#### Terminal 1 - Backend

```bash
bash start_backend.sh

# Ou manualmente:
cd backend
python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em:
- **API**: http://localhost:8000
- **Docs Interativa**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

#### Terminal 2 - Frontend

```bash
bash start_frontend.sh

# Ou manualmente:
cd frontend
npm run dev
```

A aplicação web estará disponível em:
- **Aplicação**: http://localhost:5173

## 🎯 Funcionalidades

### Frontend React

✅ **Upload de PDF**
- Suporte drag-and-drop
- Validação de formato
- Spinner de carregamento

✅ **Processamento Assíncrono**
- Requisição HTTP POST para o backend
- Tratamento de erros

✅ **Exibição de Resultados**
- Mostra totais formatados em R$
- Conta de valores encontrados
- Detalhes da operação

✅ **Design Responsivo**
- Adaptado para mobile
- Interface moderna com gradiente
- Animações suaves

### Backend FastAPI

✅ **Endpoints REST**

```bash
GET  /              # Informações da API
GET  /api/health    # Health check
POST /api/process-pdf  # Processa PDF (resposta completa)
POST /api/process-pdf/simple  # Resposta simplificada
```

✅ **CORS Habilitado**
- Permite requisições do React em http://localhost:5173
- Permite requisições do React em http://localhost:3000

✅ **Validações**
- Verifica se arquivo é PDF
- Tratamento de erros com mensagens claras

✅ **Logs**
- Logging de operações
- Rastreamento de erros

## 📊 Exemplo de Fluxo

1. **Usuário acessa** http://localhost:5173
2. **Usuário faz upload** de um PDF
3. **Frontend envia** POST request para http://localhost:8000/api/process-pdf
4. **Backend processa** o PDF usando a lógica Python existente
5. **Backend retorna** JSON com resultados
6. **Frontend exibe** os totais formatados em BRL

### Exemplo de Resposta

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

### Teste Manual via cURL

```bash
# Upload de um PDF
curl -X POST http://localhost:8000/api/process-pdf \
  -F "file=@caminho/para/arquivo.pdf"

# Health check
curl http://localhost:8000/api/health

# Informações da API
curl http://localhost:8000
```

### Teste via Swagger UI

Acesse: http://localhost:8000/docs

Pode testar os endpoints diretamente pela interface.

## ⚙️ Configuração

### Frontend - Variáveis de Ambiente

Criar arquivo `.env` no diretório `frontend/`:

```env
VITE_API_URL=http://localhost:8000
```

Usar em `App.jsx`:
```jsx
const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const response = await fetch(`${apiUrl}/api/process-pdf`, {
  method: 'POST',
  body: formData,
});
```

### Backend - Configurações

Arquivo `backend/api.py`:

```python
# CORS - modificar origins conforme necessário
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",   # React (create-react-app)
        "http://localhost:5173",   # React (Vite)
        "https://seu-dominio.com"  # Produção
    ],
)
```

## 📦 Dependências

### Backend
- fastapi==0.109.0
- uvicorn[standard]==0.27.0
- pdfplumber==0.11.0
- python-multipart==0.0.6
- aiofiles==23.2.1

### Frontend
- react@^18
- vite@latest

## 🔍 Troubleshooting

### Erro: "Could not connect to server"

**Solução**: Verifique se o backend está rodando na porta 8000

```bash
# Testar conexão
curl http://localhost:8000
```

### Erro: "CORS policy"

**Solução**: Verifique se a URL está adicionada em `allow_origins` no `api.py`

### Erro: "PDF não foi processado"

**Solução**: Verifique se o arquivo é PDF válido e confira os logs do backend

## 🚀 Deploy

### Backend (FastAPI)

```bash
# Usar Gunicorn em produção
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker api:app
```

### Frontend (React)

```bash
# Build para produção
cd frontend
npm run build

# Servir com servidor estático
npm install -g serve
serve -s dist -l 3000
```

## 📝 Próximas Melhorias

- [ ] Adicionar autenticação (JWT)
- [ ] Implementar histórico de uploads
- [ ] Dashboard de estatísticas
- [ ] Suporte a múltiplos formatos
- [ ] Testes E2E (Cypress/Playwright)
- [ ] Containerizar com Docker
- [ ] CI/CD com GitHub Actions

## 📄 Licença

Projeto desenvolvido para processamento de Guias Geradas - FIRC

## 📞 Suporte

Para dúvidas ou issues, verifique:
- Backend logs: Terminal do `start_backend.sh`
- Frontend console: DevTools do navegador
- Documentação da API: http://localhost:8000/docs

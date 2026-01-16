# 🚀 Guia Rápido - Calculadora FIRC

## 5 Minutos para Ter o Sistema Rodando

### Pré-requisitos
- Python 3.8+ instalado
- Node.js e npm instalados
- 2 terminais abertos

---

## ⚡ Início Rápido

### 1️⃣ Instalar Backend (Terminal 1)

```bash
cd calculadora_FIRC
bash install_backend.sh
```

⏳ Aguarde ~2 minutos enquanto instala as dependências Python.

### 2️⃣ Instalar Frontend (Terminal 2)

```bash
cd calculadora_FIRC
bash install_frontend.sh
```

⏳ Aguarde ~1 minuto enquanto instala as dependências Node.

### 3️⃣ Rodar Backend (Terminal 1)

```bash
bash start_backend.sh
```

✅ Quando ver `Uvicorn running on http://0.0.0.0:8000`, o backend está pronto.

Dica: Visite http://localhost:8000/docs para ver a documentação interativa da API.

### 4️⃣ Rodar Frontend (Terminal 2)

```bash
bash start_frontend.sh
```

✅ Quando ver `Local: http://localhost:5173`, o frontend está pronto.

---

## 🎯 Usando a Aplicação

1. Abra seu navegador em: **http://localhost:5173**

2. Você verá:
   ```
   💰 Calculadora FIRC
   Processador de Documentos Financeiros
   ```

3. Clique na área de upload ou arraste um PDF

4. A aplicação:
   - Envia o PDF para o backend
   - Processa e calcula os totais
   - Mostra os resultados formatados em R$

---

## 📊 Estrutura Criada

```
calculadora_FIRC/
├── backend/          ← API FastAPI (porta 8000)
├── frontend/         ← App React com Vite (porta 5173)
├── start_backend.sh  ← Iniciar backend
├── start_frontend.sh ← Iniciar frontend
└── FULL_STACK_README.md ← Documentação completa
```

---

## 🧪 Testar Rapidamente

### Teste 1: Verificar se Backend Está Rodando

```bash
curl http://localhost:8000/api/health
```

**Resposta esperada:**
```json
{"status": "healthy", "service": "Calculadora FIRC API"}
```

### Teste 2: Ver Documentação da API

Visite: http://localhost:8000/docs

Pode fazer testes diretamente pelo Swagger UI.

### Teste 3: Upload via cURL

```bash
curl -X POST http://localhost:8000/api/process-pdf \
  -F "file=@calculadora_FIRC/consultarGuiasGeradas_Report.pdf"
```

---

## 📁 Arquivos Principais

### Backend (`backend/`)
- `api.py` - API REST FastAPI
- `pdf_parser.py` - Parser de PDF
- `calculator.py` - Cálculo de totais
- `data_processor.py` - Processamento de valores

### Frontend (`frontend/src/`)
- `App.jsx` - Componente principal React
- `components/PDFUploader.jsx` - Upload de arquivo
- `components/ResultsDisplay.jsx` - Exibição de resultados

---

## 🎨 Funcionalidades da UI

✅ **Drag & Drop** - Arraste PDFs para a área de upload  
✅ **Validação** - Apenas PDFs são aceitos  
✅ **Carregamento** - Spinner animado durante processamento  
✅ **Resultados** - Exibição clara com formatação BRL  
✅ **Responsivo** - Funciona em mobile e desktop  
✅ **Erros** - Mensagens amigáveis se algo falhar  

---

## 🔗 URLs Úteis

| Serviço | URL | Descrição |
|---------|-----|-----------|
| **Frontend** | http://localhost:5173 | Aplicação React |
| **Backend** | http://localhost:8000 | API REST |
| **API Docs** | http://localhost:8000/docs | Swagger UI |
| **API ReDoc** | http://localhost:8000/redoc | ReDoc |
| **Health** | http://localhost:8000/api/health | Status da API |

---

## ⚠️ Troubleshooting

### "Could not connect to server"
Verifique se o backend está rodando:
```bash
curl http://localhost:8000
```

### "Port 8000 is already in use"
Mudar porta no `start_backend.sh`:
```bash
python -m uvicorn api:app --reload --host 0.0.0.0 --port 8001
```

### "Port 5173 is already in use"
Mudar porta no `start_frontend.sh`:
```bash
npm run dev -- --port 5174
```

### "CORS error"
Verifique se o frontend está em http://localhost:5173 e não http://localhost:3000

---

## 📝 Próximas Passos

1. **Deploy**: Veja `FULL_STACK_README.md` para deploy em produção
2. **Autenticação**: Adicione login se necessário
3. **Histórico**: Salve uploads anteriores
4. **Dashboard**: Crie estatísticas de uso

---

## 📞 Dúvidas?

- Documentação completa: [FULL_STACK_README.md](FULL_STACK_README.md)
- Arquitetura detalhada: [ARQUITETURA.md](ARQUITETURA.md)
- Backend (CLI): [README.md](README.md)

---

**Bom uso! 🚀**

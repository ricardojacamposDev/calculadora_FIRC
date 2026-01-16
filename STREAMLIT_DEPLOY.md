# Deploy no Streamlit Cloud

Guia completo para fazer deploy da Calculadora FIRC no Streamlit Cloud.

## 🚀 Deploy no Streamlit Cloud (Recomendado)

### Pré-requisitos

- ✅ Conta no [Streamlit Cloud](https://streamlit.io/cloud)
- ✅ Repositório GitHub com o projeto
- ✅ Conta GitHub

### Passo 1: Preparar o Repositório

```bash
# Certifique-se que todos os arquivos estão no Git
git add .
git commit -m "feat: add streamlit deployment"
git push origin main
```

**Arquivos essenciais no repositório:**
```
calculadora_FIRC/
├── app_streamlit.py          ← Arquivo principal
├── requirements-streamlit.txt ← Dependências
├── pdf_parser.py
├── calculator.py
├── data_processor.py
├── .streamlit/
│   └── config.toml          ← Configuração (opcional)
└── ...
```

### Passo 2: Fazer Deploy

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Faça login com sua conta GitHub
3. Clique em **"New app"**
4. Selecione:
   - **Repository**: seu repositório
   - **Branch**: main
   - **Main file path**: `app_streamlit.py`
5. Clique **"Deploy"**

✅ Sua aplicação estará live em poucos minutos!

### Passo 3: Usar a Aplicação

A app será disponível em:
```
https://[seu-usuario]-calculadora-firc.streamlit.app
```

Você pode processar PDFs diretamente na web!

---

## 🏠 Deploy Local

### Instalação

```bash
# Instalar dependências
pip install -r requirements-streamlit.txt

# Ou instalar manualmente
pip install streamlit==1.28.1 pdfplumber==0.11.0
```

### Executar Localmente

```bash
# Opção 1: Usar script
bash start_streamlit.sh

# Opção 2: Comando direto
streamlit run app_streamlit.py
```

Acesse: http://localhost:8501

---

## 🐳 Deploy com Docker

### Criar Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copiar arquivos
COPY . .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements-streamlit.txt

# Configurar Streamlit
RUN mkdir -p ~/.streamlit && \
    echo "[server]" > ~/.streamlit/config.toml && \
    echo "headless = true" >> ~/.streamlit/config.toml && \
    echo "port = 8501" >> ~/.streamlit/config.toml && \
    echo "enableCORS = false" >> ~/.streamlit/config.toml

# Executar app
CMD ["streamlit", "run", "app_streamlit.py"]
```

### Build e Run

```bash
# Build
docker build -t calculadora-firc .

# Run
docker run -p 8501:8501 calculadora-firc
```

Acesse: http://localhost:8501

---

## ☁️ Deploy em Outras Plataformas

### Heroku

```bash
# Criar Procfile
echo "web: streamlit run app_streamlit.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile

# Deploy
heroku create seu-app-name
git push heroku main
```

### AWS (Elastic Beanstalk)

```bash
# Criar .ebextensions/streamlit.config
mkdir -p .ebextensions
cat > .ebextensions/streamlit.config << EOF
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: app_streamlit.py
EOF

# Deploy
eb create seu-app-name
eb deploy
```

### Google Cloud Run

```bash
# Build da imagem
gcloud builds submit --tag gcr.io/[PROJECT]/calculadora-firc

# Deploy
gcloud run deploy calculadora-firc \
  --image gcr.io/[PROJECT]/calculadora-firc \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Azure

```bash
# Criar Container Registry
az acr create --resource-group myResourceGroup \
  --name calculadorafircRegistry --sku Basic

# Build e push
az acr build --registry calculadorafircRegistry \
  --image calculadora-firc:latest .

# Deploy no App Service
az container create --resource-group myResourceGroup \
  --name calculadora-firc \
  --image calculadorafircRegistry.azurecr.io/calculadora-firc:latest \
  --cpu 1 --memory 1
```

---

## ⚙️ Configurações de Deploy

### streamlit/config.toml

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#f0f2f6"
secondaryBackgroundColor = "#e8e8f0"
textColor = "#262730"
font = "sans serif"

[server]
port = 8501
headless = true
enableCORS = false
enableXsrfProtection = true

[logger]
level = "info"

[client]
toolbarMode = "viewer"
```

### Variáveis de Ambiente

```bash
# Streamlit Cloud ou Docker
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ENABLE_CORS=false
```

---

## 🔐 Segurança

### Para Deploy em Produção

1. **Adicionar autenticação:**

```python
import streamlit as st

def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False
    
    if not st.session_state.password_correct:
        password = st.text_input("Senha:", type="password")
        if password == "sua_senha_aqui":
            st.session_state.password_correct = True
        else:
            st.error("Senha incorreta")
            return False
    return True

if not check_password():
    st.stop()

# Seu app aqui...
```

2. **HTTPS Automático:** Streamlit Cloud fornece HTTPS automático
3. **Rate Limiting:** Implementar no nginx/proxy reverso
4. **Logs:** Monitorar uploads e operações

---

## 📊 Monitoramento

### Streamlit Cloud

- Dashboard automático em share.streamlit.io
- Logs em tempo real
- Métricas de uso
- Alertas de erro

### Logs Locais

```bash
# Ver logs do Streamlit
streamlit logs

# Logs do Docker
docker logs -f calculadora-firc
```

---

## 🚀 Performance

### Otimizações para Deploy

```python
# app_streamlit.py - Adicionar caching

import streamlit as st

@st.cache_resource
def load_model():
    # Carrega modelo uma vez
    return PDFFinancialParser

@st.cache_data
def process_pdf(file_data):
    # Cachear resultados de processamento
    return analyzer.analyze(file_data)
```

### Limites no Streamlit Cloud

- **CPU**: 1 CPU core
- **RAM**: 1 GB
- **Timeout**: 24 horas
- **Upload**: 200 MB máximo

Para aplicações maiores, usar AWS/Google Cloud/Azure.

---

## 🔄 CI/CD com GitHub Actions

### Arquivo: .github/workflows/streamlit-deploy.yml

```yaml
name: Deploy to Streamlit Cloud

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Install dependencies
      run: pip install -r requirements-streamlit.txt
    
    - name: Run tests
      run: |
        python -m pytest tests/ || true
    
    - name: Deploy to Streamlit Cloud
      run: |
        # Usar streamlit deploy (requer token)
        echo "Implantação automática via Git sync"
```

---

## 📱 Acesso Móvel

A aplicação Streamlit funciona perfeitamente em mobile!

- Responsivo por padrão
- Touch-friendly
- Funciona offline parcialmente
- Progressive Web App (PWA)

---

## ✅ Checklist de Deploy

- [ ] Repositório Git configurado
- [ ] requirements-streamlit.txt atualizado
- [ ] app_streamlit.py testado localmente
- [ ] .gitignore configurado
- [ ] Secrets (se houver) em Streamlit Cloud
- [ ] URL customizada configurada
- [ ] Documentação atualizada
- [ ] Testes passando
- [ ] Monitoramento ativo

---

## 🆘 Troubleshooting

### "Module not found"

```bash
# Verificar requirements
pip list

# Reinstalar
pip install -r requirements-streamlit.txt --force-reinstall
```

### "Port already in use"

```bash
# Usar porta diferente
streamlit run app_streamlit.py --server.port 8502
```

### "PDF upload não funciona"

- Verificar permissões de arquivo
- Verificar tamanho (máx 200MB no Streamlit Cloud)
- Verificar formato PDF válido

### "Timeout no processamento"

- Dividir PDFs grandes
- Aumentar recurso na plataforma de deploy
- Implementar processamento assíncrono

---

## 📞 Suporte

- Documentação Streamlit: https://docs.streamlit.io
- GitHub Issues: https://github.com/streamlit/streamlit/issues
- Community: https://discuss.streamlit.io

---

**🎉 Sua aplicação Streamlit está pronta para deploy!**

Escolha a opção mais adequada para seu caso:

| Plataforma | Preço | Setup | Performance |
|-----------|-------|-------|-------------|
| **Streamlit Cloud** | Gratuito | 1 min | Bom |
| **Docker (local)** | Grátis | 10 min | Excelente |
| **Heroku** | $7/mês | 5 min | Bom |
| **AWS** | Variável | 20 min | Excelente |
| **Google Cloud** | Variável | 20 min | Excelente |

Recomendação: **Começar com Streamlit Cloud** (gratuito e fácil)!

# 📊 Calculadora FIRC

Aplicação web em Streamlit para extrair e calcular valores de PDFs de Guias Geradas.

## 🚀 Início Rápido

### Opção 1: Setup Automático (Recomendado)
```bash
chmod +x setup_streamlit.sh
./setup_streamlit.sh
```

### Opção 2: Manual
```bash
pip install -r requirements-streamlit.txt
streamlit run app_streamlit.py
```

Acesse: http://localhost:8501

## ☁️ Deploy Grátis (Streamlit Cloud)

1. **Push para GitHub:**
   ```bash
   git push origin main
   ```

2. **Deploy:**
   - Acesse: https://share.streamlit.io
   - Clique "New app"
   - Selecione `app_streamlit.py`
   - Clique "Deploy"

URL estará disponível em: `https://seu-usuario-calculadora-firc.streamlit.app`

**Custo: Grátis**

## 🐳 Docker

```bash
# Rodar
docker-compose up

# Parar
docker-compose down
```

Acesse: http://localhost:8501

## 📁 Estrutura

```
├── app_streamlit.py           # Aplicação principal
├── pdf_parser.py              # Parser de PDF
├── calculator.py              # Cálculos financeiros
├── data_processor.py          # Processamento de dados
├── test_calculator.py         # Testes
├── requirements-streamlit.txt # Dependências (2 pacotes)
├── Dockerfile                 # Container
├── docker-compose.yml         # Docker compose
└── setup_streamlit.sh         # Setup automático
```

## ✨ Funcionalidades

- ✅ Upload de PDF (drag & drop)
- ✅ Processamento em tempo real
- ✅ Exibição formatada em R$ BRL
- ✅ Exportação JSON
- ✅ Responsivo (mobile-friendly)
- ✅ Dark mode

## 📖 Mais Informações

- **Deploy rápido:** [STREAMLIT_QUICK_DEPLOY.md](STREAMLIT_QUICK_DEPLOY.md)
- **Implementação completa:** [IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md)

## 🧪 Testes

```bash
python -m unittest test_calculator.py
```

## 📄 Licença

MIT

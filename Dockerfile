FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos do projeto
COPY . .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expor porta
EXPOSE 8501

# Configurar Streamlit
RUN mkdir -p ~/.streamlit && \
    echo "[server]" > ~/.streamlit/config.toml && \
    echo "headless = true" >> ~/.streamlit/config.toml && \
    echo "port = 8501" >> ~/.streamlit/config.toml && \
    echo "enableCORS = false" >> ~/.streamlit/config.toml

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Executar aplicação
CMD ["streamlit", "run", "app_streamlit.py", "--server.address=0.0.0.0"]

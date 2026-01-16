#!/bin/bash

# Script para instalar Streamlit
echo "📦 Instalando Streamlit e dependências..."

pip install -r requirements-streamlit.txt

echo ""
echo "✅ Dependências instaladas com sucesso!"
echo ""
echo "Para rodar a aplicação:"
echo "  bash start_streamlit.sh"
echo ""
echo "Ou:"
echo "  streamlit run app_streamlit.py"

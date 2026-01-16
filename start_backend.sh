#!/bin/bash

# Script para iniciar o backend FastAPI
echo "🚀 Iniciando backend FastAPI..."
echo "📍 API disponível em: http://localhost:8000"
echo "📖 Docs em: http://localhost:8000/docs"
echo ""
echo "Pressione Ctrl+C para parar o servidor"
echo ""

cd backend
python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000

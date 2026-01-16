#!/bin/bash

# Script de setup completo para Calculadora FIRC
# Instala backend e frontend automaticamente

set -e  # Exit on error

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║        CALCULADORA FIRC - Setup Completo                       ║"
echo "║     Processador de Documentos Financeiros                      ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}📦 INSTALAÇÃO AUTOMÁTICA${NC}"
echo ""

# Verificar pré-requisitos
echo "🔍 Verificando pré-requisitos..."

# Python
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}⚠️  Python não encontrado. Instale Python 3.8+${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python encontrado: $(python3 --version)${NC}"

# Node.js
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}⚠️  Node.js não encontrado. Instale Node.js${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Node.js encontrado: $(node --version)${NC}"

# npm
if ! command -v npm &> /dev/null; then
    echo -e "${YELLOW}⚠️  npm não encontrado. Instale Node.js${NC}"
    exit 1
fi
echo -e "${GREEN}✓ npm encontrado: $(npm --version)${NC}"

echo ""
echo -e "${BLUE}🔧 INSTALANDO DEPENDÊNCIAS${NC}"
echo ""

# Backend
echo "📥 Instalando dependências do Backend..."
if [ -d "backend" ]; then
    cd backend
    python3 -m pip install -r requirements.txt --quiet
    cd ..
    echo -e "${GREEN}✓ Backend pronto${NC}"
else
    echo -e "${YELLOW}⚠️  Diretório backend não encontrado${NC}"
fi

echo ""

# Frontend
echo "📥 Instalando dependências do Frontend..."
if [ -d "frontend" ]; then
    cd frontend
    npm install --silent
    cd ..
    echo -e "${GREEN}✓ Frontend pronto${NC}"
else
    echo -e "${YELLOW}⚠️  Diretório frontend não encontrado${NC}"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo -e "${GREEN}✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!${NC}"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

echo -e "${BLUE}🚀 PRÓXIMOS PASSOS:${NC}"
echo ""
echo "1️⃣  Abra um novo Terminal e execute:"
echo "   ${YELLOW}bash start_backend.sh${NC}"
echo ""
echo "2️⃣  Abra outro Terminal e execute:"
echo "   ${YELLOW}bash start_frontend.sh${NC}"
echo ""
echo "3️⃣  Acesse a aplicação em:"
echo "   ${YELLOW}http://localhost:5173${NC}"
echo ""
echo -e "${BLUE}📚 Documentação:${NC}"
echo "   - Guia Rápido: QUICKSTART.md"
echo "   - Documentação Completa: FULL_STACK_README.md"
echo "   - Arquitetura: ARQUITETURA.md"
echo ""

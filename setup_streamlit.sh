#!/bin/bash

# ✨ Calculadora FIRC - Streamlit Setup Script

echo "╔════════════════════════════════════════════════════════╗"
echo "║  Calculadora FIRC - Streamlit Setup & Deploy          ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para exibir seções
section() {
    echo -e "${BLUE}→ $1${NC}"
}

success() {
    echo -e "${GREEN}✓ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# 1. Verificar Python
section "Verificando Python..."
if ! command -v python3 &> /dev/null; then
    warning "Python3 não encontrado. Por favor, instale Python 3.8+"
    exit 1
fi
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
success "Python $PYTHON_VERSION encontrado"

# 2. Criar venv (opcional)
if [ ! -d "venv" ]; then
    section "Criando ambiente virtual..."
    python3 -m venv venv
    success "Ambiente virtual criado"
else
    success "Ambiente virtual já existe"
fi

# 3. Ativar venv
section "Ativando ambiente virtual..."
source venv/bin/activate
success "Ambiente virtual ativado"

# 4. Instalar dependências
section "Instalando dependências Streamlit..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements-streamlit.txt
success "Dependências instaladas"

# 5. Verificar arquivos
section "Verificando arquivos..."
FILES=(
    "app_streamlit.py"
    "pdf_parser.py"
    "calculator.py"
    "data_processor.py"
    "requirements-streamlit.txt"
)

MISSING_FILES=false
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ $file (FALTANDO)"
        MISSING_FILES=true
    fi
done

if [ "$MISSING_FILES" = true ]; then
    warning "Alguns arquivos estão faltando!"
    exit 1
fi
success "Todos os arquivos encontrados"

# 6. Menu de opções
echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║  O QUE DESEJA FAZER?                                   ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "1) Rodar app localmente (localhost:8501)"
echo "2) Rodar com Docker"
echo "3) Ver instruções de deploy no Streamlit Cloud"
echo "4) Sair"
echo ""

read -p "Escolha uma opção (1-4): " choice

case $choice in
    1)
        echo ""
        section "Iniciando Streamlit..."
        echo ""
        echo "📱 App rodando em: ${BLUE}http://localhost:8501${NC}"
        echo "📌 Pressione Ctrl+C para parar"
        echo ""
        streamlit run app_streamlit.py --server.address localhost
        ;;
    2)
        echo ""
        if ! command -v docker &> /dev/null; then
            warning "Docker não está instalado"
            warning "Instale em: https://www.docker.com"
            exit 1
        fi
        
        section "Buildando imagem Docker..."
        docker build -t calculadora-firc .
        
        success "Build concluído!"
        echo ""
        section "Iniciando container..."
        echo ""
        docker run -p 8501:8501 calculadora-firc
        ;;
    3)
        clear
        echo "╔════════════════════════════════════════════════════════╗"
        echo "║  DEPLOY NO STREAMLIT CLOUD (Recomendado - Gratuito)  ║"
        echo "╚════════════════════════════════════════════════════════╝"
        echo ""
        echo "1️⃣  Crie um repositório no GitHub (se não tiver)"
        echo "    → https://github.com/new"
        echo ""
        echo "2️⃣  Push dos arquivos"
        echo "    → git add ."
        echo "    → git commit -m 'Add streamlit app'"
        echo "    → git push origin main"
        echo ""
        echo "3️⃣  Acesse Streamlit Cloud"
        echo "    → https://share.streamlit.io"
        echo ""
        echo "4️⃣  Faça login com GitHub"
        echo "    → Clique em 'Sign up'"
        echo "    → GitHub > Authorize"
        echo ""
        echo "5️⃣  Deploy a app"
        echo "    → Clique em 'New app'"
        echo "    → Selecione seu repositório"
        echo "    → Branch: main"
        echo "    → File: app_streamlit.py"
        echo "    → Clique em 'Deploy'"
        echo ""
        echo "6️⃣  Pronto! 🎉"
        echo "    → URL: https://seu-usuario-calculadora-firc.streamlit.app"
        echo ""
        echo "Mais detalhes em: STREAMLIT_QUICK_DEPLOY.md"
        read -p "Pressione ENTER para voltar..."
        ;;
    4)
        echo "Até logo! 👋"
        exit 0
        ;;
    *)
        warning "Opção inválida"
        exit 1
        ;;
esac

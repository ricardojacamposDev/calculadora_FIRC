"""
Calculadora FIRC - Aplicação Streamlit
Processador de Documentos Financeiros (Guias Geradas)
"""

import streamlit as st
import tempfile
import os
import json
from pathlib import Path
import sys

# Adiciona o diretório pai ao path para importar módulos
sys.path.insert(0, str(Path(__file__).parent))

from pdf_parser import PDFFinancialParser
from calculator import FinancialCalculator

# Configuração da página
st.set_page_config(
    page_title="Calculadora FIRC",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo customizado
st.markdown("""
    <style>
    .main {
        background: white;
    }
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .result-box {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    .metric-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="header">
        <h1>💰 Calculadora FIRC</h1>
        <p>Processador Inteligente de Documentos Financeiros</p>
        <p style="font-size: 0.9rem; opacity: 0.9;">Extrai e calcula totais de Guias Geradas</p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar com informações
with st.sidebar:
    st.header("📋 Informações")
    st.markdown("""
    ### O que faz?
    - 📄 Processa PDFs de Guias Geradas
    - 💸 Calcula totais de Valor Pago
    - 🏛️ Calcula totais de Cartório
    - 📊 Exibe estatísticas
    
    ### Recursos
    - ✅ Upload simples de PDF
    - ✅ Processamento em tempo real
    - ✅ Resultados em R$ (BRL)
    - ✅ Exportação de dados
    
    ### Versão
    v1.0.0 - Streamlit Edition
    """)
    
    st.markdown("---")
    
    st.subheader("📞 Suporte")
    st.markdown("""
    Dúvidas sobre uso? Verifique:
    - [Documentação](https://github.com)
    - [Issues](https://github.com)
    """)

# Inicializar session state
if 'results' not in st.session_state:
    st.session_state.results = None
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None

# Upload de PDF
st.subheader("📁 Selecione um PDF para Processar")

uploaded_file = st.file_uploader(
    "Arraste ou clique para selecionar um arquivo PDF",
    type=['pdf'],
    key='pdf_uploader'
)

# Processar arquivo
if uploaded_file is not None:
    st.session_state.uploaded_file = uploaded_file
    
    # Criar arquivo temporário
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name
    
    try:
        with st.spinner('⏳ Processando PDF...'):
            # Extrair dados
            parser = PDFFinancialParser(tmp_file_path)
            extracted_data = parser.extract_data()
            
            # Calcular totais
            calculator = FinancialCalculator()
            result = calculator.calculate_totals(extracted_data)
            
            # Salvar resultados no session state
            st.session_state.results = {
                'data': result,
                'filename': uploaded_file.name,
                'extracted_data': extracted_data
            }
        
        st.success('✅ PDF processado com sucesso!')
        
    except Exception as e:
        st.error(f'❌ Erro ao processar PDF: {str(e)}')
    
    finally:
        # Limpar arquivo temporário
        if os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)

# Exibir resultados
if st.session_state.results:
    results = st.session_state.results['data']
    filename = st.session_state.results['filename']
    extracted_data = st.session_state.results['extracted_data']
    
    st.markdown("---")
    st.subheader("📊 Resultados do Processamento")
    
    # Informação do arquivo
    with st.expander("📄 Informações do Arquivo", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Arquivo", filename.split('/')[-1])
        with col2:
            st.metric("Status", "✅ Processado")
    
    # Resultados principais em colunas
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-box">
            <h3>Valor Pago</h3>
            <p style="font-size: 2.5rem; font-weight: bold;">
                R$ {:.2f}
            </p>
            <p style="opacity: 0.9;">
                {} valores encontrados
            </p>
        </div>
        """.format(
            results['total_valor_pago'],
            len(extracted_data.get('valor_pago', []))
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-box">
            <h3>Cartório</h3>
            <p style="font-size: 2.5rem; font-weight: bold;">
                R$ {:.2f}
            </p>
            <p style="opacity: 0.9;">
                {} valores encontrados
            </p>
        </div>
        """.format(
            results['total_cartorio'],
            len(extracted_data.get('cartorio', []))
        ), unsafe_allow_html=True)
    
    # Estatísticas detalhadas
    st.markdown("---")
    st.subheader("📈 Estatísticas Detalhadas")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Valor Pago",
            f"R$ {results['total_valor_pago']:.2f}",
            delta=f"{len(extracted_data.get('valor_pago', []))} valores"
        )
    
    with col2:
        st.metric(
            "Total Cartório",
            f"R$ {results['total_cartorio']:.2f}",
            delta=f"{len(extracted_data.get('cartorio', []))} valores"
        )
    
    with col3:
        diferenca = results['total_valor_pago'] - results['total_cartorio']
        st.metric(
            "Diferença",
            f"R$ {abs(diferenca):.2f}",
            delta="Valor Pago > Cartório" if diferenca > 0 else "Cartório > Valor Pago"
        )
    
    with col4:
        total_valores = (
            len(extracted_data.get('valor_pago', [])) + 
            len(extracted_data.get('cartorio', []))
        )
        st.metric(
            "Total de Valores",
            total_valores,
            delta="linhas processadas"
        )
    
    # Detalhes dos valores extraídos
    st.markdown("---")
    st.subheader("🔍 Valores Extraídos")
    
    tab1, tab2 = st.tabs(["Valor Pago", "Cartório"])
    
    with tab1:
        valores_pago = extracted_data.get('valor_pago', [])
        if valores_pago:
            st.write(f"**Total de valores:** {len(valores_pago)}")
            
            # Mostra em colunas
            cols = st.columns(3)
            for idx, valor in enumerate(valores_pago[:30]):  # Mostra até 30
                with cols[idx % 3]:
                    st.write(f"💵 {valor}")
            
            if len(valores_pago) > 30:
                st.info(f"... e mais {len(valores_pago) - 30} valores")
        else:
            st.warning("Nenhum valor de Valor Pago encontrado")
    
    with tab2:
        cartorio = extracted_data.get('cartorio', [])
        if cartorio:
            st.write(f"**Total de valores:** {len(cartorio)}")
            
            # Mostra em colunas
            cols = st.columns(3)
            for idx, valor in enumerate(cartorio[:30]):  # Mostra até 30
                with cols[idx % 3]:
                    st.write(f"🏛️ {valor}")
            
            if len(cartorio) > 30:
                st.info(f"... e mais {len(cartorio) - 30} valores")
        else:
            st.warning("Nenhum valor de Cartório encontrado")
    
    # Resumo em JSON
    st.markdown("---")
    st.subheader("📋 Resumo JSON")
    
    resumo = {
        "arquivo": filename,
        "total_valor_pago": round(results['total_valor_pago'], 2),
        "total_cartorio": round(results['total_cartorio'], 2),
        "diferenca": round(results['total_valor_pago'] - results['total_cartorio'], 2),
        "quantidade_valores_pago": len(extracted_data.get('valor_pago', [])),
        "quantidade_cartorio": len(extracted_data.get('cartorio', [])),
        "total_de_valores": (
            len(extracted_data.get('valor_pago', [])) + 
            len(extracted_data.get('cartorio', []))
        )
    }
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.json(resumo)
    
    with col2:
        # Botão para copiar JSON
        json_str = json.dumps(resumo, indent=2, ensure_ascii=False)
        st.download_button(
            label="📥 Baixar JSON",
            data=json_str,
            file_name=f"resultado_{Path(filename).stem}.json",
            mime="application/json"
        )
    
    # Opção para resetar
    st.markdown("---")
    if st.button("🔄 Processar Outro PDF"):
        st.session_state.results = None
        st.session_state.uploaded_file = None
        st.rerun()

else:
    # Mensagem inicial
    st.info("""
    ### 👋 Bem-vindo à Calculadora FIRC
    
    1. **Selecione um PDF** de Guias Geradas usando o uploader acima
    2. **Aguarde o processamento** - a análise é rápida
    3. **Visualize os resultados** - totais em R$ formatados
    4. **Baixe os dados** - exporte em JSON se necessário
    
    ---
    
    **Exemplo de uso:**
    - Processe um PDF de relatório financeiro
    - Obtenha totais de Valor Pago e Cartório
    - Veja estatísticas detalhadas
    - Exporte os resultados
    """)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; opacity: 0.7; font-size: 0.9rem;">
        <p>Calculadora FIRC v1.0.0 | Streamlit Edition</p>
        <p>Processamento de Documentos Financeiros</p>
    </div>
    """, unsafe_allow_html=True)

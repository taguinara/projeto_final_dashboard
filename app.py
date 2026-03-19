import streamlit as st

# 1. Configuracao inicial da pagina
st.set_page_config(
    page_title="Dashboard de Vendas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Estilo CSS Customizado 
# CORREÇÃO: Aplicando Midnight Blue na Sidebar e forçando cores #3F3FD4
st.markdown("""
    <style>
        /* Fundo principal fixo */
        .stApp {
            background-color: #191970;
        }

        /* Fundo da Sidebar (Lateral) fixo na mesma cor do fundo */
        [data-testid="stSidebar"] {
            background-color: #191970 !important;
            border-right: 1px solid #3F3FD4; /* Linha sutil para separar do conteúdo */
        }

        /* Forçar cor dos headers e textos comuns em toda a aplicação */
        h1, h2, h3, span, p, label, .stMetric div {
            color: #3F3FD4 !important;
        }

        /* Ajuste específico para os itens de navegação na sidebar */
        [data-testid="stSidebarNav"] span {
            color: #3F3FD4 !important;
        }

        /* Ajuste nos cards de métricas para visibilidade */
        [data-testid="stMetricValue"] {
            color: #3F3FD4 !important;
        }
        
        /* Cor dos ícones na sidebar */
        [data-testid="stSidebar"] div[role="img"] {
            filter: sepia(100%) saturate(300%) hue-rotate(200deg); /* Ajuste para azul */
        }
    </style>
""", unsafe_allow_html=True)

# 3. Definindo as páginas 
visao_geral = st.Page("pages/visao_geral.py", 
                      title='Visão Geral',
                      icon='🏠',
                      default=True
                    )
analise_vendas = st.Page("pages/analise_vendas.py",
                         title='Análise de Vendas',
                         icon='💰')
analise_produtos = st.Page("pages/analise_produtos.py",
                            title='Produtos',
                            icon='📦')
# analise_produtos_professor = st.Page("pages/analise_produtos_professor.py",
                 # title='Produtos - Professor',
                 # icon='🧑🏽‍🏫')
mapa_vendas = st.Page("pages/mapa_vendas.py",
                 title='Mapa de Vendas',
                 icon='📍')
sobre = st.Page("pages/sobre.py",
                 title='Sobre',
                 icon='ℹ️')


# 4. Navegação Estruturada por Seções
pg = st.navigation({
    "Principal": [visao_geral],
    "Análises": [analise_vendas, analise_produtos, mapa_vendas],
    "Sobre": [sobre]
})

# 5. Sidebar - Elementos Fixos
with st.sidebar:
    st.markdown("### 🛠️ Configurações Globais")
    st.info("Filtros aplicados em todas as páginas.")

# 6. Execução do app
pg.run()

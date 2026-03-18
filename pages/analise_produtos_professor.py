import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================
st.set_page_config(layout="wide")
st.title("📦 Análise de Produtos - Professor")

# =========================
# ESTILO
# =========================
st.markdown("""
    <style>
        .stApp {
            background-color: #191970;
        }
        h1, h2, h3, h4, h5, h6, span, p, label {
            color: #FFFFFF !important;
        }
        [data-testid="stMetricValue"] {
            color: #FFFFFF !important;
        }
    </style>
""", unsafe_allow_html=True)

# =========================
# FUNÇÃO PARA CARREGAR DADOS
# =========================
@st.cache_data
def dados_vendas():
    df = pd.read_csv('dados/vendas.csv')
    df.columns = df.columns.str.strip()
    df['Data'] = pd.to_datetime(df['Data'])
    df['Receita'] = df['Vendas']
    df['Preco_Unitario'] = df['Vendas'] / df['Quantidade']
    return df

# =========================
# FUNÇÃO PARA FORMATAÇÃO DE MOEDA
# =========================
def formatar_real(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# =========================
# EXECUÇÃO
# =========================
df = dados_vendas()

# Filtro de produto
produto = st.selectbox("Selecione um produto", df['Produto'].unique())
dados_filtrados = df[df['Produto'] == produto]

# =========================
# KPIs
# =========================
receita_total = dados_filtrados['Receita'].sum()
lucro_total = dados_filtrados['Lucro'].sum()
qtd_vendida = dados_filtrados['Quantidade'].sum()
preco_medio = dados_filtrados['Preco_Unitario'].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Receita", formatar_real(receita_total))
col2.metric("Lucro", formatar_real(lucro_total))
col3.metric("Qtd. Vendida", f"{qtd_vendida:,.0f}".replace(",", "."))
col4.metric("Preço Médio", formatar_real(preco_medio))

st.markdown("---")

# =========================
# GRÁFICOS
# =========================
st.subheader(f"📈 Evolução de Vendas - {produto}")
fig1 = px.line(
    dados_filtrados.sort_values('Data'),
    x='Data',
    y='Receita',
    markers=True
)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("🌎 Vendas por Região")
fig2 = px.bar(dados_filtrados, x='Região', y='Receita', color='Região')
st.plotly_chart(fig2, use_container_width=True)

# =========================
# PERFORMANCE VENDEDOR - SOLUÇÃO 3
# =========================
st.subheader("👨‍💼 Lucro por Vendedor")

# Criar colunas lado a lado: tabela e gráfico
col_tab, col_graf = st.columns(2)

with col_tab:
    st.markdown("#### 📋 Tabela de Lucro por Vendedor")
    tabela_vendedor = dados_filtrados.groupby("Vendedor").agg(
        Receita=("Receita", "sum"),
        Lucro=("Lucro", "sum"),
        Quantidade=("Quantidade", "sum"),
        Preço_Médio=("Preco_Unitario", "mean")
    ).round(2).sort_values(by="Receita", ascending=False)
    st.dataframe(tabela_vendedor, use_container_width=True, height=400)  # altura fixa

with col_graf:
    fig3 = px.bar(
        tabela_vendedor.reset_index(),
        x="Vendedor",
        y="Lucro",
        color="Lucro",
        color_continuous_scale=px.colors.sequential.Blues
    )
    fig3.update_layout(
        height=400,  # mesma altura da tabela
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color="#FFFFFF"
    )
    st.plotly_chart(fig3, use_container_width=True)

# =========================
# DADOS DETALHADOS
# =========================
st.markdown("---")
st.subheader("📊 Dados Detalhados")
st.dataframe(dados_filtrados, use_container_width=True)


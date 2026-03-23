import streamlit as st
import pandas as pd
import plotly.express as px
import locale

# Função para formatar valores em reais
def format_brl(value):
    try:
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_ALL, 'pt_BR')
        except locale.Error:
            return f"R$ {value:,.2f}".replace('.', 'X').replace(',', '.').replace('X', ',')
    return locale.currency(value, symbol=True, grouping=True)

# Configuração de estilo
st.markdown("""
    <style>
        .stApp { background-color: #191970; }
        h1, h2, h3, h4, h5, h6, span, p, label, .stMetric div {
            color: #FFFFFF !important;
        }
        [data-testid="stMetricValue"] { color: #FFFFFF !important; }
    </style>
""", unsafe_allow_html=True)

st.title("Análise de Produtos")

# Carregar dados
df = pd.read_csv('dados/vendas.csv')

# Selectbox de produtos
produto_selecionado = st.selectbox(
    "Selecione um produto",
    df['Produto'].unique()
)

# Filtrar dados
df_filtrado = df[df['Produto'] == produto_selecionado]

# Métricas principais
receita = df_filtrado['Vendas'].sum()
lucro = df_filtrado['Lucro'].sum()
qtd_vendida = df_filtrado['Quantidade'].sum()
preco_medio = receita / qtd_vendida if qtd_vendida else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Receita", f"R$ {receita:,.2f}", border=True)
col2.metric("📈 Lucro", f"R$ {lucro:,.2f}", border=True)
col3.metric("📦 Qtd. Vendida", qtd_vendida, border=True)
col4.metric("📊 Preço Médio", format_brl(preco_medio), border=True)

# Gráficos de análise
colA, colB = st.columns(2)

# Vendas por região
df_regiao = df_filtrado.groupby('Região')['Vendas'].sum().reset_index()
fig_regiao = px.bar(df_regiao, x='Região', y='Vendas', color='Vendas',
                    title=f'🌎 Vendas por Região - {produto_selecionado}')
colA.plotly_chart(fig_regiao, use_container_width=True)

# Vendas por vendedor
df_vendedor = df_filtrado.groupby('Vendedor')['Vendas'].sum().reset_index()
fig_vendedor = px.pie(df_vendedor, names='Vendedor', values='Vendas',
                      title=f'{produto_selecionado} - Vendas por Vendedor')
colB.plotly_chart(fig_vendedor, use_container_width=True)

# Evolução temporal de vendas
df_filtrado['Data'] = pd.to_datetime(df_filtrado['Data'])
df_filtrado['Mês'] = df_filtrado['Data'].dt.to_period('M').astype(str)
df_mensal = df_filtrado.groupby('Mês')['Vendas'].sum().reset_index()
fig_evolucao = px.area(df_mensal, x='Mês', y='Vendas', title=f'📈 Evolução de Vendas - {produto_selecionado}')
st.plotly_chart(fig_evolucao, use_container_width=True)
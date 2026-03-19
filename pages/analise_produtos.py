import streamlit as st
import pandas as pd
import plotly.express as px
import locale

# Função para formatar valores em reais
 
def format_brl(value):
    # Set the locale to Brazilian Portuguese
    # On some systems, the locale string might be slightly different (e.g., 'pt_BR.UTF-8')
    try:
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    except locale.Error:
        # Fallback for systems where 'pt_BR.UTF-8' is not available
        try:
            locale.setlocale(locale.LC_ALL, 'pt_BR')
        except locale.Error:
            print("Warning: Could not set pt_BR locale. Falling back to simple formatting.")
            return f"R$ {value:,.2f}".replace('.', 'X').replace(',', '.').replace('X', ',')
 
    # Format the value as currency with grouping enabled
    # locale.currency() returns a string like 'R$ 1.234,56'
    formatted_value = locale.currency(value, symbol=True, grouping=True)
    return formatted_value
 
###################################################################################################


st.title("📦 Análise de Produtos")

st.markdown("""
    <style>
        .stApp {
            background-color: #191970;
        }
        h1, h2, h3, h4, h5, h6, span, p, label, .stMetric div {
            color: #FFFFFF !important;
        }
        [data-testid="stMetricValue"] {
            color: #FFFFFF !important;
        }
    </style>
""", unsafe_allow_html=True)

# Carregar dados
dados_vendas = pd.read_csv('dados/vendas.csv')

# Selectbox
option = st.selectbox(
    "Selecione um produto",
    ("Headphone", "Headset", "Memoria RAM", "Mouse", "SSD", "Teclado", "Webcam")
)

# Filtrar dados
dados_filtrados = dados_vendas[dados_vendas['Produto'] == option]

# Colunas
col1, col2, col3, col4 = st.columns(4)

with col1:
    receita = dados_filtrados['Vendas'].sum()
    st.metric(label="Receita", value=f"R$ {receita:,.2f}", border=True)
with col2:
    lucro = dados_filtrados['Lucro'].sum()
    st.metric(label="Lucro", value=f"R$ {lucro:,.2f}", border=True)

with col3:
    qtd = dados_filtrados['Quantidade'].sum()
    st.metric(label="Qtd. Vendida", value=qtd, border=True)

with col4:
    preco_medio = receita / qtd 
    st.metric(label="Preço Médio", value=format_brl(preco_medio), border=True)

colA, colB = st.columns(2)

with colA:
    df_agrupado = dados_filtrados.groupby('Região')['Vendas'].sum().reset_index()
    
    fig1 = px.bar(
        df_agrupado, 
        x='Região', 
        y='Vendas', 
        title=f'🌎 Vendas por Região - {option}', 
        color='Vendas'
    )
    st.plotly_chart(fig1, use_container_width=True)

with colB:
    df_agrupado2 = dados_filtrados.groupby('Vendedor')['Vendas'].sum().reset_index()

    fig2 = px.pie(
        df_agrupado2,
        names='Vendedor',
        values='Vendas',                                                                                                                                     
        title=f'👩🏽{option} - Vendas por vendedor'
    )
    st.plotly_chart(fig2, use_container_width=True)

# Criando a coluna mês para análise temporal
# Converter em data em hora/data (datetime)

dados_filtrados['Data'] = pd.to_datetime(dados_filtrados['Data'])
dados_filtrados['Mês'] = dados_filtrados['Data'].dt.to_period('M').astype(str)


# Debugando a coluna "Mês"
# st.dataframe(dados_filtrados.head(10))

df_agrupado3 = dados_filtrados.groupby('Mês')['Vendas'].sum().reset_index()

fig3 = px.area(
    df_agrupado3, 
    x='Mês', 
    y='Vendas', 
    title=f'📈 Evolução de Vendas - {option}'
)
st.plotly_chart(fig3, use_container_width=True)

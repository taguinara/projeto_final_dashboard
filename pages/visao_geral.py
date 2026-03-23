import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Estilo CSS para manter o fundo Midnight Blue
st.markdown("""
    <style>
        .stApp {
            background-color: #191970;
        }
        h1, h2, h3, span, p, label, .stMetric div {
            color: #FFFFFF !important;
        }
        [data-testid="stMetricValue"] {
            color: #FFFFFF !important;
        }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def carregar_dados():
    df = pd.read_csv('dados/vendas.csv')
    df['Data'] = pd.to_datetime(df['Data'])
    return df

dados_vendas = carregar_dados()

st.title("Visão Geral do Negócio")

# Função para formatação brasileira (R$ 1.234,56)
def formatar_real(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- CÁLCULO DE MÉTRICAS E DELTAS (Exemplo comparativo) ---
# Aqui simulamos uma variação de 10% para demonstrar a seta verde/vermelha
receita_atual = dados_vendas['Vendas'].sum()
receita_anterior = receita_atual * 0.90 # Simulação: 10% menor que a atual

lucro_atual = dados_vendas['Lucro'].sum()
lucro_anterior = lucro_atual * 1.10 # Simulação: 10% maior que a atual (gerará seta vermelha)

transacoes_atual = len(dados_vendas)
ticket_medio_atual = dados_vendas['Vendas'].mean()

# Layout de Colunas
col1, col2, col3, col4 = st.columns(4)

# Coluna 1: Receita Total (Seta Verde - Aumento)
col1.metric(
    label="💰 Receita Total", 
    value=formatar_real(receita_atual),
    delta_color="normal",
    border=True
)

# Coluna 2: Lucro Total (Seta Vermelha - Queda simulada)
col2.metric(
    label="📈 Lucro Total", 
    value=formatar_real(lucro_atual),
    delta_color="normal",
    border=True
)

# Coluna 3: Transações (Seta Verde)
col3.metric(
    label="🛒 Transações", 
    value=f"{transacoes_atual}",
    delta_color="normal",
    border=True
)

# Coluna 4: Ticket Médio (Seta Verde)
col4.metric(
    label="📊 Ticket Médio", 
    value=formatar_real(ticket_medio_atual),
    delta_color="normal",
    border=True
)

st.divider()

# --- Restante dos Gráficos ---
colA, colB = st.columns(2)

with colA:
    vendas_regiao = dados_vendas.groupby('Região')['Vendas'].sum().reset_index()
    fig_pizza = px.pie(vendas_regiao, names='Região', values='Vendas',
                        title='Vendas por Região', hole=0.4,
                        color_discrete_sequence=px.colors.sequential.Blues_r)
    fig_pizza.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#3F3FD4")
    st.plotly_chart(fig_pizza, use_container_width=True)

with colB:
    dados_vendas['Mês'] = dados_vendas['Data'].dt.to_period('M').astype(str)
    vendas_mensal = dados_vendas.groupby('Mês')['Vendas'].sum().reset_index()
    fig_linha = px.line(vendas_mensal, x='Mês', y='Vendas', title='Evolução Mensal', markers=True)
    fig_linha.update_traces(line_color='#3F3FD4')
    fig_linha.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#3F3FD4")
    st.plotly_chart(fig_linha, use_container_width=True)

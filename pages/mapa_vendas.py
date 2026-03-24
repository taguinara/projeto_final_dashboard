import streamlit as st
import pandas as pd
import locale

# ---------- Estilo ----------
st.set_page_config(layout="wide") # Melhor visualização para tabelas e mapas
st.markdown("""
    <style>
        .stApp { background-color: #191970; }
        h1, h2, h3, h4, h5, h6, span, p, label, .stMetric div { color: #FFFFFF !important; }
        [data-testid="stMetricValue"] { color: #FFFFFF !important; }
        .stDataFrame { background-color: rgba(255, 255, 255, 0.1); border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("📍 Mapa de Vendas por Localização")
st.write("Visualize a distribuição das vendas e aplique filtros para explorar os dados.")

# ---------- Carregar dados ----------
@st.cache_data # Cache para performance
def carregar_dados():
    df = pd.read_csv("dados/vendas_geolocalizacao.csv")
    df.columns = df.columns.str.lower()
    df["data"] = pd.to_datetime(df["data"])
    return df

df = carregar_dados()

# ---------- Função de formatação ----------
def formatar_real(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ---------- Verificar colunas ----------
colunas_necessarias = ["região", "categoria", "produto", "vendedor", "data", "vendas", "lucro", "cidade"]
for col in colunas_necessarias:
    if col not in df.columns:
        st.error(f"Coluna '{col}' não encontrada no dataset.")
        st.stop()

# ---------- Sidebar - Filtros ----------
st.sidebar.header("Filtros do Mapa")
regiao = st.sidebar.selectbox("Região", ["Todas"] + sorted(df["região"].dropna().unique()))
categoria = st.sidebar.selectbox("Categoria", ["Todas"] + sorted(df["categoria"].dropna().unique()))
produto = st.sidebar.selectbox("Produto", ["Todos"] + sorted(df["produto"].dropna().unique()))
vendedor = st.sidebar.selectbox("Vendedor", ["Todos"] + sorted(df["vendedor"].dropna().unique()))

# Faixa de valor de vendas
min_venda, max_venda = float(df['vendas'].min()), float(df['vendas'].max())
faixa_venda = st.sidebar.slider("Faixa de Valor da Venda (R$)", min_venda, max_venda, (min_venda, max_venda))

# Intervalo de datas
data_min, data_max = df['data'].min().date(), df['data'].max().date()
data_range = st.sidebar.date_input("Selecione o Período", value=(data_min, data_max), min_value=data_min, max_value=data_max)

# ---------- Filtrar dataframe ----------
df_filtrado = df.copy()

if regiao != "Todas":
    df_filtrado = df_filtrado[df_filtrado["região"] == regiao]
if categoria != "Todas":
    df_filtrado = df_filtrado[df_filtrado["categoria"] == categoria]
if produto != "Todos":
    df_filtrado = df_filtrado[df_filtrado["produto"] == produto]
if vendedor != "Todos":
    df_filtrado = df_filtrado[df_filtrado["vendedor"] == vendedor]

df_filtrado = df_filtrado[(df_filtrado["vendas"] >= faixa_venda[0]) & (df_filtrado["vendas"] <= faixa_venda[1])]

# Tratamento para evitar erro caso o usuário selecione apenas uma data ou limpe o campo
if isinstance(data_range, tuple) and len(data_range) == 2:
    df_filtrado = df_filtrado[(df_filtrado["data"].dt.date >= data_range[0]) & (df_filtrado["data"].dt.date <= data_range[1])]

# ---------- Métricas ----------
qtd_pontos = df_filtrado.shape[0]
qtd_cidades = df_filtrado['cidade'].nunique()
total_vendas = df_filtrado['vendas'].sum()
total_lucro = df_filtrado['lucro'].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("📍 Pontos de Venda", qtd_pontos)
col2.metric("📍 Cidades", qtd_cidades)
col3.metric("💰 Vendas Totais", formatar_real(total_vendas))
col4.metric("💰 Lucro Total", formatar_real(total_lucro))

# ---------- Mapa ----------
st.subheader("Mapa de Vendas")
lat_col = next((c for c in df_filtrado.columns if 'lat' in c), None)
lon_col = next((c for c in df_filtrado.columns if 'lon' in c or 'lng' in c), None)

if lat_col and lon_col:
    # Mostra os pontos no mapa
    st.map(df_filtrado[[lat_col, lon_col]])
else:
    st.warning("⚠️ Colunas de latitude e longitude não encontradas.")

# ---------- Tabela de Resumo por Cidade  ----------
st.subheader("Resumo por Cidade")

# Agrupando os dados por cidade e calculando as métricas
df_resumo_cidade = df_filtrado.groupby("cidade").agg({
    "vendas": "sum",
    "lucro": "sum",
    "produto": "count" # Quantidade de vendas realizadas
}).rename(columns={"produto": "Qtd Vendas"}).reset_index()

# Ordenando pelas cidades com mais vendas
df_resumo_cidade = df_resumo_cidade.sort_values(by="vendas", ascending=False)

# Exibindo a tabela formatada
st.dataframe(
    df_resumo_cidade,
    column_config={
        "cidade": "Cidade",
        "vendas": st.column_config.NumberColumn("Total Vendas", format="R$ %.2f"),
        "lucro": st.column_config.NumberColumn("Total Lucro", format="R$ %.2f"),
        "Qtd Vendas": "Nº de Transações"
    },
    hide_index=True,
    use_container_width=True
)
"""
gerar_dados_geolocalizacao.py
------------------------------
Gera um arquivo CSV com dados de geolocalização vinculados aos produtos
e regiões presentes em dados/vendas.csv.

Saída: dados/vendas_geolocalizacao.csv
"""

import pandas as pd
import numpy as np

np.random.seed(42)

# ---------------------------------------------------------------------------
# 1. Cidades reais por região com suas coordenadas (lat, lon)
# ---------------------------------------------------------------------------
CIDADES_POR_REGIAO = {
    "Norte": [
        ("Manaus",          -3.1190,  -60.0217),
        ("Belém",           -1.4558,  -48.4902),
        ("Porto Velho",     -8.7612,  -63.9004),
        ("Macapá",           0.0349,  -51.0694),
        ("Boa Vista",        2.8235,  -60.6758),
        ("Rio Branco",      -9.9754,  -67.8249),
        ("Palmas",         -10.2491,  -48.3243),
    ],
    "Nordeste": [
        ("Salvador",       -12.9714,  -38.5014),
        ("Fortaleza",       -3.7172,  -38.5433),
        ("Recife",          -8.0476,  -34.8770),
        ("Maceió",          -9.6658,  -35.7350),
        ("Natal",           -5.7945,  -35.2110),
        ("Teresina",        -5.0892,  -42.8019),
        ("São Luís",        -2.5307,  -44.3068),
        ("João Pessoa",     -7.1195,  -34.8450),
        ("Aracaju",        -10.9472,  -37.0731),
    ],
    "Centro-Oeste": [
        ("Brasília",       -15.7801,  -47.9292),
        ("Goiânia",        -16.6864,  -49.2643),
        ("Cuiabá",         -15.6010,  -56.0974),
        ("Campo Grande",   -20.4697,  -54.6201),
        ("Anápolis",       -16.3281,  -48.9530),
        ("Rondonópolis",   -16.4727,  -54.6364),
    ],
    "Sudeste": [
        ("São Paulo",      -23.5505,  -46.6333),
        ("Rio de Janeiro", -22.9068,  -43.1729),
        ("Belo Horizonte", -19.9167,  -43.9345),
        ("Campinas",       -22.9099,  -47.0626),
        ("Vitória",        -20.3155,  -40.3128),
        ("Uberlândia",     -18.9186,  -48.2772),
        ("Ribeirão Preto", -21.1775,  -47.8103),
        ("Niterói",        -22.8833,  -43.1036),
    ],
    "Sul": [
        ("Curitiba",       -25.4284,  -49.2733),
        ("Porto Alegre",   -30.0346,  -51.2177),
        ("Florianópolis",  -27.5954,  -48.5480),
        ("Joinville",      -26.3045,  -48.8487),
        ("Caxias do Sul",  -29.1678,  -51.1794),
        ("Londrina",       -23.3045,  -51.1696),
        ("Maringá",        -23.4205,  -51.9333),
        ("Blumenau",       -26.9194,  -49.0661),
    ],
}

# Ruído máximo em graus para simular pontos dentro de cada cidade (~5 km)
NOISE_DEG = 0.05

# ---------------------------------------------------------------------------
# 2. Lê o arquivo de vendas
# ---------------------------------------------------------------------------
VENDAS_PATH = "./dados/vendas.csv"
SAIDA_PATH  = "./dados/vendas_geolocalizacao.csv"

df_vendas = pd.read_csv(VENDAS_PATH)

print(f"Registros carregados de '{VENDAS_PATH}': {len(df_vendas)}")
print(f"Regiões encontradas : {sorted(df_vendas['Região'].unique())}")
print(f"Produtos encontrados: {sorted(df_vendas['Produto'].unique())}\n")

# ---------------------------------------------------------------------------
# 3. Funções auxiliares
# ---------------------------------------------------------------------------

def sortear_cidade(regiao: str, rng: np.random.Generator) -> tuple:
    """Retorna (cidade, lat, lon) aleatorios para a região dada."""
    opcoes = CIDADES_POR_REGIAO.get(regiao)
    if opcoes is None:
        return ("Desconhecida", np.nan, np.nan)
    idx = rng.integers(0, len(opcoes))
    return opcoes[idx]


def adicionar_ruido(valor: float, rng: np.random.Generator) -> float:
    """Adiciona pequeno ruído para simular endereços distintos na cidade."""
    return round(valor + rng.uniform(-NOISE_DEG, NOISE_DEG), 6)


# ---------------------------------------------------------------------------
# 4. Gera as colunas de geolocalização
# ---------------------------------------------------------------------------
rng = np.random.default_rng(42)

cidades  = []
lats     = []
lons     = []

for _, row in df_vendas.iterrows():
    cidade, lat, lon = sortear_cidade(row["Região"], rng)
    cidades.append(cidade)
    lats.append(adicionar_ruido(lat, rng))
    lons.append(adicionar_ruido(lon, rng))

df_vendas["Cidade"]    = cidades
df_vendas["Latitude"]  = lats
df_vendas["Longitude"] = lons

# ---------------------------------------------------------------------------
# 5. Cria também um resumo agregado por Produto + Região + Cidade
# ---------------------------------------------------------------------------
df_resumo = (
    df_vendas
    .groupby(["Produto", "Região", "Cidade"], as_index=False)
    .agg(
        Total_Vendas    = ("Vendas",     "sum"),
        Total_Quantidade= ("Quantidade", "sum"),
        Total_Lucro     = ("Lucro",      "sum"),
        Num_Transacoes  = ("Vendas",     "count"),
        Latitude        = ("Latitude",   "mean"),   # centróide da cidade
        Longitude       = ("Longitude",  "mean"),
    )
    .round({"Total_Vendas": 2, "Total_Lucro": 2,
            "Latitude": 6, "Longitude": 6})
    .sort_values(["Região", "Produto", "Cidade"])
    .reset_index(drop=True)
)

# ---------------------------------------------------------------------------
# 6. Salva os arquivos
# ---------------------------------------------------------------------------
df_vendas.to_csv(SAIDA_PATH, index=False)
print(f"Arquivo principal salvo em '{SAIDA_PATH}' ({len(df_vendas)} linhas)")

RESUMO_PATH = "./dados/vendas_geo_resumo.csv"
df_resumo.to_csv(RESUMO_PATH, index=False)
print(f"Resumo agregado  salvo em '{RESUMO_PATH}' ({len(df_resumo)} linhas)\n")

# ---------------------------------------------------------------------------
# 7. Preview
# ---------------------------------------------------------------------------
print("=== Primeiras linhas do arquivo principal ===")
print(df_vendas[["Data","Produto","Região","Cidade","Latitude","Longitude",
                  "Vendas","Lucro"]].head(10).to_string(index=False))

print("\n=== Primeiras linhas do resumo por Produto/Região/Cidade ===")
print(df_resumo.head(10).to_string(index=False))

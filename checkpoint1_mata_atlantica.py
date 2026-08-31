"""
CHECKPOINT 1 - EXERCÍCIO INTEGRADOR DE ANÁLISE DE DADOS

Integrante: Joseh gabriel RM553094

Tema: Características funcionais de árvores e plantas arbóreas da Mata Atlântica
Fonte original: Rodrigues et al. (2018), Zenodo DOI 10.5281/zenodo.1241023

Observação:
O arquivo CSV desta atividade é um recorte de 51 espécies do arquivo
species-level_trait.csv disponibilizado.

Bibliotecas utilizadas: Python, NumPy, Pandas, Matplotlib e Seaborn.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 180)
sns.set_theme(style="whitegrid")

PASTA = Path(__file__).resolve().parent
ARQUIVO = PASTA / "mata_atlantica_arvores.csv"
PASTA_GRAFICOS = PASTA / "graficos"
PASTA_GRAFICOS.mkdir(exist_ok=True)

print("=" * 90)
print("CHECKPOINT 1 - ANÁLISE DE DADOS")
print("=" * 90)

# 1. CARREGAR E APRESENTAR OS DADOS
df = pd.read_csv(ARQUIVO)

print("\n1) PRIMEIRAS LINHAS DA BASE")
print(df.head(10))
print(f"\nDimensão da base: {df.shape[0]} linhas x {df.shape[1]} colunas")

# 2. INFORMAÇÕES GERAIS, TIPOS E ESTATÍSTICAS
print("\n2) INFORMAÇÕES GERAIS")
df.info()

print("\nTipos das colunas:")
print(df.dtypes)

print("\nEstatísticas descritivas:")
print(df.describe().round(3))

# 3. DIAGNÓSTICO DE QUALIDADE
print("\n3) DIAGNÓSTICO DE QUALIDADE DOS DADOS")

print("\nValores ausentes por coluna:")
print(df.isna().sum())

print(f"\nLinhas duplicadas: {df.duplicated().sum()}")

colunas_numericas = [col for col in df.columns if col != "Species"]

print("\nValores negativos nas variáveis numéricas:")
print((df[colunas_numericas] < 0).sum())

print("\nClasses de dispersão encontradas:")
print(sorted(df["DS_anemo-0_zoo-1"].dropna().unique()))

def contar_outliers_iqr(serie):
    q1 = serie.quantile(0.25)
    q3 = serie.quantile(0.75)
    iqr = q3 - q1
    limite_inferior = q1 - 1.5 * iqr
    limite_superior = q3 + 1.5 * iqr
    return int(((serie < limite_inferior) | (serie > limite_superior)).sum())

outliers = pd.Series(
    {col: contar_outliers_iqr(df[col]) for col in colunas_numericas},
    name="quantidade_outliers"
).sort_values(ascending=False)

print("\nPossíveis outliers pelo método IQR:")
print(outliers)

# 4. LIMPEZA E PRÉ-PROCESSAMENTO
print("\n4) LIMPEZA E PRÉ-PROCESSAMENTO")

for coluna in colunas_numericas:
    df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

# Rótulos mais legíveis para o tipo de dispersão.
mapa_dispersao = {
    0: "Anemocoria",
    1: "Zoocoria"
}
df["dispersao"] = df["DS_anemo-0_zoo-1"].map(mapa_dispersao)

# Imputação por mediana somente nas variáveis numéricas com dados ausentes.
# A mediana é robusta a valores extremos e evita excluir espécies inteiras.
df_processado = df.copy()

for coluna in colunas_numericas:
    if df_processado[coluna].isna().any():
        df_processado[coluna] = df_processado[coluna].fillna(
            df_processado[coluna].median()
        )

# Padronização z-score das variáveis numéricas para comparação entre escalas.
X = df_processado[colunas_numericas].to_numpy(dtype=float)
medias = np.mean(X, axis=0)
desvios = np.std(X, axis=0, ddof=0)
X_padronizado = (X - medias) / desvios

df_padronizado = pd.DataFrame(
    X_padronizado,
    columns=[f"{col}_z" for col in colunas_numericas]
)

print("\nPré-processamento concluído:")
print("- Tipos numéricos conferidos.")
print("- Valores ausentes preenchidos pela mediana da respectiva variável.")
print("- Variável de dispersão convertida para Anemocoria/Zoocoria.")
print("- Possíveis outliers identificados, mas não removidos automaticamente.")
print("- Variáveis numéricas padronizadas com z-score.")
print(f"- Valores ausentes após a imputação: {df_processado.isna().sum().sum()}")

# QUESTÃO 1
print("\n" + "=" * 90)
print("QUESTÃO 1 - ANÁLISE DAS PRINCIPAIS VARIÁVEIS")
print("=" * 90)

print("\nQuantidade de espécies por síndrome de dispersão:")
print(df_processado["dispersao"].value_counts())

variaveis_principais = [
    "SLA_cm2/g",
    "LDMC_mg/g",
    "SSD_g/cm3",
    "Hpot95_m",
    "SeedMass_g"
]

print("\nResumo das principais variáveis:")
print(df_processado[variaveis_principais].describe().round(3))

# Gráfico 1 - distribuição da altura potencial
plt.figure(figsize=(9, 6))
plt.hist(df_processado["Hpot95_m"], bins=12)
plt.title("Distribuição da altura potencial")
plt.xlabel("Altura potencial (m)")
plt.ylabel("Frequência")
plt.tight_layout()
plt.savefig(PASTA_GRAFICOS / "01_distribuicao_altura_potencial.png", dpi=150)
plt.close()

# Gráfico 2 - densidade da madeira por síndrome de dispersão
plt.figure(figsize=(9, 6))
sns.boxplot(data=df_processado, x="dispersao", y="SSD_g/cm3")
plt.title("Densidade do caule por síndrome de dispersão")
plt.xlabel("Síndrome de dispersão")
plt.ylabel("Densidade específica do caule (g/cm³)")
plt.tight_layout()
plt.savefig(PASTA_GRAFICOS / "02_boxplot_densidade_dispersao.png", dpi=150)
plt.close()

# Gráfico 3 - SLA x LDMC
plt.figure(figsize=(9, 6))
sns.scatterplot(
    data=df_processado,
    x="SLA_cm2/g",
    y="LDMC_mg/g",
    hue="dispersao"
)
plt.title("Relação entre SLA e LDMC")
plt.xlabel("SLA (cm²/g)")
plt.ylabel("LDMC (mg/g)")
plt.tight_layout()
plt.savefig(PASTA_GRAFICOS / "03_sla_x_ldmc.png", dpi=150)
plt.close()

# QUESTÃO 2
print("\n" + "=" * 90)
print("QUESTÃO 2 - CORRELAÇÃO ENTRE AS VARIÁVEIS")
print("=" * 90)

correlacao = df_processado[colunas_numericas].corr()

matriz_abs = np.array(correlacao.abs(), dtype=float, copy=True)
np.fill_diagonal(matriz_abs, np.nan)

posicao = np.unravel_index(
    np.nanargmax(matriz_abs),
    matriz_abs.shape
)

var_1 = correlacao.index[posicao[0]]
var_2 = correlacao.columns[posicao[1]]
valor_correlacao = correlacao.loc[var_1, var_2]

print("\nMatriz de correlação:")
print(correlacao.round(3))

print(
    f"\nMaior correlação absoluta: {var_1} x {var_2} = "
    f"{valor_correlacao:.3f}"
)

plt.figure(figsize=(12, 9))
sns.heatmap(correlacao, annot=False)
plt.title("Correlação entre as características das espécies")
plt.tight_layout()
plt.savefig(PASTA_GRAFICOS / "04_heatmap_correlacoes.png", dpi=150)
plt.close()

# QUESTÃO 3
print("\n" + "=" * 90)
print("QUESTÃO 3 - O QUE PODEMOS OBSERVAR NOS DADOS")
print("=" * 90)

classe_media = df_processado.groupby("dispersao")[variaveis_principais].mean()

especie_maior_altura = df_processado.loc[
    df_processado["Hpot95_m"].idxmax(), ["Species", "Hpot95_m"]
]

especie_maior_semente = df_processado.loc[
    df_processado["SeedMass_g"].idxmax(), ["Species", "SeedMass_g"]
]

especie_maior_densidade = df_processado.loc[
    df_processado["SSD_g/cm3"].idxmax(), ["Species", "SSD_g/cm3"]
]

print(
    f"1. A maior altura potencial da amostra pertence a "
    f"{especie_maior_altura['Species']} ({especie_maior_altura['Hpot95_m']:.2f} m)."
)

print(
    f"2. A maior massa de semente observada pertence a "
    f"{especie_maior_semente['Species']} ({especie_maior_semente['SeedMass_g']:.4f} g)."
)

print(
    f"3. A maior densidade específica do caule pertence a "
    f"{especie_maior_densidade['Species']} "
    f"({especie_maior_densidade['SSD_g/cm3']:.3f} g/cm³)."
)

print(
    f"4. A correlação mais forte foi entre {var_1} e {var_2} "
    f"({valor_correlacao:.3f}), mostrando uma relação inversa muito forte "
    f"entre essas duas características."
)

print("\nMédias por síndrome de dispersão:")
print(classe_media.round(3))

# QUESTÃO 4
print("\n" + "=" * 90)
print("QUESTÃO 4 - TRATAMENTO DOS DADOS")
print("=" * 90)

print("""
A base apresenta valores ausentes em algumas características funcionais.
Em vez de excluir as espécies que possuem algum valor ausente, foi aplicada
imputação pela mediana de cada variável numérica. Essa escolha reduz a perda
de observações e é relativamente robusta à presença de valores extremos.

Também foram realizados:
- conferência e conversão dos tipos numéricos;
- transformação do código de dispersão em rótulos legíveis;
- identificação de possíveis outliers pelo método IQR;
- padronização por z-score para permitir comparação entre variáveis com escalas
  muito diferentes.

Os outliers não foram removidos automaticamente, pois uma espécie com uma
característica extrema pode representar uma condição biológica real e não um erro.
A base original também foi preservada, enquanto a versão processada é usada
para as análises comparativas.
""")

# CONCLUSÃO
print("=" * 90)
print("CONCLUSÃO")
print("=" * 90)


print(
    "Os dados mostram diferenças consideráveis entre as espécies analisadas. "
    "A altura, a densidade do caule, as características das folhas e a massa "
    "das sementes variam bastante entre as espécies. A correlação também ajudou "
    "a perceber algumas relações entre as características. Antes das análises, "
    "foi necessário tratar os valores que estavam faltando e organizar as variáveis."
)


print(f"\nOs 4 gráficos foram salvos em: {PASTA_GRAFICOS}")
print("Análise concluída com sucesso.")

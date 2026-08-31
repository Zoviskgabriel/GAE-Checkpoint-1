# Checkpoint 1 – Análise de Dados

## Tema

Características de árvores e outras plantas da Mata Atlântica.

## Base de dados

Para este trabalho foi usada uma base real com informações sobre características
funcionais de espécies da Floresta Atlântica subtropical brasileira.

A base original foi publicada por Rodrigues et al. e está disponível no Zenodo.
Neste trabalho foi usado um recorte com 51 espécies. Os valores não foram
inventados ou gerados artificialmente.

Fonte:
- Zenodo: https://zenodo.org/records/1241023
- DOI: https://doi.org/10.5281/zenodo.1241023

## O que tem na base

A tabela possui informações sobre folhas, caule, vasos, estômatos, altura,
sementes e dispersão das espécies.

Algumas das variáveis usadas na análise são:

- `SLA_cm2/g`: área foliar específica;
- `LDMC_mg/g`: matéria seca da folha;
- `Chlorophyll_FCI`: clorofila;
- `LeafTough_N/mm`: resistência da folha;
- `LeafThick_mm`: espessura da folha;
- `SSD_g/cm3`: densidade específica do caule;
- `XylProp_%`: proporção de xilema;
- `BarkProp_%`: proporção de casca;
- `VesselDens_n/mm2`: densidade dos vasos;
- `VesselDiam_microm`: diâmetro dos vasos;
- `Hpot95_m`: altura potencial;
- `SeedMass_g`: massa da semente;
- `DS_anemo-0_zoo-1`: tipo de dispersão.

## Análise feita

Primeiro a base é carregada com Pandas e são mostradas as primeiras linhas,
o tamanho da tabela e os tipos das colunas.

Depois são verificadas algumas coisas que poderiam atrapalhar a análise:
valores vazios, linhas repetidas, valores negativos e possíveis outliers.

Os valores que estavam faltando foram preenchidos usando a mediana da própria
coluna. A escolha foi feita porque a mediana é menos afetada por valores muito
altos ou muito baixos.

Os possíveis outliers foram apenas identificados. Eles não foram retirados,
pois podem representar características reais de determinadas espécies.

Também foi feita a padronização das variáveis numéricas usando z-score.

## Questão 1 – Análise das principais variáveis

Foram analisadas principalmente:

- SLA;
- LDMC;
- densidade específica do caule;
- altura potencial;
- massa das sementes.

Também foram feitos três gráficos para ajudar na interpretação:

1. distribuição da altura potencial;
2. densidade do caule comparando os tipos de dispersão;
3. relação entre SLA e LDMC.

## Questão 2 – Correlação

Foi calculada uma matriz de correlação entre as variáveis numéricas.

A maior correlação encontrada foi entre a proporção de medula e a proporção
de xilema, com valor de aproximadamente **-0,948**.

Foi feito um heatmap para facilitar a visualização das correlações.

## Questão 3 – O que podemos observar

Alguns dos resultados que chamaram atenção foram:

- a maior altura potencial da amostra foi de **35,23 m**, para *Ficus adhatodifolia*;
- a maior massa de semente foi de **2,0303 g**, para *Andira fraxinifolia*;
- a maior densidade específica do caule foi de **0,766 g/cm³**, para *Calyptranthes tricona*;
- a amostra possui mais espécies com dispersão por animais (zoocoria) do que por vento (anemocoria).

Também foi possível comparar as médias das características entre os dois tipos
de dispersão.

## Questão 4 – Tratamento dos dados

A base tinha alguns valores faltantes. Em vez de excluir todas as linhas que
tinham algum dado faltando, foi usada a mediana de cada variável para completar
esses valores.

Além disso:

- os tipos das colunas foram conferidos;
- a variável de dispersão foi transformada em nomes mais fáceis de entender;
- os possíveis outliers foram identificados pelo método IQR;
- as variáveis foram padronizadas com z-score.

## Gráficos

O programa gera quatro gráficos automaticamente:

1. `01_distribuicao_altura_potencial.png`
2. `02_boxplot_densidade_dispersao.png`
3. `03_sla_x_ldmc.png`
4. `04_heatmap_correlacoes.png`

## Como executar

Instale as bibliotecas:

```bash
pip install pandas numpy matplotlib seaborn
```

Depois execute:

```bash
python checkpoint1_mata_atlantica.py
```

Os gráficos serão salvos na pasta `graficos`.

## Conclusão

A análise mostrou que as espécies da amostra apresentam diferenças grandes em
suas características. Algumas são mais altas, outras possuem maior densidade
do caule ou sementes maiores.

A análise de correlação foi útil para encontrar relações entre as variáveis,
enquanto o tratamento dos dados foi importante para conseguir trabalhar com
as colunas que possuíam valores faltantes.

No geral, a base mostrou ser interessante para analisar como diferentes
características das plantas podem variar entre espécies da Mata Atlântica.

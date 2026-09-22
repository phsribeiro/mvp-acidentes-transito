# MVP - Acidentes de Transito

## Objetivo

Analisar acidentes de transito para identificar quando e onde as ocorrencias se concentram e quais fatores aparecem associados a maior gravidade.

## Perguntas de negocio

1. Quais dias e horarios concentram mais acidentes?
2. Quais regioes apresentam mais ocorrencias?
3. Quais fatores estao associados aos acidentes mais graves?
4. Como o perfil das ocorrencias varia ao longo do tempo?

## Fonte dos dados

O MVP utiliza uma amostra publica de 50.000 registros do conjunto **Motor Vehicle Collisions - Crashes**, disponibilizado pelo NYC Open Data por meio de uma API Socrata:

`https://data.cityofnewyork.us/resource/h9gi-nx95.csv`

A fonte e publica e sera usada para fins academicos. A coleta analisada foi realizada em 22/09/2026. A politica de uso e a referencia ao portal NYC Open Data devem acompanhar a entrega final.

## Pipeline implementado

1. Ingestao dos dados brutos.
2. Persistencia da camada bronze.
3. Conversao e limpeza de datas e horarios.
4. Tratamento de valores ausentes.
5. Criacao de indicadores de data, horario e gravidade.
6. Agregacoes por periodo e regiao.
7. Analise dos fatores contribuintes registrados para os veiculos.
8. Persistencia dos resultados na camada gold.

As tabelas Delta sao gerenciadas pelo Unity Catalog:

- `bronze_acidentes`: dados brutos validados.
- `silver_acidentes`: dados limpos e enriquecidos.
- `gold_acidentes_por_dia`: volume e gravidade media por dia da semana.
- `gold_acidentes_por_hora`: volume e gravidade media por hora.
- `gold_acidentes_por_regiao`: ocorrencias, feridos, mortos e gravidade por regiao.
- `gold_acidentes_por_ano`: evolucao anual das ocorrencias e da gravidade.
- `gold_acidentes_por_fator`: frequencia, feridos, mortos e gravidade media por fator contribuinte.

### Tratamentos realizados

- `crash_date` convertido para data a partir do formato ISO.
- `crash_time` convertido para horario, aceitando valores como `3:10`.
- Regioes ausentes substituidas por `NAO INFORMADA`.
- Feridos e mortos ausentes substituidos por zero.
- Indicador de gravidade calculado como `feridos + 10 * mortos`.
- Criacao das colunas `dia_semana`, `hora` e `ano`.
- Preservacao dos cinco campos de fator contribuinte para a analise final.

### Controles de qualidade

Na execucao validada foram processados 50.000 registros, com os seguintes resultados:

- datas nulas: 0;
- regioes nulas: 0;
- gravidades nulas: 0.

## Estrutura

```text
mvp-acidentes-transito/
├── README.md
├── notebooks/
│   ├── 01_ingestao_dados.py
│   ├── 02_limpeza_transformacao.ipynb
│   └── 03_analise_resultados.ipynb
├── resultados/
│   ├── acidentes_mais_graves.csv
│   ├── acidentes_por_ano.csv
│   ├── acidentes_por_dia.csv
│   ├── acidentes_por_fator.csv
│   ├── acidentes_por_hora.csv
│   └── acidentes_por_regiao.csv
└── docs/
```

## Ordem de execucao

Execute os notebooks nesta ordem no Databricks Free Edition:

1. `01_ingestao_dados.py`
2. `02_limpeza_transformacao.ipynb`
3. `03_analise_resultados.ipynb`

O notebook 01 cria `bronze_acidentes`, o notebook 02 cria `silver_acidentes` e o notebook 03 cria as tabelas gold.

## Resultados esperados

As tabelas gold foram exportadas para a pasta `resultados/`. Os principais resultados observados foram:

- **Dia com maior volume:** sexta-feira, com 7.643 acidentes. Domingo teve a maior gravidade media entre os dias, com 0,53.
- **Horario com maior volume:** 17h, com 3.319 acidentes. A maior gravidade media ocorreu as 22h, com 0,66.
- **Regiao com maior volume conhecido:** Brooklyn, com 11.438 acidentes. A maior gravidade media entre as regioes identificadas ocorreu em Staten Island, com 0,48.
- **Registros sem regiao:** 17.286 ocorrencias, equivalentes a 34,6% da amostra. Por isso, `NAO INFORMADA` nao deve ser interpretada como uma regiao real.
- **Ano com maior volume:** 2021, com 40.648 acidentes, aproximadamente 81,3% da amostra. Esse desequilibrio limita comparacoes entre anos.
- **Ocorrencia mais grave:** acidente de 22/05/2021, em regiao nao informada, com 3 mortos e gravidade 30 segundo o indicador criado.
- **Fator mais frequente:** `Driver Inattention/Distraction`, com 14.108 registros, 7.202 feridos e 14 mortos.
- **Maior gravidade media:** `Physical Disability`, com 1,74, mas baseada em apenas 19 registros.
- **Fator com maior total de mortes:** `Unsafe Speed`, com 38 mortes em 2.124 registros e gravidade media de 0,91.

Os fatores sao registrados em ate cinco colunas por acidente. Portanto, os totais de `acidentes_por_fator.csv` representam registros de fatores, e nao necessariamente acidentes unicos.

Os arquivos `acidentes_mais_graves.csv` e os demais CSVs devem ser consultados para a apresentacao completa dos resultados.

## Limitacoes

- A analise utiliza uma amostra de 50.000 registros.
- Os dados representam ocorrencias registradas em Nova York e nao devem ser generalizados para outras cidades.
- A amostra e fortemente concentrada em 2021, portanto a evolucao anual nao representa uma serie temporal equilibrada.
- Uma parcela relevante dos registros nao possui regiao informada.
- A analise de fatores pode contar mais de um fator para o mesmo acidente.
- Fatores com poucos registros podem apresentar gravidade media alta por efeito de amostra pequena.
- A formula de gravidade e um indicador criado para este MVP, nao uma classificacao oficial de severidade.
- Associacao entre variaveis nao implica causalidade.

## Ambiente

A execucao principal e feita no Databricks Free Edition com tabelas Delta gerenciadas pelo Unity Catalog. Nenhum token ou credencial deve ser salvo neste repositorio.

# Databricks notebook source
# MAGIC %md
# MAGIC # 01 - Ingestao dos acidentes de transito
# MAGIC
# MAGIC Este notebook baixa uma amostra publica de ocorrencias e valida a estrutura inicial dos dados.

# COMMAND ----------

import io
import requests
import pandas as pd

url = "https://data.cityofnewyork.us/resource/h9gi-nx95.csv?$limit=50000"
response = requests.get(url, timeout=60)
response.raise_for_status()

raw_pdf = pd.read_csv(io.BytesIO(response.content))
print(f"Linhas carregadas: {len(raw_pdf):,}")
print(f"Colunas carregadas: {len(raw_pdf.columns)}")

# COMMAND ----------

accidents_df = spark.createDataFrame(raw_pdf)

print(f"Linhas no Spark: {accidents_df.count():,}")
accidents_df.printSchema()

# COMMAND ----------

display(accidents_df.limit(10))

# COMMAND ----------

# Verificacao inicial de campos fundamentais para as perguntas de negocio.
required_columns = [
    "crash_date",
    "crash_time",
    "borough",
    "number_of_persons_injured",
    "number_of_persons_killed",
]

missing_columns = [column for column in required_columns if column not in accidents_df.columns]

if missing_columns:
    raise ValueError(f"Colunas obrigatorias ausentes: {missing_columns}")

print("Validacao inicial concluida com sucesso.")

# Persistencia da camada bruta em uma tabela gerenciada pelo Unity Catalog.
bronze_table = "bronze_acidentes"
accidents_df.write.mode("overwrite").format("delta").saveAsTable(bronze_table)
print(f"Dados brutos salvos na tabela: {bronze_table}")

# Databricks notebook source
# MAGIC %md ## Create Unity Catalog and Schemas

# COMMAND ----------

# Prod environment
PROD_CATALOG_NAME = "prod"
PROD_SCHEMA_NAME = "scoring"

# Dev environment
DEV_CATALOG_NAME = "dev"

# Scoring dataset
scoring_dataset = "/databricks-datasets/Rdatasets/data-001/csv/datasets/iris.csv"

# COMMAND ----------

# Prod
spark.sql(f"CREATE CATALOG IF NOT EXISTS {PROD_CATALOG_NAME}")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {PROD_CATALOG_NAME}.{PROD_SCHEMA_NAME}")

# Dev
spark.sql(f"CREATE CATALOG IF NOT EXISTS {DEV_CATALOG_NAME}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create scoring input tables

# COMMAND ----------

from pyspark.sql.types import *

df = spark.read.format("csv").option("header", "true").load(scoring_dataset)

df = df.withColumnRenamed("Sepal.Length", "sepal_length")
df = df.withColumnRenamed("Sepal.Width", "sepal_width")
df = df.withColumnRenamed("Petal.Length", "petal_length")
df = df.withColumnRenamed("Petal.Width", "petal_width")
df = df.drop("_c0", "Species")

df = df.withColumn("sepal_length", df["sepal_length"].cast(FloatType()))
df = df.withColumn("sepal_width", df["sepal_width"].cast(FloatType()))
df = df.withColumn("petal_length", df["petal_length"].cast(FloatType()))
df = df.withColumn("petal_width", df["petal_width"].cast(FloatType()))

df.write.format("delta").mode("overwrite").saveAsTable(f"{PROD_CATALOG_NAME}.{PROD_SCHEMA_NAME}.input")

# Databricks notebook source
# MAGIC %md
# MAGIC # XGBoost Classification in Python

# COMMAND ----------

# MAGIC %md ## Setup
# MAGIC
# MAGIC If you are running Databricks Runtime, uncomment `%pip install xgboost` in Cmd 3 to install the xgboost library.  
# MAGIC If you are running Databricks Runtime ML, xgboost is already installed. Skip to Cmd 4. 

# COMMAND ----------

# If you are running Databricks Runtime, uncomment this line and run this cell:
%pip install xgboost

# COMMAND ----------

# MAGIC %md
# MAGIC ## Parameters

# COMMAND ----------

train_dataset = dbutils.widgets.get("train_dataset")
input_table = dbutils.widgets.get("input_table")
predictions_table = dbutils.widgets.get("predictions_table")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Prepare data

# COMMAND ----------

import pandas as pd
import xgboost as xgb

# COMMAND ----------

raw_input = pd.read_csv(train_dataset,
                        header = 0,
                       names=["item","sepal length","sepal width", "petal length", "petal width","class"])
new_input = raw_input.drop(columns=["item"])
new_input["class"] = new_input["class"].astype('category')
new_input["classIndex"] = new_input["class"].cat.codes

# COMMAND ----------

from sklearn.model_selection import train_test_split
# Split to train/test
training_df, test_df = train_test_split(new_input)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Train XGBoost Model with Pandas DataFrames

# COMMAND ----------

dtrain = xgb.DMatrix(training_df[["sepal length","sepal width", "petal length", "petal width"]], label=training_df["classIndex"])

# COMMAND ----------

param = {'max_depth': 2, 'eta': 1, 'silent': 1, 'objective': 'multi:softmax'}
param['nthread'] = 4
param['eval_metric'] = 'auc'
param['num_class'] = 6

# COMMAND ----------

num_round = 10
bst = xgb.train(param, dtrain, num_round)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Prediction

# COMMAND ----------

scoring_data = spark.table(input_table)
scoring_data_pd = scoring_data.toPandas()
scoring_data_pd = scoring_data_pd.rename(columns={'sepal_length': 'sepal length', 'sepal_width': 'sepal width', 'petal_length': 'petal length', 'petal_width': 'petal width'})

# COMMAND ----------

dtest = xgb.DMatrix(scoring_data_pd)
ypred = bst.predict(dtest)
scoring_data_pd["predictions"] = ypred

# COMMAND ----------

scoring_data_pd = scoring_data_pd.rename(columns={'sepal length': 'sepal_length', 'sepal width': 'sepal_width', 'petal length': 'petal_length', 'petal width': 'petal_width'})

# COMMAND ----------

scoring_data_pd.display()

# COMMAND ----------

spark.createDataFrame(scoring_data_pd).write.format("delta").mode("overwrite").saveAsTable(predictions_table)

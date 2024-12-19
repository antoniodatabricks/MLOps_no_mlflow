# Databricks notebook source
# MAGIC %md
# MAGIC ## From within Databricks

# COMMAND ----------

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.jobs import Task, NotebookTask, Source

w = WorkspaceClient()

waiter = w.jobs.run_now_and_wait(job_id="1071752157059301", job_parameters={"input_table": "prod.default.non_mlflow_input_table_test", "predictions_table": "prod.default.non_mlflow_output_table_test"})

print(f"Job completed with final state: {waiter.state.life_cycle_state}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## From outside of Databricks

# COMMAND ----------

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.jobs import Task, NotebookTask, Source

w = WorkspaceClient(
    host='https://<your-databricks-instance>',
    token='<your-personal-access-token>'
)

waiter = w.jobs.run_now_and_wait(job_id="1071752157059301", job_parameters={"input_table": "prod.default.non_mlflow_input_table_test", "predictions_table": "prod.default.non_mlflow_output_table_test"})

print(f"Job completed with final state: {waiter.state.life_cycle_state}")

# COMMAND ----------



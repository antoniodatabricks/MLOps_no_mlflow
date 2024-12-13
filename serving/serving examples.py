# Databricks notebook source
# MAGIC %md
# MAGIC ## From within Databricks

# COMMAND ----------

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.jobs import Task, NotebookTask, Source

w = WorkspaceClient()

waiter = w.jobs.run_now_and_wait(job_id="613342059187312", job_parameters={"input_table": "prod.scoring.input", "predictions_table": "prod.scoring.predictions"})

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

waiter = w.jobs.run_now_and_wait(job_id="613342059187312", job_parameters={"input_table": "prod.scoring.input", "predictions_table": "prod.scoring.predictions"})

print(f"Job completed with final state: {waiter.state.life_cycle_state}")

# COMMAND ----------



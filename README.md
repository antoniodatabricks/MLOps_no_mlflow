# MLOps

MLOps pipeline from DEV to PROD

1. Create a repo in GitHub copying the code base from https://github.com/antoniodatabricks/MLOps_no_mlflow
2. Create a development branch in addition to the existing Main branch
3. Clone the development branch using Databricks Repos
4. Run https://github.com/antoniodatabricks/MLOps_no_mlflow/tree/development/demo_prep
5. Update the environment-related information in the bundle file by adding the Databricks Workspace URL:
   https://github.com/antoniodatabricks/MLOps_no_mlflow/blob/development/databricks.yml#L24
6. Update all “notebook_path” in the bundle file to reflect the new notebook paths. For examplehttps://github.com/antoniodatabricks/MLOps_no_mlflow/blob/development/databricks.yml#L11
7. Create a new GitAction Secret named “DATABRICKS_PROD_WS_TOKEN” containing a valid Databricks Personal Access Token
8. Commit the change to the development branch
9. Create a Pull Request from the development branch to the main branch (this should trigger a code validation action)
10. Merge the Pull Request (this should trigger the deployment in the Databricks Workspace)
11. GitHub Actions also triggers the execution of the job training_scoring. Wait for it to finish
12. Update the Databricks App source code with the ID of the job training_scoring deployed in the previous steps
    https://github.com/antoniodatabricks/MLOps_no_mlflow/blob/main/databricks_app/app.py#L23
14. Create a Custom Databricks App pointing to your local git folder https://github.com/antoniodatabricks/MLOps_no_mlflow/tree/main/databricks_app and provide its service principal admin privileges in the Workspace
15. Provide the Databricks App service principal all privileges to the catalog prod
16. Test the app by passing Input Table = prod.default.non_mlflow_input_table_test and Department = test

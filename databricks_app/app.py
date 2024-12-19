from flask import Flask, render_template, request, redirect, url_for, flash
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.jobs import Task, NotebookTask, Source

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

# Background processing logic
def process_input(input_table, department):
    """
    Example background process that returns True for success and False for error.
    Modify this logic as needed.
    """
    # Example condition: Both inputs must not be empty and must be alphanumeric
    if input_table and department:

        w = WorkspaceClient()

        catalog_output = "prod" #TODO: Parameterize this
        schema_output = "default" #TODO: Parameterize this
        output_table = f"{catalog_output}.{schema_output}.{department}_output_table"

        w.jobs.run_now(job_id="xxxx",
                       job_parameters={"input_table": input_table, 
                                       "predictions_table": output_table})
        
        return output_table

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get data from the form
        input_table = request.form.get('input_table')
        department = request.form.get('department')

        # Process the inputs

        try:
            output_table = process_input(input_table, department)
        except Exception as e:
            return str(e)

        return render_template("index.html", label=output_table)

    # Render the form page
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

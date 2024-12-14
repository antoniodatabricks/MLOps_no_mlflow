from flask import Flask, render_template, request, redirect, url_for, flash
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.jobs import Task, NotebookTask, Source

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

# Background processing logic
def process_input(input_table, prediction_table):
    """
    Example background process that returns True for success and False for error.
    Modify this logic as needed.
    """
    # Example condition: Both inputs must not be empty and must be alphanumeric
    if input_table and prediction_table:

        w = WorkspaceClient()

        waiter = w.jobs.run_now_and_wait(job_id="886001476856551", 
                                         job_parameters={"input_table": input_table, 
                                                         "predictions_table": prediction_table})
        return True, waiter.state.life_cycle_state
    return False, None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get data from the form
        input_table = request.form.get('input_table')
        prediction_table = request.form.get('prediction_table')

        # Process the inputs

        try:
            result, state = process_input(input_table, prediction_table)
        except Exception as e:
            return str(e)

        if result:
            flash(f'Databricks job finished with status: {state}', 'success')
        else:
            flash('Error! Invalid input or processing failed.', 'error')

        # Redirect to the same page to display the message
        return redirect(url_for('index'))

    # Render the form page
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

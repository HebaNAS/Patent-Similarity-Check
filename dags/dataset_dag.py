# Loading dependencies

import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from datetime import date, timedelta
from datetime import datetime as dt

# Import script files which are going be executed as Tasks by the DAG
import create_dataset

# DAG unique identifier
DAG_ID = 'dataset_dag'

# Datetime object to indicate at which time the DAG should start
DAG_START_DATE = airflow.utils.dates.days_ago(1)

# Scheduled interval at which the DAG will run
# here it will run only once
DAG_SCHEDULE_INTERVAL = None

# Default arguments applied to the DAG
DAG_DEFAULT_ARGS = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': DAG_START_DATE,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

yesterday = date.today() - timedelta(days=1)
dt = yesterday.strftime("%Y-%m-%d")


def conditionally_trigger(context, dag_run_obj):
    """
    This function decides whether or not to Trigger the remote DAG
    """

    params = context['params']['condition_param']

    # Look for the condition to trigger the DAG inside the context
    # parameters
    if context['params']['condition_param']:
        dag_run_obj.payload = {'message': context['params']['message']}
        print(dag_run_obj.payload)

        return dag_run_obj
    return None


# Create the DAG
with DAG(
        DAG_ID,
        default_args=DAG_DEFAULT_ARGS,
        schedule_interval=DAG_SCHEDULE_INTERVAL
) as dag:

    # Initialise a PythonOperator to execute the pdf_to_images.py script
    create_dataset_task = PythonOperator(
        task_id='create_dataset_task', python_callable=create_dataset.main, dag=dag)

    # Define the single task in this controller example DAG
    trigger_training_pipeline_task = TriggerDagRunOperator(
        task_id='trigger_training_pipeline_task',
        trigger_dag_id="training_pipeline",
        python_callable=conditionally_trigger,
        params={'condition_param': True,
                'message': 'New Dataset, Triggering Training'},
        dag=dag,
    )

    # Define pipeline sequence, allow for parallel tasks
    create_dataset_task >> trigger_training_pipeline_task

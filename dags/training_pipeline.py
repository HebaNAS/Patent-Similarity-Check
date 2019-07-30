# Loading dependencies

import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.subdag_operator import SubDagOperator
from datetime import date, timedelta
from datetime import datetime as dt

# Import script files which are going be executed as Tasks by the DAG
import create_dataset

# DAG unique identifier
DAG_ID = 'training_pipeline'

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

# Create the DAG
with DAG(
        DAG_ID,
        default_args=DAG_DEFAULT_ARGS,
        schedule_interval=DAG_SCHEDULE_INTERVAL
) as dag:

    # Initialise a PythonOperator to execute the pdf_to_images.py script
    create_dataset_task = PythonOperator(
        task_id='create_dataset_task', python_callable=create_dataset.main, dag=dag)

    # Define pipeline sequence, allow for parallel tasks
    create_dataset_task

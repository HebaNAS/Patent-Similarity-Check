# Loading dependencies

import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import date, timedelta
from datetime import datetime as dt

# Import script files which are going be executed as Tasks by the DAG
import images_to_text
import text_preprocessing
import document_embeddings

# DAG unique identifier
DAG_ID = 'core_pipeline'

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

    # Initialise a PythonOperator to execute the images_to_text.py script
    images_to_text_task = PythonOperator(
        task_id='images_to_text_task', python_callable=images_to_text.main, dag=dag)

    # Initialise a PythonOperator to execute the text_preprocessing.py script
    text_preprocessing_task = PythonOperator(
        task_id='text_preprocessing_task', python_callable=text_preprocessing.main, dag=dag)

    # Initialise a PythonOperator to execute the document_embeddings.py script
    document_embeddings_task = PythonOperator(
        task_id='document_embeddings_task', python_callable=document_embeddings.main, dag=dag)

    # Define pipeline sequence
    images_to_text_task >> text_preprocessing_task >> document_embeddings_task

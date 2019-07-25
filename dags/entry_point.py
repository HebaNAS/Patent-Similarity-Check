# Loading dependencies

import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.subdag_operator import SubDagOperator
from datetime import date, timedelta
from datetime import datetime as dt

# Import script files which are going be executed as Tasks by the DAG
import scripts.pdfs_to_images
import scripts.figure_extraction
import scripts.image_preprocessing
import core_pipeline

# DAG unique identifier
DAG_ID = 'entry_point'

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
    pdfs_to_images_task = PythonOperator(
        task_id='pdfs_to_images_task', python_callable=pdfs_to_images.main, dag=dag)

    # Initialise a PythonOperator to execute the figure_extraction.py script
    figure_extraction_task = PythonOperator(
        task_id='figure_extraction_task', python_callable=figure_extraction.main, dag=dag)

    # Initialise a PythonOperator to execute the images_to_text.py script
    image_preprocessing_task = PythonOperator(
        task_id='image_preprocessing_task', python_callable=image_preprocessing.main, dag=dag)

    # Define pipeline sequence
    pdfs_to_images_task >> figure_extraction_task >> image_preprocessing_task

    # Start parallel pipelines
    image_preprocessing_task >> core_pipeline
    image_preprocessing_task >> dynamic_dag

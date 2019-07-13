# Loading dependencies

import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.hive_operator import HiveOperator
from airflow.contrib.sensors.file_sensor import FileSensor
from datetime import date, timedelta
from datetime import datetime as dt

# Import script files which are going be executed as Tasks by the DAG
import pdfs_to_images
import images_to_text
import text_preprocessing

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

	# Initialise a PythonOperator to execute the pdf_to_images.py script
	pdfs_to_images_task = PythonOperator(task_id='pdfs_to_images_task', python_callable=pdfs_to_images.main, dag=dag)

	# Initialise a PythonOperator to execute the images_to_text.py script
	images_to_text_task = PythonOperator(task_id='images_to_text_task', python_callable=images_to_text.main, dag=dag)

	# Initialise a PythonOperator to execute the text_preprocessing.py script
	text_preprocessing_task = PythonOperator(task_id='text_preprocessing_task', python_callable=text_preprocessing.main, dag=dag)

	# Define pipeline sequence
	pdfs_to_images_task >> images_to_text_task >> text_preprocessing_task

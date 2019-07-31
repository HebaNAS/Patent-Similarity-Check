# Loading dependencies
import airflow
from airflow import DAG
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from datetime import date, timedelta
from datetime import datetime as dt

# Import script files which are going be executed as Tasks by the DAG
import folder_watch

# DAG unique identifier
DAG_ID = 'trigger_training'

# Datetime object to indicate at which time the DAG should start
DAG_START_DATE = airflow.utils.dates.days_ago(1)

# Scheduled interval at which the DAG will run
# here it will run once a day
DAG_SCHEDULE_INTERVAL = '@daily'

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

# Creating the DAG
with DAG(
        DAG_ID,
        default_args=DAG_DEFAULT_ARGS,
        schedule_interval=DAG_SCHEDULE_INTERVAL
) as dag:

    # Initialise a TriggerDagRunOperator that waits for a python callable
    # to return true so it triggers the training_pipeline dag
    trigger_training_dag = TriggerDagRunOperator(
        task_id='trigger_training_dag', python_callable=folder_watch.main, op_args='/usr/local/airflow/Dataset', trigger_dag_id='training_pipeline', dag=dag)

    trigger_training_dag

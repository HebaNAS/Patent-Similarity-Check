# Loading dependencies
import airflow
from airflow import DAG
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from datetime import date, timedelta
from datetime import datetime as dt

# Import script files which are going be executed as Tasks by the DAG
import scripts.folder_watch

# DAG unique identifier
DAG_ID = 'file_add_watcher'

# Datetime object to indicate at which time the DAG should start
DAG_START_DATE = airflow.utils.dates.days_ago(1)

# Scheduled interval at which the DAG will run
# here it will run once every hour
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

    # Initialise a TriggerDagRunOperator that waits for the BashOperator
    # to return true so it triggers the core_pipeline dag
    trigger_entry_point = TriggerDagRunOperator(
        task_id='trigger_entry_point_dag', python_callable=folder_watch.main, trigger_dag_id='entry_point', dag=dag)

    trigger_entry_point

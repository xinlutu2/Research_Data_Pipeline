"""Simple weather DAG that uses a few python operators."""
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

import challenge as c

from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2018, 4, 1),
    'email': ['airflow@airflow.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG Object
dag = DAG(
    'weather_dag',
    default_args=default_args,
    schedule_interval='0 0 * * *',  # DAG will run once a day at midnight
    catchup=False,
)

start_tast = DummyOperator(
    task_id='start',
    dag=dag
)


# Fetch weather data based on source_id, flatten into .csv files, save on local file system
get_weather_task = PythonOperator(task_id='get_weather',
                                  provide_context=True,
                                  python_callable=c.Extract_Transform.get_weather,
                                  params={'base':'Morse'},
                                  retries=3,
                                  dag=dag)


# Move entire file structure onto S3
load_to_s3_task = PythonOperator(task_id='load_to_s3',
                                 provide_context=True,
                                 python_callable=c.Load.upload_to_S3,
                                 params={'base':'Morse'},
                                 retries=3,
                                 dag=dag)

# end workflow
end_task = DummyOperator(task_id='end', dag=dag)

start_tast >> get_weather_task >> load_to_s3_task >> end_task

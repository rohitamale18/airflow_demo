from datetime import timedelta

import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.sensors import S3KeySensor
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.utils.trigger_rule import TriggerRule

from src.utils import download_s3_file


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(2),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

word_count_dag = DAG(
    'word-counter',
    default_args=default_args,
    description='Count the frequency of occurrence of a word in a file',
    schedule_interval=timedelta(days=1),
)

local_file_sensor = FileSensor(
    task_id='check_for_local_file',
    filepath='/usr/local/airflow/data/sample.txt',
    dag=word_count_dag,
    timeout=30,
    poke_interval=10,
)

s3_file_sensor = S3KeySensor(
    task_id='check_for_s3_file',
    aws_conn_id='my_conn_S3',
    bucket_name='calculator-api',
    bucket_key='twitter-raw/eia-prod/input.txt',
    wildcard_match=True,
    timeout=30,
    poke_interval=10,
    dag=word_count_dag,
    trigger_rule=TriggerRule.ALL_FAILED,
)

s3_file_download = PythonOperator(
    task_id='download_text_file_from_s3',
    python_callable=download_s3_file,
    op_args=['calculator-api', 'twitter-raw/eia-prod/input.txt', '/usr/local/airflow/data/sample.txt'],
    dag=word_count_dag,
)

count_words = BashOperator(
    task_id='count_words',
    bash_command='spark-submit \
/opt/spark-2.4.1/examples/src/main/python/wordcount.py /usr/local/airflow/data/sample.txt',
    name='word-count',
    trigger_rule=TriggerRule.ONE_SUCCESS,
    dag=word_count_dag,
)

# s3_file_sensor.set_upstream(local_file_sensor)
local_file_sensor >> s3_file_sensor >> s3_file_download
count_words.set_upstream(local_file_sensor)
count_words.set_upstream(s3_file_download)

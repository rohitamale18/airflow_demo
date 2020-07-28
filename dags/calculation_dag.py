from datetime import timedelta

import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(2),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'adhoc':False,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'trigger_rule': u'all_success'
}


def set_variables(a, b):
    return a, b


def add_nums(**context):
    values = context['task_instance'].xcom_pull(task_ids='set_data')
    s = values[0] + values[1]
    print("Sum is: " + str(s))
    return s


def multiply_nums(**context):
    values = context['task_instance'].xcom_pull(task_ids='set_data')
    s = values[0] * values[1]
    print("Product is: " + str(s))
    return s


test_dag = DAG(
    'calculation-dag',
    default_args=default_args,
    description='Demo DAG to calculate results',
    schedule_interval=timedelta(days=1),
)

set_nums = PythonOperator(
    task_id='set_data',
    python_callable=set_variables,
    op_args=[5, 10],
    dag=test_dag,
)

addition = PythonOperator(
    task_id='add_data',
    python_callable=add_nums,
    provide_context=True,
    dag=test_dag,
)

multiplication = PythonOperator(
    task_id='multiply_data',
    python_callable=multiply_nums,
    provide_context=True,
    dag=test_dag,
)

set_nums >> addition
set_nums >> multiplication

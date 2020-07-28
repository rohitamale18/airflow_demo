from datetime import timedelta

import airflow
from airflow import DAG
from airflow.contrib.operators.ssh_operator import SSHOperator
from airflow.contrib.hooks.ssh_hook import SSHHook


sshHook = SSHHook(remote_host='172.20.0.2',
                  port=22,
                  username='airflow',)


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

word_count_remote_dag = DAG(
    'word-counter-remote',
    default_args=default_args,
    description='Count the frequency of occurrence of a word in a file',
    schedule_interval=timedelta(days=1),
)

count_words = SSHOperator(
    task_id='set_env_vars',
    ssh_hook=sshHook,
    command='export JAVA_URL_VERSION="8u212b04" \
    export SPARK_LOCAL_IP="spark-master" \
    export PYTHONHASHSEED="1" \
    export HOSTNAME="067ee4f55627" \
    export SPARK_MASTER_WEBUI_PORT="8080" \
    export JAVA_BASE_URL="https://github.com/AdoptOpenJDK/openjdk8-upstream-binaries/releases/download/jdk8u212-b04/OpenJDK8U-" \
    export HOME="/root" \
    export OLDPWD="/spark/examples" \
    export SCALA_HOME="/usr/share/scala" \
    export JAVA_VERSION="8u212-b04" \
    export SPARK_MASTER_LOG="/spark/logs" \
    export HADOOP_VERSION="2.7" \
    export TERM="xterm" \
    export SPARK_VERSION="2.4.3" \
    export PATH="/usr/local/openjdk-8/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" \
    export LANG="C.UTF-8" \
    export SCALA_VERSION="2.12.4" \
    export DAEMON_RUN="true" \
    export JAVA_HOME="/usr/local/openjdk-8" \
    export PWD="/spark" \
    export SPARK_MASTER_PORT="7077" \
    export SPARK_HOME="/spark"; \
    /spark/bin/spark-submit /spark/examples/src/main/python/wordcount.py /spark/sample.txt',
    name='word-count-remote',
    dag=word_count_remote_dag,
)

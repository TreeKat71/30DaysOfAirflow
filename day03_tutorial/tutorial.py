from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'muller',
    'depends_on_past': False,
    'start_date': datetime(2019, 8, 1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('daily_report',
          default_args=default_args,
          schedule_interval=timedelta(days=1))

# t1, t2 and t3 are examples of tasks created by instantiating operators
t1_a = BashOperator(
    task_id='get_db_A',
    bash_command='sh script_A.sh',
    dag=dag)

t1_b = BashOperator(
    task_id='get_db_B',
    bash_command='sh script_B.sh',
    dag=dag)

t1_c = BashOperator(
    task_id='get_db_C',
    bash_command='sh script_C.sh',
    dag=dag)

t2 = BashOperator(
    task_id='join_data',
    bash_command='sh join_data.sh',
    dag=dag)

t3 = BashOperator(
    task_id='analyze',
    bash_command='sh analyze.sh',
    dag=dag)


(t1_a, t1_b, t1_c) >> t2 >> t3

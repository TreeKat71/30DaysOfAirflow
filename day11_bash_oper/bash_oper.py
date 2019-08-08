import re
from datetime import datetime, timedelta

import requests
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
#===================   dag config  =====================
default_args = {
    'owner': 'muller'
}

dag = DAG('example_bash_oper',
           catchup=False,
           start_date = datetime(2019, 1, 1),
           schedule_interval='@daily',
           default_args=default_args)
#=========================  Python Operator  ============================
t_print_date = BashOperator(
    task_id='print_date',
    bash_command='date',
    xcom_push=True, # airflow version 1.10.3 or 1.10.4
    # do_xcom_push=True, # airflow current master branch
    dag=dag,
)

t_scrape_data = BashOperator(
    task_id='scrape_data',
    bash_command=("""
        curl -s "https://www.nasdaq.com/" \
                | grep 'storeIndexInfo(\"S&P 500\"' \
                | awk -F'","' '{print $2}'
    """),
    xcom_push=True, # airflow version 1.10.3 or 1.10.4
    # do_xcom_push=True, # airflow current master branch
    dag=dag,
)


templated_command = """
    echo "{{ ti.xcom_pull(task_ids='print_date') }} \
    {{ ti.xcom_pull(task_ids='scrape_data') }}"
"""

t_combine = BashOperator(
    task_id='combine',
    bash_command=templated_command,
    dag=dag,
)


t_print_date >> t_scrape_data >> t_combine

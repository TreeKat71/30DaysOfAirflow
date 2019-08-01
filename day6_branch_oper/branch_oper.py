import re
from datetime import datetime, timedelta

import requests
from airflow import DAG
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
#===================   dag config  =====================
default_args = {
    'owner': 'muller'
}

dag = DAG('example_branch_python_operator',
           catchup=False,
           start_date = datetime(2019, 1, 1),
           schedule_interval='@daily',
           default_args=default_args)
#=========================  Python Branch Operator  ============================
PATTERN = 'storeIndexInfo\("S&P 500","(.+?)"'
extractor = re.compile(PATTERN)

def if_value_higher_3000():
    """
    This function shows
    1. get value from website
    2. if value > 3000, we send email as an alert, otherwise we do nothing

    python branch operator should return "task name" as a choice
    """
    res = requests.get("https://www.nasdaq.com/")
    SnP500_value = extractor.findall(res.text)[0]
    # You can see this result from the log
    print(SnP500_value)
    if float(SnP500_value) > 3000:
        return 'send_email'
    else:
        return 'do_nothing'

t_get_SnP500 = BranchPythonOperator(
    task_id='get_SnP500_value',
    python_callable=if_value_higher_3000,
    dag=dag,
)

#===============================================================================
t_send_email = DummyOperator(
    task_id='send_email',
    dag=dag,
)

t_do_nothing = DummyOperator(
    task_id='do_nothing',
    dag=dag,
)

#===============================================================================
t_get_SnP500 >> (t_send_email, t_do_nothing)

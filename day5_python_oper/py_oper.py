import re
from datetime import datetime, timedelta

import requests
from airflow import DAG
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
#===================   dag config  =====================
default_args = {
    'owner': 'muller'
}

dag = DAG('example_python_operators',
           start_date = datetime(2019, 1, 1),
           schedule_interval='@daily',
           default_args=default_args)
#============================== Python Operator ================================
PATTERN = 'storeIndexInfo\("S&P 500","(.+?)"'
extractor = re.compile(PATTERN)

def get_SnP500():
    """
    use requests library to scrapy site nasdaq
    to get S&P 500 value
    """
    res = requests.get("https://www.nasdaq.com/")
    value = extractor.findall(res.text)[0]
    return value

t_get_SnP500 = PythonOperator(
                    task_id="get_SnP500_value",
                    python_callable=get_SnP500,
                    dag=dag)

#=========================  Python Branch Operator  ============================
def if_value_higher_3000(**kwargs):
    """
    This function shows
    1. get value from task "get_SnP500_value"
    2. if value > 3000, we send email as an alert, otherwise we do nothing

    python branch operator should return "task name" as a choice
    """
    # Xcom is a mechanism how airflow tasks exchange values
    # We will dive into xcom later
    SnP500_value = kwargs['ti'].xcom_pull(task_ids="get_SnP500_value")
    if SnP500_value > 3000:
        return 'send_email'
    else:
        return 'do_nothing'

t_if_value_higher_3000 = BranchPythonOperator(
    task_id='if_value_higher_3000',
    python_callable=if_value_higher_3000,
    provide_context=True, # if you want to use kwargs, remember to set this True
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
t_get_SnP500 >> t_if_value_higher_3000 >> (t_send_email, t_do_nothing)

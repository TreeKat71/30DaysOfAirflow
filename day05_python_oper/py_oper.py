import re
from datetime import datetime, timedelta

import requests
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
#===================   dag config  =====================
default_args = {
    'owner': 'muller'
}

dag = DAG('example_python_operator',
           catchup=False,
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

#===============================================================================
t_send_email = DummyOperator(
    task_id='send_email',
    dag=dag,
)
#===============================================================================
t_get_SnP500 >> t_send_email

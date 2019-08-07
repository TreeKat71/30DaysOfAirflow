import re
from datetime import datetime, timedelta

import requests
from airflow import DAG
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.email_operator import EmailOperator
#===================   dag config  =====================
default_args = {
    'owner': 'muller'
}

dag = DAG('example_xcom_3',
           catchup=False,
           start_date = datetime(2019, 1, 1),
           schedule_interval='@daily',
           default_args=default_args)
#=========================  Python Branch Operator  ============================
PATTERN = 'storeIndexInfo\("S&P 500","(.+?)"'
extractor = re.compile(PATTERN)

def get_value_see_if_value_higher_3000(**kwargs):
    res = requests.get("https://www.nasdaq.com/")
    value = extractor.findall(res.text)[0]
    SnP500_value = float(value)
    kwargs['ti'].xcom_push(key='SnP',value=SnP500_value)
    # if SnP500_value > 3000:
    if True:
        return 'send_email'
    else:
        return 'do_nothing'

t_higher_3000 = BranchPythonOperator(
    task_id='higher_3000',
    python_callable=get_value_see_if_value_higher_3000,
    provide_context=True,
    dag=dag,
)
#===============================================================================
t_send_email = EmailOperator(
            task_id='send_email',
            subject="Today's S&P 500 value",
            to=" {{ var.json.var3.email_to }} ",
            html_content="""
                Hey, it is {{ ti.xcom_pull(key='SnP', task_ids='higher_3000') }}
            """,
            dag=dag)

t_do_nothing = DummyOperator(
    task_id='do_nothing',
    dag=dag,
)

#===============================================================================
t_higher_3000 >> (t_send_email, t_do_nothing)

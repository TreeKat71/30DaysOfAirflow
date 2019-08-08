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

dag = DAG('example_email_operator_with_var',
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
    # As we are going to test email operator,
    # we set it to Ture
    if True:
        return 'send_email'
    else:
        return 'do_nothing'

t_get_SnP500 = BranchPythonOperator(
    task_id='get_SnP500_value',
    python_callable=if_value_higher_3000,
    dag=dag,
)

#===============================================================================
t_send_email = EmailOperator(
            task_id='send_email',
            subject="Today's S&P 500 value",
            to=" {{ var.json.var3.email_to }} ",
            cc=" {{ var.json.var3.email_cc }} ",
            html_content="Hey, it is higher than 3000",
            dag=dag)

t_do_nothing = DummyOperator(
    task_id='do_nothing',
    dag=dag,
)

#===============================================================================
t_get_SnP500 >> (t_send_email, t_do_nothing)

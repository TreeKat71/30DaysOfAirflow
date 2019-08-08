import re
from datetime import datetime, timedelta

import requests
from airflow import DAG
from airflow.operators.email_operator import EmailOperator
#===================   dag config  =====================
default_args = {
    'owner': 'muller'
}

dag = DAG('example_xcom_1',
           catchup=False,
           start_date = datetime(2019, 1, 1),
           schedule_interval='@daily',
           default_args=default_args)
#=========================  Python Operator  ============================
PATTERN = 'storeIndexInfo\("S&P 500","(.+?)"'
extractor = re.compile(PATTERN)
res = requests.get("https://www.nasdaq.com/")
SnP500_value = extractor.findall(res.text)[0]
print(f"XXXXX{SnP500_value}XXXXX")

t_send_email = EmailOperator(
            task_id='send_email',
            subject="Today's S&P 500 value",
            to=" {{ var.json.var3.email_to }} ",
            html_content=f"Hey, it is {SnP500_value}",
            dag=dag)

t_send_email

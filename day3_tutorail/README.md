Tutorial
------------
> Please read this with tutorial.py

For examples, we want to export a report daily.
<br>
There are steps to do this:
- task_1_a : extract data from db_A
- task_1_b : extract data from db_B
- task_1_c : extract data from db_C
- task_2 : join datasets and transform them to the format you want
- task_3 : analyze data


Define workflow
------------
In Airflow, workflow is called "DAG" – or a Directed Acyclic Graph.
<br>
DAG is a collection of tasks with their relationships and dependencies.


Define dag
------------
Define the "export report" workflow, triggered everyday
```python
dag = DAG('export_report', # dag name
          default_args=default_args,  # args passed in as default, we will dive into them later
          schedule_interval=timedelta(days=1) # frequency that dag will be executed
          )
```
Airflow also supports **cron expression**
<br>
The above workflow is equivant to below
```python
dag = DAG(..., schedule_interval='0 0 * * *')
or
dag = DAG(..., schedule_interval="@daily")
```


Define tasks
------------
There are lots kinds of operators that you can use in the dag.
Right now I simply use BashOperator as an example
```python
t1 = BashOperator(
      task_id='print_date',
      bash_command='date',
      dag=dag)
```

Define dependency
------------
I think it is quite straightforward
```python
t1 >> t2
# t2 will be executed when t1 is finished
```

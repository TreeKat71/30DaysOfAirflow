Tasks
------------
As I mentioned earlier, task is defined by operator.

What is operator
------------
There are two main kinds of operators you can use in airflow.
1. Operators
2. Sensors

And I will briefly introduce what they are, and when you are going to use these.

Operators
------------
>While DAGs describe how to run a workflow, Operators determine what actually gets done.
<br>
<br>
An operator describes a single task in a workflow. 

Operators are the core concept of the airflow, and you can use operators to do almost whatever you want.

For example, you can use BashOperator to run a linux command, or use PythonOperator to run a python function. Lots of things you can do with operators.

part of operators:
- bash_operator
- branch_operator
- email_operator
- mysql_operator
- python_operator
- subdag_operator
- ssh_operator
- spark_sql_operator
- sftp_operator
- ...


Sensors
------------
>Sensors are a special kind of operator that will keep running until a certain criterion is met.

For example, you need to analyze a file to export a report to your boss, but you don't know the exactly time the file will be done (which is handled by other team).
You and other team have a deal, they will put the file at a specific folder when it is done.
Then you can use sensor to poke this folder.

part of sensors:
- bigquery_sensor
- file_sensor
- hdfs_sensor
- http_sensor
- s3_key_sensor
- sql_sensor
- sftp_sensor
- ...



What is Next
------------
As different operators can do different thing, such as
BashOperator can run a linux command, PythonOperator can run a python function. They must have different input arguments.
<br>
So in the next few sections, I will introduce some operators I use more often.

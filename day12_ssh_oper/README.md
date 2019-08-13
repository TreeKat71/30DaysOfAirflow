Description
------------
In this section, I am going to demonstrate how to access remote server in airflow.

This section will cover things below
- Authentication
- BashOperator
- SSHOperator



Authentication
------------
In general, there are two ways to access remote servers

1. Password Authentication
2. [Public Key Authentication](https://serverpilot.io/docs/how-to-use-ssh-public-key-authentication)

*click the link and follow the steps if you don't know how to set things properly



BashOperator
------------
Airflow will run tasks automatically so we are not able to enter the password during the tasks.

As a workaround, we can access remote server without password by setting public-key authentication.

```python
t1 = BashOperator(
    task_id='task_name',
    # ssh remote server and run command "cat sample.txt"
    bash_command='ssh muller@12.34.56.78 cat sample.txt',
    dag=dag,
)
```

But I recommend you use SSHOperator instead, which uses **Hook**/**Connection** to access servers. Right now, just take them as a magic way to connect to servers, I will explain it in the next section.



SSHOperator
------------
> Execute commands on given remote host using the ssh_hook.


Simple example

```python
t1 = SSHOperator(
        task_id='task_name',
        ssh_conn_id='conn_id', # some magic
        command='cat sample.txt', # command run on remote server
        dag=dag)
```



What's Next
------------
Right now, you can access remote server without password, but it is not an ideal way to handle this.

In the next section, I will introduce how to use **Hook**/**Connection** to make your code more flexible and clear.

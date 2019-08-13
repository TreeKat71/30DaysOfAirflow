Description
------------
In this section, I am going to demonstrate how to access remote server in airflow.

This section will cover things below
- Authentication
- BashOperator
- SSHOperator



Authentication
------------
In general, there are two ways to access server

1. Password Authentication
2. [Public Key Authentication](https://serverpilot.io/docs/how-to-use-ssh-public-key-authentication)



BashOperator
------------
Start from what we are familiar with - BashOperator

As a workaround, we can access remote server without password, after setting authentication properly.

```python
t1 = BashOperator(
    task_id='task_name',
    # ssh remote server and run command "cat sample.txt"
    bash_command='ssh muller@12.34.56.78 cat sample.txt',
    dag=dag,
)
```

But I recommend you use SSHOperator instead, which uses **Hook**/**Connection** to access servers.

I will mention them in the next section.



SSHOperator
------------
> Execute commands on given remote host using the ssh_hook.


Simple example

```python
t1 = SSHOperator(
        task_id='task_name',
        ssh_conn_id='conn_id',
        command='cat sample.txt',
        dag=dag)
```



What's Next
------------
Right now, you can access remote server after setting the public key authentication, but it seems not an ideal way to handle this.

In the next section, I will introduce how to use **Hook**/**Connection** to make your code more flexible and clear.

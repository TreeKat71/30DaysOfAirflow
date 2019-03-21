## Basic Setting
- airflow needs a home
- "~/airflow" is the default, if you don't set it

What I prefer

```python
# pipenv will load .env automatically
$ touch .env
add AIRFLOW_HOME=where_you_want/airflow into .env
```
![alt .env](imgs/env.png)
or
```python
$ export AIRFLOW_HOME=where_you_want/airflow
```


## Install
What I prefer
```python
# use pipenv to control python version and create virtual environment
$ pipenv shell --python 3.6
# you should see "Loading .env environment variables…"
# if you take .env as your previous step
$ pipenv install apache-airflow
```
or
```python
$ pip install apache-airflow
```

## Hello World
```python
# initialize the database (sqlite)
$ airflow initdb

# start the web server, default port is 8080
$ airflow webserver
```
- visit localhost:8080 in the browser
- and enable the example dag in the home page

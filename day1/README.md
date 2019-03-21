Basic Setting
------------
- airflow needs a home
- "~/airflow" is the default, if you don't set it

What I prefer: use .env to set environment variables

    $ touch .env

add "AIRFLOW_HOME=where_you_want/airflow" to .env

![alt .env](imgs/env.png)
or

    $ export AIRFLOW_HOME=where_you_want/airflow



Installation
------------
What I prefer: use pipenv to control python version and create virtual environment

    $ pipenv shell --python 3.6
    // pipenv will load .env automatically
    // you would see "Loading .env environment variables…", if you take .env as your previous step
    $ pipenv install apache-airflow
or

    $ pip install apache-airflow


Hello World
------------
initialize the database (sqlite)

    $ airflow initdb

start the web server, default port is 8080

    $ airflow webserver

- visit localhost:8080 in the browser
- and enable the example dag in the home page

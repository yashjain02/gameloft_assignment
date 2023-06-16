from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.email import send_email
from snowflake_query import Snowflake

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 2,
    'retry_delay': timedelta(minutes=1),
    'email_on_failure': True,
    'email': global-de@gameloft.com
}

dag = DAG('snowflake_queries_dag',
           default_args=default_args, 
           schedule_interval='0 0 * * *')

queries = {
    'import_user_data_task': '',
    'import_currency_conversion_task': '',
    'aggregate_transaction_task': ''
}
def execute_query(query):
    try:
        snowflake_query = Snowflake()
        snowflake_query.query(query)
    except Exception as e:
        send_email(global-de@gameloft.com, "Task Failed", "snowflake_queries_dag has been broken")
        raise e

start_task = DummyOperator(task_id='start_task', dag=dag)

import_user_data_task = PythonOperator(
    task_id='import_user_data_task',
    provide_context=True,
    python_callable=execute_query,
    op_kwargs={'query': queries['import_user_data_task']},
    dag=dag
)

import_currency_conversion_task = PythonOperator(
    task_id='import_currency_conversion_task',
    provide_context=True,
    python_callable=execute_query,
    op_kwargs={'query': queries['import_currency_conversion_task']},
    dag=dag
)

aggregate_transaction_task = PythonOperator(
    task_id='aggregate_transaction_task',
    provide_context=True,
    python_callable=execute_query,
    op_kwargs={'query': queries['aggregate_transaction_task']},
    dag=dag
)

end_task = DummyOperator(task_id='end_task', dag=dag)

start_task >> [import_user_data_task, import_currency_conversion_task] >> aggregate_transaction_task >> end_task

# Airflow pattern: DAG with task dependencies
from airflow import DAG
from airflow.operators.python import PythonOperator

with DAG('data_pipeline', schedule_interval='@daily') as dag:
    extract = PythonOperator(task_id='extract', python_callable=extract_data)
    transform = PythonOperator(task_id='transform', python_callable=transform_data)
    load = PythonOperator(task_id='load', python_callable=load_data)
    validate = PythonOperator(task_id='validate', python_callable=validate_data)
    
    extract >> transform >> load >> validate

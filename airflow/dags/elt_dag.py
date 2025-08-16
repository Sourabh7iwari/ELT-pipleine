from datetime import datetime, timedelta
from airflow import DAG
from docker.types import Mount

from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator

from airflow.providers.docker.operators.docker import DockerOperator
import subprocess

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}

def run_elt_script():
    script_path = "/opt/airflow/elt/elt_script.py"
    result = subprocess.run(["python", script_path],
                            capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"ELT script failed: {result.stderr}")
    else:
        print(f"ELT script output: {result.stdout}")
    
dag = DAG(
    'elt_and_dbt',
    default_args=default_args,
    description='A simple ETL DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2025, 8, 2),
    catchup=False,
)

t1 = PythonOperator(
    task_id = "run_elt_script",
    python_callable=run_elt_script,
    dag=dag 
)

t2 =  DockerOperator(
    task_id = "dbt_run",
    image = 'ghcr.io/dbt-labs/dbt-postgres:1.4.7',
    command=[
       "run",
        "--profiles-dir",
        "/root",
        "--project-dir",
        "/dbt",
        "--full-refresh"
    ],
    auto_remove=True,
    docker_url="unix://var/run/docker.sock",
    mounts=[
        Mount(source='/home/sourabh7iwari/Repository/elt/custom_postgres',
              target='/dbt', type='bind'),
        Mount(source='/home/sourabh7iwari/.dbt',
              target='/root', type='bind')
    ],
    network_mode="elt_elt_network",
    mount_tmp_dir=False,
    dag=dag
)

t1 >> t2
import subprocess
import time

def wait_for_postgres(host, max_retries=5,delay=5):
    """
    Wait for PostgreSQL to be ready by attempting to connect to it.
    :param host: Hostname or IP address of the PostgreSQL server.
    :param max_retries: Maximum number of connection attempts.
    :param delay: Delay between attempts in seconds.
    """
    for attempt in range(max_retries):
        try:
            result = subprocess.run(
                ["pg_isready", "-h", host],
                check=True,
                capture_output=True,
                text=True
            )
            if "accepting connections" in result.stdout:
                print(f"PostgreSQL is ready on {host}.")
                return True
        except subprocess.CalledProcessError as e:
            print(f"Attempt {attempt + 1}/{max_retries}: PostgreSQL is not ready yet. Error: {e}")
            time.sleep(delay)
    print(f"PostgreSQL is not ready after {max_retries} attempts.")
    return False   

if not wait_for_postgres(host="source_postgres"):
    exit(1)

print("Starting the ETL process...")

source_config={
    'dbname': 'source_db',
    'user': 'postgres',
    'password': 'secret',
    'host': 'source_postgres',
}

destination_config={
    'dbname': 'destination_db',
    'user': 'postgres',
    'password': 'secret',
    'host': 'destination_postgres',
}

dump_command = [
    "pg_dump",
    '-h', source_config['host'],
    '-U', source_config['user'],
    '-d', source_config['dbname'],
    '-f', 'data_dump.sql',
    '-w'
    ]

subprocess_env =  dict(PGPASSWORD=source_config['password'])
try:
    subprocess.run(dump_command, env=subprocess_env, check=True)
    print("Data dump completed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error during data dump: {e}")

load_command = [
    "psql",
    '-h', destination_config['host'],
    '-U', destination_config['user'],
    '-d', destination_config['dbname'],
    '-a','-f', 'data_dump.sql',
]

subprocess_env = dict(PGPASSWORD=destination_config['password'])

try:
    subprocess.run(load_command, env=subprocess_env, check=True)
    print("Data load completed successfully.")
except subprocess.CalledProcessError as e:  
    print(f"Error during data load: {e}")

print("ETL process completed.")
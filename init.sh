#!/bin/bash
set -e

echo "Upgrading Airflow database..."
airflow db upgrade

echo "Creating admin user..."
airflow users create \
  --username airflow \
  --password password \
  --firstname John \
  --lastname Doe \
  --role Admin \
  --email admin@example.com

echo "Initialization complete. Exiting."
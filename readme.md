## Follow the steps below to run the project:

### Prerequisites
- Ensure Docker and Docker Compose are installed on your system.

### Steps to Run
1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2. Build and start the project using Docker Compose:
    ```bash
    docker-compose up --build
    ```

3. Open your browser and navigate to:
    ```
    http://localhost:8080
    ```

4. Enter your credentials to log in.
- **Username:** `airflow`
- **Password:** `password`
5. Run the DAG from the web interface.

6. Check the results in the PostgreSQL database using the CLI:
    ```bash
    docker exec -it <postgres-container-name> psql -U postgres
    ```
    postgres container name is generally is : elt-destination_postgres-1

Replace `<postgres-container-name>`(elt-destination_postgres-1), and `<database-name>`(postgres).

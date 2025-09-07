# BI Project - ELT Pipeline with Apache Airflow

This repository contains the ELT pipeline for the Business Intelligence project and its automated orchestration with Apache Airflow using Docker.



## Project Structure


* `assignmentProyect01/`
* `|-- ETLProject.ipynb` : Main notebook for manual execution of the pipeline
* `|-- requirements.txt`     : Python dependencies
* `|-- olist.db`             : Generated SQLite database
* `|-- src/`                 : Source code (extraction, loading, transformation, configuration)
* `|-- dataset/`             : Original CSV data files
* `|-- queries/`             : SQL queries for transformations
* `|-- airflow/`             : Configuration and files for Airflow with Docker
* `|   |-- docker-compose.yml`       : Docker orchestration for Airflow and PostgreSQL
* `|   |-- requirements.txt`         : Dependencies for Airflow
* `|   |-- dags/`
* `|       |-- elt_pipeline_dag.py`  : DAG that automates the ELT pipeline
* `|-- tests/`                       : Unit tests and test data

## Environment Setup

Before running the pipeline, you need to set up a Python virtual environment:

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
   - **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   - **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Install ipykernel to use the virtual environment in Jupyter:
```bash
pip install ipykernel
```

5. Create a Jupyter kernel with the virtual environment:
```bash
python -m ipykernel install --user --name=venv --display-name="Python (venv)"
```

### Using the Virtual Environment in VS Code

When opening `ETLProject.ipynb` in VS Code:

1. Open the project folder in VS Code
2. Open the `ETLProject.ipynb` file
3. VS Code will automatically detect available kernels
4. Click on the kernel selector in the top right corner of the notebook (it might show "Select Kernel" or the current kernel name)
5. Choose "Python Environments..." from the dropdown
6. Select "Python (venv)" or the path to your virtual environment (usually `./venv/Scripts/python.exe` on Windows or `./venv/bin/python` on macOS/Linux; 
If it doesn't appear, restart vscode and activate the venv again.)
7. The notebook will now use your virtual environment with all installed dependencies

**Note:** Make sure you have the Python extension installed in VS Code for proper notebook support.

**Important:** Keep the virtual environment activated for all subsequent operations, including Docker commands, as the `cryptography` library and other dependencies are installed there.

## Manual ELT Pipeline Execution

To run the pipeline manually (for example in Jupyter):

1. Make sure you have a Python environment installed with the necessary dependencies (`pandas`, `sqlalchemy`, etc.).
2. Execute the main notebook `ETLProject.ipynb` where the following is performed:
   * Data extraction from CSV files.
   * Loading to SQLite database.
   * Execution of transformation queries.
   * Results visualization.
3. Verify that tables and results are generated correctly in the database.

## Orchestration with Apache Airflow using Docker

To automate the pipeline using Airflow:

### Prerequisites

* Have Docker Desktop installed and running.
* Clone this repository and navigate to the `airflow` folder.

### Configuration

1. Generate a Fernet key and update it in `docker-compose.yml`:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

2. Place the generated key in the `AIRFLOW__CORE__FERNET_KEY` variable inside the `docker-compose.yml` file.

### Initialization and Deployment

1. Initialize the Airflow database and create an administrator user:

```bash
docker compose run airflow-webserver airflow db init
docker compose run airflow-webserver airflow users create --username admin --firstname Admin --lastname User --role Admin --email admin@example.com --password admin
docker compose run airflow-webserver pip install -r /requirements.txt
```

2. Start the scheduler and Airflow web server:

```bash
docker compose up airflow-webserver airflow-scheduler
```

### Usage

1. Open the Airflow web interface at:

```text
http://localhost:8080
```

2. Log in with the created credentials (username: `admin`, password: `admin`).
3. Activate the `elt_pipeline` DAG and run it manually or schedule automatic executions.
4. Monitor task status and review logs in the interface.

## Final Comments

* The orchestration reuses the original pipeline code without modifying it, ensuring that tests continue to work.
* For visualization and results analysis, use the main `ETLProject.ipynb` notebook.
* The project includes unit tests in the `tests/` directory to ensure code quality and reliability.
* You can extend the Airflow DAG or integrate it into more complex workflows if desired.

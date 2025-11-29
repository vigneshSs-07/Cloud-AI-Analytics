# Automate Google Cloud SQL PostgreSQL with Terraform and Python (Step‑by‑Step)

This project demonstrates how to provision a production-ready Google Cloud SQL for PostgreSQL instance using Terraform and how to interact with it using a simple Python application.

## Table of Contents

- [Project Overview](#project-overview)
- [Infrastructure Details (Terraform)](#infrastructure-details-terraform)
- [Python Application](#python-application)
- [Prerequisites](#prerequisites)
- [Deployment Steps](#deployment-steps)
- [Running the Python Application](#running-the-python-application)
- [Cleanup](#cleanup)

## Project Overview

This repository contains two main components:

1.  **Terraform Configuration**: Code to define, create, and manage a high-availability Google Cloud SQL for PostgreSQL instance.
2.  **Python Script**: A sample application that connects to the provisioned database, creates a table, inserts data, and queries it.

## Infrastructure Details (Terraform)

The Terraform code in the `terraform/` directory provisions the following Google Cloud resources:

- **Google Project Services**: Enables necessary APIs for the project to function:
  - `sqladmin.googleapis.com`
  - `compute.googleapis.com`
  - `servicenetworking.googleapis.com`

- **Google Cloud SQL Instance (`google_sql_database_instance`)**: A fully configured PostgreSQL 15 instance with the following production-grade features:
  - **Edition**: `ENTERPRISE` edition for robust features.
  - **High Availability**: `REGIONAL` availability to withstand zonal failures.
  - **Machine Type**: `db-custom-1-3840` (1 vCPU, 3.8 GB RAM).
  - **Automated Backups**: Daily backups with a 30-day retention policy and Point-in-Time Recovery enabled.
  - **Maintenance Window**: Scheduled for low-traffic periods (Sunday, 3 AM UTC).
  - **Monitoring**: Query Insights are enabled to help diagnose performance issues.
  - **Storage**: Starts with 10 GB of SSD storage with auto-resizing enabled.
  - **Networking**: Configured with a public IP and an authorized network to allow connections from a specific IP address.
  - **Labels**: Resources are tagged with `environment`, `owner`, and `managed-by` for better organization and cost tracking.

- **SQL Database (`google_sql_database`)**: Creates a database named `appdb` within the instance.

- **SQL User (`google_sql_user`)**: Creates a user named `appuser` to be used by the application.

### Configuration

The infrastructure is configurable via `variables.tf`. Key variables include:
- `project_id`: Your Google Cloud project ID.
- `region`: The GCP region for deployment.
- `database_name`, `db_user`, `db_password`: Credentials for the database.
- `my_public_ip`: Your public IP address, required to authorize your connection to the database.

## Python Application

The `python/main.py` script performs the following actions:

1.  **Connects** to the PostgreSQL database using the `psycopg2` library.
2.  **Creates a Table**: Defines and creates an `employees_2` table if it doesn't already exist.
3.  **Inserts Data**: Populates the table with sample employee records.
4.  **Queries Data**: Fetches and prints all records from the `employees_2` table.

**Note**: The script currently contains hardcoded credentials. For a real-world application, these should be externalized using environment variables or a secret management system.

## Prerequisites

- Terraform CLI installed.
- Google Cloud SDK installed and configured.
- Python 3 and `pip` installed.
- A Google Cloud Project with billing enabled.

## Deployment Steps

1.  **Clone the repository.**

2.  **Authenticate with Google Cloud:**
    ```sh
    gcloud auth application-default login
    ```

3.  **Configure Terraform Variables:**
    Create a `terraform.tfvars` file in the `terraform/` directory and populate it with your specific values.
    ```hcl
    project_id   = "your-gcp-project-id"
    my_public_ip = "your.public.ip.address/32"
    db_password  = "a-strong-and-secret-password"
    ```

4.  **Deploy the Infrastructure:**
    Navigate to the `terraform/` directory and run the following commands:
    ```sh
    terraform init
    terraform apply
    ```
    Review the plan and type `yes` to confirm.

## Running the Python Application

1.  **Install Dependencies:**
    Navigate to the `python/` directory and install the required library:
    ```sh
    pip install psycopg2-binary
    ```

2.  **Update Connection Details:**
    In `python/main.py`, update the `DB_HOST` with the public IP address of your newly created Cloud SQL instance. You can find this in the Terraform output or the GCP Console. Update `DB_PASS` to match the password you set in `terraform.tfvars`.

3.  **Run the script:**
    ```sh
    python main.py
    ```

## Cleanup

To avoid ongoing charges, destroy the infrastructure when you are finished.

1.  Navigate to the `terraform/` directory.
2.  Run the destroy command:
    ```sh
    terraform destroy
    ```
    Type `yes` to confirm the deletion of all created resources.

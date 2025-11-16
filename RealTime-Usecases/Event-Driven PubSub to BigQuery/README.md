# README.md

## Event-Driven Pipeline: Pub/Sub → Cloud Functions (Gen2) → BigQuery (with DLQ)

This repository contains a complete, production-ready **event-driven
data ingestion pipeline** built on **Google Cloud** using:

-   **Pub/Sub** as event ingestion
-   **Cloud Functions (Gen2)** via an Eventarc trigger as the processing layer
-   **BigQuery** as the data destination
-   **Dead-Letter Queue (DLQ)** for failed processing
-   **Terraform** to deploy all infrastructure

The Cloud Function is written in **Python** and automatically retries
failed inserts. Pub/Sub redirects permanently failed messages to a DLQ
after the configured max retry attempts.

------------------------------------------------------------------------

# Components

## 1. Pub/Sub Topic

Name: `events-topic`

## 2. Cloud Function (Gen2)

The function processes Pub/Sub messages and inserts them into BigQuery. It is configured to retry on failure.

## 3. BigQuery Dataset & Table

The dataset and table are created via Terraform to store the ingested events.

| Column        | Type      | Mode     | Description                  |
| Column        | Type      | Mode     |
| ------------- | --------- | -------- |
| `id`          | STRING    | REQUIRED |
| `payload`     | STRING    | NULLABLE |
| `received_at` | TIMESTAMP | REQUIRED |


## 4. Dead-Letter Queue (DLQ)

Topic: `events-topic-dlq`
This topic receives messages that fail processing repeatedly in the Cloud Function.

## 5. Terraform

The Terraform code in this repository automates the deployment of all the resources mentioned above.

## File Structure
.
├── main.tf
├── variables.tf
├── provider.tf
├── outputs.tf
├── terraform.tfvars (optional)
├── function/
│   ├── main.py
│   └── requirements.txt
├── sample_message.json
└── README.md


------------------------------------------------------------------------

# Deployment Instructions

## Prerequisites

Install Terraform, gcloud CLI, and Python 3.11. Authenticate using:

    gcloud auth login
    gcloud auth application-default login

## Configure Variables

Create `terraform.tfvars`:

    project_id = "your-project-id"
    region     = "us-central1"
    location   = "US"

## Deploy

    terraform init
    terraform apply

Terraform will:

✔ Enable required APIs
✔ Create Pub/Sub topic
✔ Create DLQ topic
✔ Create Pub/Sub subscription with dead_letter_policy
✔ Create BigQuery dataset/table
✔ Upload Cloud Function source to GCS
✔ Deploy Cloud Functions Gen2 with Eventarc trigger


Cloud Function Code

Located in function/main.py.

Summary:

Decodes Pub/Sub event

Attempts BigQuery insert

Raises exception on failure → Pub/Sub retries

After max attempts → DLQ topic

------------------------------------------------------------------------

# Sample Message

    {
      "id": "evt-10001",
      "type": "order_created",
      "source": "checkout_service",
      "timestamp": "2025-01-15T12:34:56Z",
      "customer": {
        "customer_id": "CUST-9001",
        "name": "Jane Smith",
        "email": "jane.smith@example.com"
      },
      "order": {
        "order_id": "ORD-56789",
        "total_amount": 249.75,
        "currency": "USD",
        "items": [
          {
            "sku": "SKU-001",
            "product_name": "Laptop Backpack",
            "quantity": 1,
            "unit_price": 49.75
          },
          {
            "sku": "SKU-002",
            "product_name": "Noise Cancelling Headphones",
            "quantity": 1,
            "unit_price": 200.00
          }
        ]
      },
      "metadata": {
        "request_id": "req-001-xyz",
        "ip_address": "203.0.113.50"
      }
    }

------------------------------------------------------------------------

# DLQ Behavior

After repeated failures, Pub/Sub sends messages to `events-topic-dlq`.

------------------------------------------------------------------------

# Cleanup

    terraform destroy

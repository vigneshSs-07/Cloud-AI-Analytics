# Real-Time Event-Driven Pipeline: Cloud Storage to BigQuery with Cloud Run Functions (Gen2)

An event-driven **Cloud Run Function (Gen 2)** that automatically loads Avro files into BigQuery whenever a file is uploaded to a Cloud Storage bucket.

---

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [How the Internal Call Flow Works](#how-the-internal-call-flow-works)
- [Project Structure](#project-structure)
- [Google Cloud Services Used](#google-cloud-services-used)
- [Prerequisites](#prerequisites)
- [Deployment](#deployment)
- [Testing](#testing)
- [Cleanup](#cleanup)
- [Configuration Details](#configuration-details)

---

## Architecture Overview

```
┌─────────────┐      upload       ┌─────────────┐    event     ┌─────────────┐
│  User /      │ ──────────────▶  │  Cloud       │ ──────────▶ │  Cloud Run  │
│  Pipeline    │  campaigns.avro  │  Storage     │  finalize   │  Function   │
└─────────────┘                   │  (GCS)       │             │  (Gen 2)    │
                                  └─────────────┘             └──────┬──────┘
                                                                     │
                                                               load_table_from_uri
                                                                     │
                                                                     ▼
                                                              ┌─────────────┐
                                                              │  BigQuery   │
                                                              │  Dataset:   │
                                                              │  loadavro   │
                                                              └─────────────┘
```

---

## How the Internal Call Flow Works

When an Avro file is uploaded to GCS, the following chain of events happens internally:

### Step 1 — File Upload to GCS

A file (e.g. `campaigns.avro`) is uploaded to the GCS bucket `gs://<PROJECT_ID>`. This can be done manually, via `gcloud storage cp`, or from an automated pipeline.

### Step 2 — GCS Emits a `google.storage.object.finalize` Event

Cloud Storage detects that a new object has been created (or an existing one overwritten) and emits an **object finalize** event. This event contains a JSON payload with metadata:

```json
{
  "bucket": "<PROJECT_ID>",
  "name": "campaigns.avro",
  "contentType": "application/avro",
  "size": "12345",
  "timeCreated": "2026-04-16T10:00:00.000Z"
}
```

### Step 3 — Eventarc Routes the Event via Pub/Sub

Behind the scenes, GCS does **not** call the function directly. Instead:

1. The **GCS service agent** (`service-<PROJECT_NUMBER>@gs-project-accounts.iam.gserviceaccount.com`) publishes a message to a **Pub/Sub topic** that Eventarc manages automatically.
2. **Eventarc** picks up the Pub/Sub message and routes it to the Cloud Run service backing the function.
3. This is why the GCS service agent needs the `roles/pubsub.publisher` role, and the Eventarc service agent needs `roles/eventarc.serviceAgent`.

### Step 4 — Cloud Run Function Is Invoked

The function `load_bigquery_from_avro(event, context)` in `main.py` is called with:

- **`event`** — a dict containing `bucket` and `name` from the GCS event payload.
- **`context`** — metadata about the event (event ID, timestamp, event type).

### Step 5 — BigQuery Load Job Is Created

Inside the function:

1. The **bucket name** and **file name** are extracted from the event.
2. The **table name** is derived from the file name by stripping the `.avro` extension (e.g. `campaigns.avro` → `campaigns`).
3. A `BigQuery.Client()` is initialised (uses the function's service account credentials automatically).
4. A **load job** is configured with:
   - `source_format = AVRO` — tells BigQuery to parse Avro format.
   - `autodetect = True` — schema is inferred from the Avro file's embedded schema.
   - `create_disposition = CREATE_IF_NEEDED` — creates the table if it doesn't exist.
   - `write_disposition = WRITE_TRUNCATE` — overwrites the table on each load.
5. `load_table_from_uri()` sends a request to the **BigQuery Jobs API** (`bigquery.jobs.insert`) with the GCS URI (`gs://bucket/file.avro`).

### Step 6 — BigQuery Reads Directly from GCS

BigQuery does **not** download the file through the function. Instead:

1. The load job tells BigQuery's internal infrastructure to read directly from `gs://<bucket>/<file>`.
2. BigQuery's distributed workers parse the Avro file, infer the schema, and write the data into the target table.
3. The function calls `load_job.result()` which blocks (polls the Jobs API) until the load job completes.

### Step 7 — Completion

Once BigQuery finishes loading, the function logs the job ID and exits. If anything fails, the error is logged and the exception is re-raised (Cloud Run will record it as a failed invocation).

```
                                    Internal Call Flow
                                    ==================

User uploads file to GCS
        │
        ▼
GCS detects object.finalize
        │
        ▼
GCS Service Agent publishes to Pub/Sub topic (managed by Eventarc)
        │
        ▼
Eventarc routes the event to Cloud Run (Gen 2) service
        │
        ▼
Cloud Run invokes load_bigquery_from_avro(event, context)
        │
        ▼
Function calls BigQuery Jobs API → load_table_from_uri(gs://...)
        │
        ▼
BigQuery workers read Avro file DIRECTLY from GCS (not through the function)
        │
        ▼
Data is written to BigQuery table: loadavro.<filename>
        │
        ▼
Function receives job completion → logs success
```

---

## Project Structure

```
Cloud Run Functions to Load BigQuery/
├── main.py              # Python Cloud Run Function (entry point)
├── requirements.txt     # Python dependencies (installed during deployment)
├── run.sh               # Deployment script (creates all resources)
├── cleanup.sh           # Teardown script (deletes all resources)
├── campaigns.avro       # Sample Avro file for testing
└── README.md            # This file
```

| File | Purpose |
|---|---|
| `main.py` | Contains `load_bigquery_from_avro()` — the function that loads Avro files from GCS into BigQuery. |
| `requirements.txt` | Lists `google-cloud-bigquery` and `google-cloud-storage` as dependencies. |
| `run.sh` | End-to-end deployment: enables APIs, configures IAM, creates bucket/dataset, deploys function, and uploads a test file. |
| `cleanup.sh` | Deletes the function, triggers, dataset, bucket, and Artifact Registry repos. Preserves service accounts. |

---

## Google Cloud Services Used

| Service | Role |
|---|---|
| **Cloud Run Functions (Gen 2)** | Hosts the Python function. Gen 2 functions run on Cloud Run under the hood. |
| **Cloud Storage (GCS)** | Stores the Avro files. Emits `object.finalize` events on upload. |
| **BigQuery** | Destination for the loaded data. Runs the load job server-side. |
| **Eventarc** | Routes GCS events to the Cloud Run Function via Pub/Sub. |
| **Pub/Sub** | Message bus between GCS and Eventarc (managed automatically). |
| **Cloud Build** | Builds the function's container image during deployment. |
| **Artifact Registry** | Stores the built container image (`gcf-artifacts` repository). |

---

## Prerequisites

- A Google Cloud project with billing enabled.
- `gcloud` CLI installed and authenticated (`gcloud auth login`).
- The following roles on your account:
  - `roles/owner` or a combination of `roles/cloudfunctions.admin`, `roles/iam.serviceAccountAdmin`, `roles/storage.admin`, `roles/bigquery.admin`.

---

## Deployment

Run the deployment script in **Cloud Shell** or any terminal with `gcloud` configured:

```bash
bash run.sh
```

The script performs the following steps in order:

1. **Sets project and region** configuration variables.
2. **Enables required APIs** — Cloud Functions, Cloud Build, Eventarc, Cloud Run, Pub/Sub, Logging, Artifact Registry.
3. **Configures IAM permissions**:
   - Grants `roles/eventarc.eventReceiver` to the default Compute Engine service account.
   - Provisions and grants `roles/pubsub.publisher` to the GCS service agent.
   - Provisions and grants `roles/eventarc.serviceAgent` to the Eventarc service agent.
4. **Installs Python dependencies** locally (optional, for Cloud Shell testing).
5. **Creates a GCS bucket** (`gs://<PROJECT_ID>`) and a **BigQuery dataset** (`loadavro`).
6. **Deploys the Cloud Run Function** (Gen 2, Python 3.12, 512Mi memory, 540s timeout).
7. **Verifies the Eventarc trigger** was created.
8. **Uploads a test Avro file** to the bucket to trigger the function.

---

## Testing

After deployment, verify the data loaded into BigQuery:

```sql
SELECT * FROM loadavro.campaigns LIMIT 10;
```

You can also upload additional Avro files to trigger the function:

```bash
gcloud storage cp my_other_file.avro gs://$PROJECT_ID
```

This will create a new table `loadavro.my_other_file` in BigQuery.

To check function logs:

```bash
gcloud functions logs read load_bigquery_from_avro --region=us-central1 --gen2
```

---

## Cleanup

To delete all created resources (except service accounts and IAM bindings):

```bash
bash cleanup.sh
```

This removes:
- Cloud Run Function
- Eventarc triggers
- BigQuery dataset `loadavro` (and all tables)
- GCS bucket `gs://<PROJECT_ID>` (and all objects)
- Artifact Registry `gcf-artifacts` repository
- Local `campaigns.avro` file

---

## Configuration Details

| Parameter | Value | Description |
|---|---|---|
| Region | `us-central1` | Deployment region for all resources |
| Runtime | `python312` | Python 3.12 |
| Memory | `512Mi` | Function memory allocation |
| Timeout | `540s` | Maximum execution time (9 minutes) |
| Trigger event | `google.storage.object.finalize` | Fires when a file is created/overwritten in GCS |
| BigQuery dataset | `loadavro` | Target dataset for all loaded tables |
| Write disposition | `WRITE_TRUNCATE` | Overwrites the table on each load |
| Source format | `AVRO` | Apache Avro binary format |
| Schema detection | `autodetect` | Inferred from the Avro file's embedded schema |

import base64
import json
import os
from datetime import datetime, timezone
from google.cloud import bigquery
from functions_framework import cloud_event

PROJECT_ID = os.environ.get("PROJECT_ID") 
BQ_DATASET = os.environ.get("BQ_DATASET")
BQ_TABLE = os.environ.get("BQ_TABLE")

bq = bigquery.Client()

@cloud_event
def pubsub_to_bq(event):
    data = event.data or {}

    if "message" not in data:
        raise ValueError("Missing 'message' in CloudEvent data")

    message = data["message"]
    if "data" not in message:
        raise ValueError("Missing 'data' in Pub/Sub message")

    # Decode
    decoded = base64.b64decode(message["data"]).decode("utf-8")

    # Try parse JSON
    try:
        payload_json = json.loads(decoded)
    except:
        payload_json = None

    # Extract row_id from JSON if available
    if isinstance(payload_json, dict) and "id" in payload_json:
        row_id = payload_json["id"]

    # Otherwise use CloudEvent ID
    else:
        # CloudEvent ID is at event["id"]
        row_id = event["id"]

    # Prepare row
    rows = [{
        "id": str(row_id),
        "payload": decoded,
        "received_at": datetime.now(timezone.utc).isoformat()
    }]

    table_id = f"{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}"
    errors = bq.insert_rows_json(table_id, rows)

    if errors:
        raise RuntimeError(f"BigQuery insert failed: {errors}")

    return "OK"


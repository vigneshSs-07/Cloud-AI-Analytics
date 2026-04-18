# =============================================================================
# main.py — Cloud Run Function: Load Avro files from GCS into BigQuery
#
# Trigger : google.storage.object.finalize (fires when a file is uploaded to GCS)
# Runtime : Python 3.12
# Entry   : load_bigquery_from_avro
# =============================================================================

from google.cloud import bigquery


def load_bigquery_from_avro(event, context):
    """Triggered by a GCS event to load an Avro file into BigQuery.

    Args:
        event  (dict): GCS event payload containing 'bucket' and 'name' keys.
        context (google.cloud.functions.Context): Event metadata (id, timestamp, etc.).
    """
    try:
        # Extract the bucket name and file name from the GCS event payload
        bucket_name = event["bucket"]
        file_name = event["name"]

        # Target BigQuery dataset and table
        # Table name is derived from the file name (e.g. campaigns.avro -> campaigns)
        dataset_id = "loadavro"
        table_id = file_name.replace(".avro", "")

        # Initialise the BigQuery client and build the table reference
        client = bigquery.Client()
        table_ref = client.dataset(dataset_id).table(table_id)

        # Configure the load job
        #   - AVRO source format
        #   - autodetect: infer schema from the Avro file
        #   - CREATE_IF_NEEDED: create the table if it does not exist
        #   - WRITE_TRUNCATE: overwrite the table on each load
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.AVRO,
            autodetect=True,
            create_disposition=bigquery.CreateDisposition.CREATE_IF_NEEDED,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        )

        # Build the GCS URI and start the load job
        uri = f"gs://{bucket_name}/{file_name}"
        load_job = client.load_table_from_uri(uri, table_ref, job_config=job_config)

        # Block until the job completes
        load_job.result()

        print(f"Job {load_job.job_id} completed. Created table {table_id}.")

    except Exception as e:
        print(f"Error loading data into BigQuery: {e}")
        raise
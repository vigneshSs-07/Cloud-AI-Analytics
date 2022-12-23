from google.auth import compute_engine
from google.cloud import bigquery
SERVICE_ACCOUNT_JSON=r'/home/cloudaianalytics/BigQuery/sravanitest-ac41e3dc16ee.json'

client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_JSON)
bucket_name = 'bqdemogcp-pde' 
project = "sravanitest"
dataset_id = "demogcp_pde"
table_id = "clusteringdemo" #gs://bqdemogcp-pde/clustering.csv

destination_uri = "gs://{}/clustering.csv".format(bucket_name)
dataset_ref = bigquery.DatasetReference(project, dataset_id)
table_ref = dataset_ref.table(table_id)
print("****", table_ref)

extract_job = client.extract_table(
    table_ref,
    destination_uri,
    # Location must match that of the source table.
    location="us-central1",
)  # API request
extract_job.result()  # Waits for job to complete.
print("Data is Exported")

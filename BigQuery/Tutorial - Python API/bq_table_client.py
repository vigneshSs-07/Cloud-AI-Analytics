#Tutorial 1 - List of Operations in Google BigQuery Tables - Python Client
from google.cloud import bigquery
SERVICE_ACCOUNT_JSON=r'/home/cloudaianalytics/BigQuery/sravanitest-ac41e3dc16ee.json'


def create_table(table_id):
    # Construct a BigQuery client object.
    client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_JSON)

    schema=[
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("gender", "STRING"),
		bigquery.SchemaField("count", "INTEGER")
    ]

    table = bigquery.Table(table_id, schema=schema)
    table = client.create_table(table)  # Make an API request.
    print(
        "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
    )
    

def load_table_to_bq(table_id):
    # Construct a BigQuery client object.
    client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_JSON)

    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("name", "STRING"),
            bigquery.SchemaField("gender", "STRING"),
            bigquery.SchemaField("count", "INTEGER")
        ],
        source_format=bigquery.SourceFormat.CSV, skip_leading_rows=1, autodetect=True,
    )
    file_path=r'/home/cloudaianalytics/BigQuery/yob2014.txt'
    source_file = open(file_path, "rb")
    job = client.load_table_from_file(source_file, table_id, job_config=job_config)

    job.result()  # Waits for the job to complete.

    table = client.get_table(table_id)  # Make an API request.
    print("Loaded {} rows and table is {}".format(table.num_rows, table_id))



def get_table(table_id):
    # Construct a BigQuery client object.
    client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_JSON)

    table = client.get_table(table_id)  # Make an API request.

    # View table properties
    print("Got table '{}.{}.{}'.".format(table.project, table.dataset_id, table.table_id))
    print("Table schema: {}".format(table.schema))
    print("Table description: {}".format(table.description))
    print("Table has {} rows".format(table.num_rows))
    


def list_tables(dataset_id):
    # Construct a BigQuery client object.
    client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_JSON)

    tables = client.list_tables(dataset_id)  # Make an API request.

    print("Tables contained in '{}':".format(dataset_id))
    for table in tables:
        print("{}.{}.{}".format(table.project, table.dataset_id, table.table_id))


def delete_table(table_id):
    # Construct a BigQuery client object.
    client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_JSON)

    
    client.delete_table(table_id, not_found_ok=True)  # Make an API request.
    print("Deleted table '{}'.".format(table_id))

if __name__ == "__main__":
    table_id="sravanitest.learngcppde.table_demo2"
    dataset_id="sravanitest.learngcppde"
    #create_table(table_id)
    #load_table_to_bq(table_id)
    #get_table(table_id)
    #list_tables(dataset_id)
    delete_table(table_id)

    
#Tutorial 1 - List of Operations in Google BigQuery Dataset - Python Client 
from google.cloud import bigquery
from google.cloud.exceptions import NotFound
SERVICE_ACCOUNT_JSON=r'/home/cloudaianalytics/BigQuery/sravanitest-ac41e3dc16ee.json'

def create_dataset(client,dataset_id):

    dataset = bigquery.Dataset(dataset_id)
    dataset.location = "us-east1"
    dataset = client.create_dataset(dataset)  
    print("Created dataset {}.{}".format(client.project, dataset.dataset_id))


def create_table(client,table_id):
    
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


def list_datasets(client):

    datasets = list(client.list_datasets())  
    project = client.project

    if datasets:
        print("Datasets in project {}:".format(project))
        for dataset in datasets:
            print("\t{}".format(dataset.dataset_id))
    else:
        print("{} project does not contain any datasets.".format(project))  


def label_dataset(client,dataset_id):
    
    dataset = client.get_dataset(dataset_id)  
    dataset.labels = {"learning": "learning_dataset_withvignesh"}
    dataset = client.update_dataset(dataset, ["labels"])  
    print("Labels added to {}".format(dataset_id))
    

def get_dataset(client,dataset_id):
    
    dataset = client.get_dataset(dataset_id)  

    full_dataset_id = "{}.{}".format(dataset.project, dataset.dataset_id)
    friendly_name = dataset.friendly_name
    print(
        "Got dataset '{}' with friendly_name '{}'.".format(
            full_dataset_id, friendly_name
        )
    )

    # View dataset properties.
    print("Description: {}".format(dataset.description))
    print("Labels:")
    labels = dataset.labels
    if labels:
        for label, value in labels.items():
            print("\t{}: {}".format(label, value))
    else:
        print("\tDataset has no labels defined.")

    # View tables in dataset.
    create_table(client,"sravanitest.learndemo_dataset_gcp.demo_table") # developing from scratch
    print("Tables:")
    tables = list(client.list_tables(dataset))  # Make an API request(s).
    if tables:
        for table in tables:
            print("\t{}".format(table.table_id))
    else:
        print("\tThis dataset does not contain any tables.")
   


def get_dataset_labels(client,dataset_id):
    
    dataset = client.get_dataset(dataset_id)  

    # View dataset labels.
    print("Dataset ID: {}".format(dataset_id))
    print("Labels:")
    if dataset.labels:
        for label, value in dataset.labels.items():
            print("\t{}: {}".format(label, value))
    else:
        print("\tDataset has no labels defined.")
   

def delete_dataset(client,ataset_id):
    
    client.delete_dataset(
        dataset_id, delete_contents=True, not_found_ok=True
    )  

    print("Deleted dataset '{}'.".format(dataset_id))
    
if __name__ == "__main__":
    client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_JSON)
    print("*****", client.project)
    dataset_id ="{}.learndemo_dataset_gcp".format(client.project)
    create_dataset(client,dataset_id)
    list_datasets(client)
    label_dataset(client,dataset_id)
    get_dataset(client,dataset_id)
    get_dataset_labels(client,dataset_id)
    delete_dataset(client,dataset_id)
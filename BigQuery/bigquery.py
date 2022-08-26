#import libraries
from google.cloud import bigquery
from google.cloud.exceptions import NotFound


#Function to create a dataset in Bigquery
def bq_create_dataset(client, dataset):
    dataset_ref = bigquery_client.dataset(dataset)

    try:
        dataset = bigquery_client.get_dataset(dataset_ref)
        print('Dataset {} already exists.'.format(dataset))
    except NotFound:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = 'US'
        dataset = bigquery_client.create_dataset(dataset)
        print('Dataset {} created.'.format(dataset.dataset_id))
    return dataset

#Function to create a dataset in Table
def bq_create_table(client, dataset, table_name):
    dataset_ref = bigquery_client.dataset(dataset)

    # Prepares a reference to the table
    table_ref = dataset_ref.table(table_name)

    try:
        table =  bigquery_client.get_table(table_ref)
        print('table {} already exists.'.format(table))
    except NotFound:
        schema = [
            bigquery.SchemaField('S_No', 'INTEGER', mode='REQUIRED'),
            bigquery.SchemaField('Age_in_cm', 'INTEGER', mode='REQUIRED'),
            bigquery.SchemaField('Weight_in_Kg', 'INTEGER', mode='REQUIRED'),
            bigquery.SchemaField('Name', 'STRING', mode='REQUIRED'),
        ]
        table = bigquery.Table(table_ref, schema=schema)
        table = bigquery_client.create_table(table)
        print('table {} created.'.format(table.table_id))
    return table

#Function to export data into table in Bigquery
def export_items_to_bigquery(client, dataset, table):    

    # Prepares a reference to the dataset
    dataset_ref = bigquery_client.dataset(dataset)

    table_ref = dataset_ref.table(table)
    table = bigquery_client.get_table(table_ref)  # API call

    rows_to_insert = [
        (1, 32, 32, "Harry"),
        (2, 64, 29, "Ron"),
        (3, 108, 108, "Hermonie")
    ]
    errors = bigquery_client.insert_rows(table, rows_to_insert)  # API request
    assert errors == []

if __name__ == "__main__":
    #creating bigquery object
    bigquery_client = bigquery.Client()
    dataset = "demo_dataset"
    table_name = "demo_table"
    data = bq_create_dataset(bigquery_client, dataset)
    table = bq_create_table(bigquery_client, dataset, table_name)
    export_items_to_bigquery(bigquery_client, dataset, table_name) #it should not be assigned, since this method is not returning anything

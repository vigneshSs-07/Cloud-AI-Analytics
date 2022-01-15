from google.cloud import bigquery
#Creating an instance for bigquery client
client = bigquery.Client()

#View location to be stored
view_id = "datalab-336505.demodata.02cancer_view"
#Source table location
source_id = "datalab-336505.demodata.cancer"

#https://googleapis.dev/python/bigquery/latest/generated/google.cloud.bigquery.table.Table.html?highlight=bigquery%20table#google.cloud.bigquery.table.Table
view = bigquery.Table(view_id)
# SQL query defining the table as a view (defaults to None).
view.view_query = f"SELECT mean_radius,mean_texture,mean_perimeter,target FROM `{source_id}` limit 10 "
# https://googleapis.dev/python/bigquery/latest/generated/google.cloud.bigquery.client.Client.html?highlight=create_table#google.cloud.bigquery.client.Client.create_table
view = client.create_table(view)

# Make an API request to create the view.
if __name__ == "__main__":    
    print(f"Created {view.table_type}: {str(view.reference)}")

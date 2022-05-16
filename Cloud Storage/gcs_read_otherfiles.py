import google.auth
from google.cloud import storage
import json
import pandas as pd

credentials, project = google.auth.default()  
#List buckets using the default account on the current gcloud cli
client = storage.Client(credentials=credentials)
buckets = client.list_buckets()
for bucket in buckets:
    print(bucket)

#custom function to read data from cvs/sql/excel/xml file
def read_file_gcs(bucket_name, general_file_name):
    """
    Read a file from the bucket
    """

    # create storage client
    client = storage.Client()
    # get bucket with name
    BUCKET= client.get_bucket(bucket_name)
    # get bucket data as blob
    blob = BUCKET.blob(general_file_name)
    assert blob.exists()  # Will be false if the next line would raise NotFound
    # convert to string
    data = blob.download_as_string()
    return data

bucket_name = "demo_bucket_97"
general_file_name = "sample.yml"  #cloudsql/table_creation.sql  sample.yml
data = read_file_gcs(bucket_name, general_file_name)
print(data)

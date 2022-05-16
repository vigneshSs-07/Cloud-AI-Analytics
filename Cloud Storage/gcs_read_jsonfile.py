import google.auth
from google.cloud import storage
import json

credentials, project = google.auth.default()  
#List buckets using the default account on the current gcloud cli
client = storage.Client(credentials=credentials)
buckets = client.list_buckets()
for bucket in buckets:
    print(bucket)

#custom function to read data in json file
def get_json_gcs(bucket_name, file_name):
    # create storage client
    client = storage.Client()
    # get bucket with name
    BUCKET = client.get_bucket(bucket_name)

    # get the blob
    blob = BUCKET.get_blob(file_name)

    # load blob using json
    file_data = json.loads(blob.download_as_string())
    return file_data

bucket_name = "demo_bucket_97"
file_name = "Sample.json"
json_data = get_json_gcs(bucket_name, file_name)
print(json_data)
print(json_data['firstName'])
print(json_data['phoneNumbers'])
import json

def get_json(bucket, file_name):
    """ Read contents in config.json file across environment.
    input parameters::
        bucket: Name of the GCS bucket
        ENV: Name of the env
    output paramters::
        returns: dataproc cluster parameters.
    """ 

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket)
    blob = bucket.blob(file_name)
    data = json.loads(blob.download_as_string())
    return data
  
  if __name__=="__main__":
    bucket = ""
    file_name = ""
    data = get_json(bucket, file_name)

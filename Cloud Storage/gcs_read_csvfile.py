import google.auth
from google.cloud import storage
import pandas as pd

#requirements.txt
# google-cloud-storage==1.30.0
# gcsfs==0.6.2   pip3 install gcsfs
# pandas==1.1.0  pip3 install pandas
# fsspec              pip3 install fsspec

#custom function to read data in json file
def get_csv_gcs(bucket_name, file_name):
    csv_data = pd.read_csv('gs://' + bucket_name + '/' + file_name, encoding='utf-8')  
    # csv_data = pd.read_excel('gs://' + bucket_name + '/' + file_name, encoding='utf-8')    
    return csv_data

bucket_name = "demo_bucket_97"
file_name = "earthquakes.csv"
csv_data = get_csv_gcs(bucket_name, file_name)
print(csv_data.head(5))

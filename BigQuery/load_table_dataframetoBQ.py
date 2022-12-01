#import libraries - HOW TO LOAD DATAFRAME(DATA) TO BIG QUERY TABLE USING PYTHON CLIENT LIBRARY
import datetime
from google.cloud import bigquery
import pandas
import pytz
from google.oauth2 import service_account

key_path= "/home/cloudaianalytics/BigQuery/sravanitest-ac41e3dc16ee.json"
project_id="sravanitest"
dataset_id = "learngcppde"
table="wikidata"
table_id="{}.{}.{}".format(project_id, dataset_id, table)
print("********* NAME OF TABLE IS", table_id)

def load_table_dataframe(key_path,project_id,table_id):
    credentials = service_account.Credentials.from_service_account_file(
        key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )

    # Construct a BigQuery client object.
    client = bigquery.Client(credentials=credentials, project=project_id)

    records = [
        {
            "title": u"The Meaning of Life",
            "release_year": 1983,
            "length_minutes": 112.5,
            "release_date": pytz.timezone("Europe/Paris")
            .localize(datetime.datetime(1983, 5, 9, 13, 0, 0))
            .astimezone(pytz.utc),
            # Assume UTC timezone when a datetime object contains no timezone.
            "dvd_release": datetime.datetime(2002, 1, 22, 7, 0, 0),
        },
        {
            "title": u"Monty Python and the Holy Grail",
            "release_year": 1975,
            "length_minutes": 91.5,
            "release_date": pytz.timezone("Europe/London")
            .localize(datetime.datetime(1975, 4, 9, 23, 59, 2))
            .astimezone(pytz.utc),
            "dvd_release": datetime.datetime(2002, 7, 16, 9, 0, 0),
        },
        {
            "title": u"Life of Brian",
            "release_year": 1979,
            "length_minutes": 94.25,
            "release_date": pytz.timezone("America/New_York")
            .localize(datetime.datetime(1979, 8, 17, 23, 59, 5))
            .astimezone(pytz.utc),
            "dvd_release": datetime.datetime(2008, 1, 14, 8, 0, 0),
        },
        {
            "title": u"And Now for Something Completely Different",
            "release_year": 1971,
            "length_minutes": 88.0,
            "release_date": pytz.timezone("Europe/London")
            .localize(datetime.datetime(1971, 9, 28, 23, 59, 7))
            .astimezone(pytz.utc),
            "dvd_release": datetime.datetime(2003, 10, 22, 10, 0, 0),
        },
    ]
    dataframe = pandas.DataFrame(
        records,
        # In the loaded table, the column order reflects the order of the
        # columns in the DataFrame.
        columns=[
            "title",
            "release_year",
            "length_minutes",
            "release_date",
            "dvd_release",
        ],
    )
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE")

    job = client.load_table_from_dataframe(
        dataframe, table_id, job_config=job_config
    )  
    job.result()  

    data = client.get_table(table_id)  
    return data

data = load_table_dataframe(key_path,project_id, table_id)


def load_table_dataframe_config(key_path,project_id,table_id, data):
    credentials = service_account.Credentials.from_service_account_file(
        key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )

    # Construct a BigQuery client object.
    client = bigquery.Client(credentials=credentials, project=project_id)

    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE")

    job = client.load_table_from_dataframe(
        data, table_id, job_config=job_config
    )  
    job.result()  

    data = client.get_table(table_id)  
    return data
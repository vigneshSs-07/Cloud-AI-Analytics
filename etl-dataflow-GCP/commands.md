This example reads a json schema of the intended output into BigQuery and transforms the date data to match the format BigQuery expects.

### Commands:

1. Make Sure API for BigQuery, CLoud Storage and Cloud Dataflow Services are enabled.
2. Activate Cloud Shell
3. Activate account with this command
    a. gcloud auth list
4. List the project ID with this command
    a. gcloud config list project
5. Now set a variable equal to your project id:
    a. export PROJECT='theta-device-359600'


### Create Cloud Storage Bucket

1. Create a Standard Storage Class bucket
    a. gsutil mb -c standard -l us-east1 gs://$PROJECT
2. Copy Files to Your Bucket
    a. gsutil cp gs://spls/gsp290/data_files/usa_names.csv gs://$PROJECT/data_files/
    b. gsutil cp gs://spls/gsp290/data_files/head_usa_names.csv gs://$PROJECT/data_files/


### Create the BigQuery Dataset

1. Create a Dataset name called lake in Big Query
    a. bq mk lake

### Build a Dataflow Pipeline

1. Build a BigData ETL pipeline with a TextIO source and a BigQueryIO destination to ingest data into BigQuery. 
2. It will do the following:
    a. Ingest the files from Cloud Storage.
    b. Convert the lines read to dictionary objects.
    c. Transform the data which contains the year to a format BigQuery understands as a date.
    d. Output the rows to BigQuery.

3. The Dataflow job for this demo requires Python3.7. To do that execute below command in terminal
    a. docker run -it -e PROJECT=$PROJECT -v $(pwd)/dataflow-python-examples:/dataflow python:3.7 /bin/bash
4. run the command  to install apache-beam
    a. pip install apache-beam[gcp]==2.24.0
5. navigate to that path
    a. cd dataflow/dataflow_python_examples  --change accordingly
6. Execute the below command:
    a. python data_transformation.py \
        --project=$PROJECT \
        --region=us-east1 \
        --runner=DataflowRunner \
        --staging_location=gs://$PROJECT/test \
        --temp_location gs://$PROJECT/test \
        --input gs://$PROJECT/data_files/head_usa_names.csv \
        --output lake.table_name \
        --save_main_session



# Resources:

1. https://cloud.google.com/storage/docs/gsutil/commands/mb
2. https://cloud.google.com/sdk/gcloud/reference/dataflow/jobs/run
3. https://github.com/tuanavu/google-dataflow-examples/blob/master/examples/wordcount.py
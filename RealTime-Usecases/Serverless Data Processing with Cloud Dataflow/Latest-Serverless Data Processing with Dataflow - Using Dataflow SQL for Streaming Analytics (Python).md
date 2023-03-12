# Serverless Data Processing with Dataflow - Using Dataflow SQL for Streaming Analytics (Python)

### Aggregating streaming site traffic by minute with SQL
StreamingMinuteTraffic pipeline to perform the following:
1. Reads the day’s traffic from a PubSub topic.
2. Converts each event into a CommonLog object
3. Uses SQL instead of Python transforms to again window the data per minute sum the total number of pageviews
4. Writes the resulting data to BigQuery.

### Next you will download a code repository for use in this lab.

- git clone https://github.com/GoogleCloudPlatform/training-data-analyst
- cd /home/jupyter/training-data-analyst/quests/dataflow_python/


### Task 1. Prepare the environment

- The first step is to generate data for the pipeline to process. You will open the lab environment and generate the data as before.Open the appropriate lab. 
- In the terminal in your IDE, run the following commands to change to the directory you will use for this lab:

###### Change directory into the lab

- cd 6_SQL_Streaming_Analytics/lab
- export BASE_DIR=$(pwd)

###### Set up the virtual environment and dependencies

- Before you can begin editing the actual pipeline code, you need to ensure you have installed the necessary dependencies.
- Execute the following to create a virtual environment for your work in this lab:
- sudo apt-get update && sudo apt-get install -y python3-venv

###### Create and activate virtual environment
- python3 -m venv df-env
- source df-env/bin/activate
  
###### Next, install the packages you will need to execute your pipeline:

- python3 -m pip install -q --upgrade pip setuptools wheel
- python3 -m pip install apache-beam[gcp]

###### Ensure that the Dataflow API is enabled:

- gcloud services enable dataflow.googleapis.com

### Set up the data environment

###### Create GCS buckets and BQ dataset

- cd $BASE_DIR/../..
- source create_streaming_sinks.sh

###### Change to the directory containing the practice version of the code
- cd $BASE_DIR


### Task 2. Read from PubSub, convert to CommonLog, and add and populate the DateTime field and Write an SQL statement to window and aggregate the data

***Go through code***


### Task 4. Execute the pipeline

Return to the terminal and execute the following commands to run your pipeline:
export PROJECT_ID=$(gcloud config get-value project)
export REGION=us-central1
export BUCKET=gs://${PROJECT_ID}
export PIPELINE_FOLDER=${BUCKET}
export RUNNER=DataflowRunner
export PUBSUB_TOPIC=projects/${PROJECT_ID}/topics/my_topic
export TABLE_NAME=${PROJECT_ID}:logs.minute_traffic


python3 streaming_minute_traffic_SQL_pipeline.py \
--project=${PROJECT_ID} \
--region=${REGION} \
--staging_location=${PIPELINE_FOLDER}/staging \
--temp_location=${PIPELINE_FOLDER}/temp \
--runner=${RUNNER} \
--input_topic=${PUBSUB_TOPIC} \
--table_name=${TABLE_NAME} \
--experiments=use_runner_v2

                                        (or)

python3 streaming_minute_traffic_SQL_pipeline.py --project=${PROJECT_ID} --region=${REGION} --staging_location=${PIPELINE_FOLDER}/staging --temp_location=${PIPELINE_FOLDER}/temp --runner=${RUNNER} --input_topic=${PUBSUB_TOPIC} --table_name=${TABLE_NAME} --experiments=use_runner_v2

### Task 5. Generate lag-less streaming input

Make sure you are in the training-data-analyst/quests/dataflow_python folder:

- cd /home/jupyter/training-data-analyst/quests/dataflow_python/
- bash generate_streaming_events.sh



### Task 6. In BigQuery, query the result data:

Examine your results after a few minutes have windowed and written to BigQuery, then cancel the pipeline and generator.

- SELECT * FROM logs.minute_traffic
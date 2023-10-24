>>> **PROFESSIONAL DATA ENGINEER** - *Google Cloud Platform*
------------------------

> TITLE: "Lab on Streaming Data to Cloud Bigtable in GCP"
> 
> Author:
  >- Name: "Vignesh Sekar S"
  >- Designation: "Multi Cloud Architect"
  >- Tags: [Google Cloud, DataEngineer, Python, PySpark, SQL, BigData]

--------------------------------------------------------------------------------------------------------------------

# Overview

* You are just starting your junior data engineer role. So far you have been helping teams create and manage data using BigQuery, Pub/Sub, and Dataflow.

* You are expected to have the skills and knowledge for these tasks.

###### Lab challenge

1. You are asked to help a newly formed development team with some of their initial work on a new project around real-time environmental sensor data. 
2. You have been asked to assist the team with streaming temperature data into BigQuery using Pub/Sub and Dataflow; you receive the following request to complete the following tasks:

    * Create a Cloud Storage bucket as the temporary location for a Dataflow job.
    * Create a BigQuery dataset and table to receive the streaming data.
    * Create up a Pub/Sub topic and test publishing messages to the topic.
    * Create and run a Dataflow job to stream data from a Pub/Sub topic to BigQuery.
    * Run a query to validate streaming data.

3. Some standards you should follow:

    * Ensure that any needed APIs (such as Dataflow) are successfully enabled.


### Task 1. Create a Cloud Storage bucket

* Create a Cloud Storage bucket 

     * gsutil mb gs://bq-streaming-bucket


### Task 2. Create a BigQuery dataset and table

* Create a BigQuery dataset called BigQuery dataset name in the region named US (multi region).In the created dataset, create a table called BigQuery table name.


### Task 3. Set up a Pub/Sub topic

* Create a Pub/Sub topic called Pub/Sub topic name.Use the default settings, which has enabled the checkbox for Add a default subscription.


### Task 4. Run a Dataflow pipeline to stream data from a Pub/Sub topic to BigQuery

* Create and run a Dataflow job called Dataflow job name to stream data from a Pub/Sub topic to the BigQuery table you created in a previous task.

* Use the Pub/Sub topic that you created in a previous task: Pub/Sub topic name

* Use the Cloud Storage bucket that you created in a previous task as the temporary location

* Use the BigQuery dataset and table that you created in a previous task as the output table: BigQuery dataset name.BigQuery table name

* Use Region as the regional endpoint.


### Task 5. Publish a test message to the topic and validate data in BigQuery

* Publish a message to your topic using the following code syntax for Message: {"data": "KF is a Kind person"}

* Run a SELECT statement in BigQuery to see the test message populated in your table.

* Note: If you do not see any test messages in your BigQuery table, check that the Dataflow job has a status of Running, and then send another test message.


------------------------------------------------------------------------------------------------------------------------
  <div class="footer">
              copyright © 2022—2023 Cloud & AI Analytics. 
                                      All rights reserved
          </div>

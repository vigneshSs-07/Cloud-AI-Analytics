>>> **PROFESSIONAL DATA ENGINEER** - *Google Cloud Platform*
------------------------

> TITLE: "Hands on Creating Native and External table in Cloud BigQuery using bq CLI"
> 
> Author:
  >- Name: "Vignesh Sekar S"
  >- Designation: "Multi Cloud Architect"
  >- Tags: [Google Cloud, DataEngineer, Python, PySpark, SQL, BigData]

--------------------------------------------------------------------------------------------------------------------

# Overview

1. BigQuery is Google's fully managed, NoOps, low-cost analytics database. With BigQuery, you can query terabytes of data without a database administrator or infrastructure. BigQuery uses familiar SQL and a pay-only-for-what-you-use charging model. 
   
2. BigQuery allows you to focus on analyzing data to find meaningful insights. In this codelab, you'll use the bq command-line tool to load a local CSV file into a new BigQuery table.

3. You can access BigQuery by using the Console, Web UI or a command-line tool using a variety of client libraries such as Java, .NET, or Python. There are also a variety of solution providers that you can use to interact with BigQuery.

4. This hands-on lab shows you how to use bq, the python-based command line tool for BigQuery, to query public tables and load sample data into BigQuery.


###  Cloud Shell

1. Cloud Shell is a virtual machine that is loaded with development tools. It offers a persistent 5GB home directory and runs on the Google Cloud. Cloud Shell provides command-line access to your Google Cloud resources.

2. Click Activate Cloud Shell Activate Cloud Shell icon at the top of the Google Cloud console.
When you are connected, you are already authenticated, and the project is set to your Project_ID, PROJECT_ID. The output contains a line that declares the Project_ID for this session:

1. **gcloud auth list**: List all credentialed accounts.

2. **gcloud config list**: Display all the properties for the current configuration.

3. **gcloud init**: Initialize, authorize, and configure the gcloud CLI.

4. **gcloud version**: Display version and installed components.

5. **gcloud config set project**: Set a default Google Cloud project to work on.

6. **gcloud info**: Display current gcloud CLI environment details.

7. **gcloud help**: Search the gcloud CLI reference documents for specific terms.

8.  **gcloud auth login**: Authorize Google Cloud access for the gcloud CLI with Google Cloud user credentials and set the current account as active.

9. **gcloud projects describe**: Display metadata for a project (including its ID).

10. **gcloud config set**: Define a property (like compute/zone) for the current configuration.

11. **gcloud config get**: Fetch the value of a gcloud CLI property.


### bq command-line tool reference

1. bq version - command to display the version number of your bq command-line tool.

2. bq help query/show/mk
  
###### Creating a dataset

   *  bq --location=US mk -d \
    --default_table_expiration 3600 \
    --description "This dataset created through BQ CLI." \
    demodataset_bqcli

                            (or)

   * bq mk demodataset_bqcli   

###### Use the bq ls command to list any existing datasets in your projec

   * bq ls

###### Run bq ls and the lucky-leaf-396003 Project ID to list the datasets in that specific project, followed by a colon (:):

   * bq ls lucky-leaf-396003:

                            (or)

   * bq ls lucky-leaf-396003:samples

###### Creating a Table

   * bq mk \
    -t \
    --expiration 3600 \
    --description "This is my table" \
    --label organization:development \
    mydataset.mytable \
    qtr:STRING,sales:FLOAT,year:STRING

###### Examine a table

   * bq show lucky-leaf-396003:demodataset_bqcli.mytable 

###### Creating a table using bq cli from local

   * bq load \
      --source_format=CSV \
      --skip_leading_rows=1 \
      demodataset_bqcli.customer_transactions \
      ./customer_transactions.csv \
      id:string,zip:string,Timestamp:timestamp,amount:numeric,fdbk:float,sku:string

###### Creating a table using bq cli from Google Cloud Storage

   * bq mkdef --source_format=CSV gs://demodataset_biglake/customer_transactions.csv > mytable_def

         * Use the **bq mkdef** command to create a table definition in JSON format for data stored in Cloud Storage or Google Drive.

   * bq mk --table --external_table_definition=mytable_def \
        demodataset_bqcli.customer_transactions_from_storage \
        id:string,zip:string,TimeStamp:timestamp,amount:numeric,Feedback:float,sku:string


###### Used the following options:

  * --source_format=CSV uses the CSV data format when parsing the data file.
  * --skip_leading_rows=1 skips the first line in the CSV file because it is a header row.
  * Bq_load_codelab.customer_transactions—the first positional argument—defines which table the data should be loaded into.
  * ./customer_transactions.csv—the second positional argument—defines which file to load. In addition to local files, the bq load command can load files from Cloud Storage with gs://my_bucket/path/to/file URIs.
  * A schema, which can be defined in a JSON schema file or as a comma-separated list. (You used a comma-separated list for simplicity.)
  * You used the following schema in the customer_transactions table:

        * Id:string: A customer identifier
        * Zip:string: A US postal zip code
        * Ttime:timestamp: The date and time that the transaction took place
        * Amount:numeric: The amount of a transaction (A numeric column stores data in decimal form, which is * useful for monetary values.)
        * Fdbk:float: The rating from a feedback survey about the transaction
        * Sku:string: An identifier for the item purchased


###### Verify that the table loaded by showing the table properties.

   *  bq show demodataset_bqcli.customer_transactions
   *  bq show demodataset_bqcli.customer_transactions_from_storage


### Get information about tables

   *  bq show --format=prettyjson demodataset_bqcli.customer_transactions

                (or)

   *  bq show --schema --format=prettyjson lucky-leaf-396003:demodataset_bqcli.customer_transactions_from_storage.


### Query the data

   *  bq head --max_rows=1 --start_row=1 --selected_fields=id,zip \
        demodataset_bqcli.customer_transactions_from_storage

   *  bq query --nouse_legacy_sql '
        SELECT *
        FROM `demodataset_bqcli.customer_transactions` c
        '

###### Copy data from one table to another table

   *  bq cp demodataset_bqcli.customer_transactions demodataset_bqcli.customer_transactions_from_storageCopy

### Clean up

### Delete the dataset that you created with the bq rm command. Use the -r flag to remove any tables that it contains.

   *  bq rm -r demodataset_bqcli   - Remove Dataset

   *  bq rm -t demodataset_bqcli.customer_transactions  - Remove Table

### drop table with bq command to avoid confirmation

   *  bq rm -f -t zinc-forge-380121:mydataset.mytable1


--------------------------------------------------------------------------------------------------------------------


  <div class="footer">
              copyright © 2022—2023 Cloud & AI Analytics. 
                                      All rights reserved
          </div>

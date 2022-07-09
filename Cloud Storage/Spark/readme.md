# How to Read and Write Spark Dataframe to Storage Bucket in Google Cloud Platform


### Create Dataproc cluster in GCP

gcloud dataproc clusters create dataproc-demo --region us-east1 --zone us-east1-d --single-node --master-machine-type n1-standard-2 --master-boot-disk-size 30 --image-version 2.0-debian10 --project esoteric-state-347411


### Submit Pyspark Job

gcloud dataproc jobs submit pyspark.py \
    --cluster=dataproc-demo \
    --region= us-east1

### Copy file to gcs bucket

gsutil cp (local-filename-cloudshell)  (gcs-bucket-folder/file)

### Resources:

1. https://github.com/GoogleCloudDataproc/spark-bigquery-connector
2. https://www.geeksforgeeks.org/creating-a-pyspark-dataframe/
3. https://www.analyticsvidhya.com/blog/2021/09/beginners-guide-to-create-pyspark-dataframe/
4. https://rs111.medium.com/pandas-with-google-cloud-storage-and-big-query-46961d7bd910
5. https://newbedev.com/write-a-pandas-dataframe-to-google-cloud-storage-or-bigquery

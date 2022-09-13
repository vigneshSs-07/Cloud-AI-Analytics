from pyspark.sql import SparkSession
import pandas

#create spark session
spark = SparkSession.builder.appName("Test").getOrCreate()

#input gcs path
df = spark.read.format("parquet").load("gs://composerbucket-001/userdata1.parquet")

#spark dataframe
df.show()

#write to gcs bucket
df.write.csv('gs://composerbucket-001/Pyspark/Output1', header=True)

#df.write.format("csv").option("path",f'gs://{bucket}/Pyspark/Output/{file_name}').save(header = 'true')


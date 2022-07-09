
from pyspark.sql.types import StructType,StructField, StringType, IntegerType
from pyspark.sql import SparkSession
 
# creating the session
spark = SparkSession.builder.getOrCreate()

#data
data2 = [("James","","Smith","36636","M",3000),
    ("Michael","Rose","","40288","M",4000),
    ("Robert","","Williams","42114","M",4000),
    ("Maria","Anne","Jones","39192","F",4000),
    ("Jen","Mary","Brown","","F",-1)
  ]

#column
schema = StructType([ \
    StructField("firstname",StringType(),True), \
    StructField("middlename",StringType(),True), \
    StructField("lastname",StringType(),True), \
    StructField("id", StringType(), True), \
    StructField("gender", StringType(), True), \
    StructField("salary", IntegerType(), True) \
  ])

#create spark dataframe
df = spark.createDataFrame(data=data2,schema=schema)
df.printSchema()
df.show(truncate=False)


#write to gcs bucket
df.write.format("csv").option("path", f"gs://composerbucket-001/Pyspark/Output").save(header=True)




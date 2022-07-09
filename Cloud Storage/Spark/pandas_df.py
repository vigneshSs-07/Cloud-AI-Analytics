from google.cloud import storage
import pandas

df = pandas.DataFrame([{'Name': 'A', 'Id': 100}, {'Name': 'B', 'Id': 110}])
df.head()
#df.to_csv()
df.to_csv('gs://composerbucket-001/df.csv')

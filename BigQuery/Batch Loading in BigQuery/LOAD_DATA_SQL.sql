LOAD DATA INTO `vaulted-journal-420209.demo_daatset_001.titanic_data`
   OPTIONS(
    description="my table",
    expiration_timestamp="2025-01-01 00:00:00 UTC"
  )
  FROM FILES(
    format='CSV',
    uris = ['gs://example_bucket_demo_0001/titanic_datafusion.csv']
  )

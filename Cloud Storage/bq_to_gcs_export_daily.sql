-- Query to Export data from BQ tables to GCS Bucket

-- Export data from GCP Bigquery to GCS bucket on daily basis using BQ Scheduled Queries

EXPORT DATA
  OPTIONS (
    uri = 'gs://demogcp_bucket_gcli_001/bq_data_exported/bq_gcs_export_daily_*.csv',
    format = 'CSV',
    overwrite = true,
    header = true,
    field_delimiter = ';')
AS (
  SELECT order_id, customer_id, order_date,status 
  FROM `civic-kayak-413201.dbt_vsekar.stg_orders`
  ORDER BY order_date
);

/*
-- Resources

1. https://cloud.google.com/bigquery/docs/exporting-data#parquet_export_details


*/

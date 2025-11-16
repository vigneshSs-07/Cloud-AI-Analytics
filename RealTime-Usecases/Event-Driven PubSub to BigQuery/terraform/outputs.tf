output "pubsub_topic" {
  description = "Pub/Sub topic name"
  value       = google_pubsub_topic.events.name
}

output "bq_table" {
  description = "BigQuery table id"
  value       = "${google_bigquery_dataset.events_ds.dataset_id}.${google_bigquery_table.events_tbl.table_id}"
}

output "function_name" {
  description = "Cloud Functions Gen2 name"
  value       = google_cloudfunctions2_function.pubsub_to_bq.name
}

output "function_bucket" {
  description = "Storage bucket for function source"
  value       = google_storage_bucket.function_bucket.url
}

output "dead_letter_topic" {
  value = google_pubsub_topic.events_dlq.name
}
# -----------------------------
# Cloud Functions Gen2 (google_cloudfunctions2_function)
# -----------------------------
resource "google_cloudfunctions2_function" "pubsub_to_bq" {
  name     = var.function_name
  project  = var.project_id
  location = var.region

  build_config {
    runtime     = "python311"
    entry_point = "pubsub_to_bq"

    # use storage source
    source {
      storage_source {
        bucket     = google_storage_bucket.function_bucket.name
        object     = google_storage_bucket_object.function_zip_obj.name
        generation = google_storage_bucket_object.function_zip_obj.generation
      }
    }
  }

  service_config {
    # memory: allowed values like "256M"
    available_memory   = "256M"
    timeout_seconds    = 60
    max_instance_count = 3
    ingress_settings   = "ALLOW_INTERNAL_ONLY"

    environment_variables = {
      BQ_DATASET = google_bigquery_dataset.events_ds.dataset_id
      BQ_TABLE   = google_bigquery_table.events_tbl.table_id
      PROJECT_ID = var.project_id
    }

    service_account_email = google_service_account.fn_sa.email
  }

  event_trigger {
    event_type     = "google.cloud.pubsub.topic.v1.messagePublished"
    pubsub_topic   = google_pubsub_topic.events.id
    trigger_region = var.region
  }

  depends_on = [
    google_project_service.required_apis,
    google_storage_bucket_object.function_zip_obj
  ]
}

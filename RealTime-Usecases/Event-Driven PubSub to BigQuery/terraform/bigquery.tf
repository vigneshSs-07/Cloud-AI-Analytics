# -----------------------------
# BigQuery dataset & table
# -----------------------------
resource "google_bigquery_dataset" "events_ds" {
  dataset_id    = var.dataset_name
  project       = var.project_id
  location      = var.location
  friendly_name = "Events dataset"
  description   = "Dataset for streaming events from Pub/Sub"
}

resource "google_bigquery_table" "events_tbl" {
  dataset_id          = google_bigquery_dataset.events_ds.dataset_id
  project             = var.project_id
  table_id            = var.table_name
  deletion_protection = false

  schema = jsonencode([
    {
      name = "id"
      type = "STRING"
      mode = "REQUIRED"
    },
    {
      name = "payload"
      type = "STRING"
      mode = "NULLABLE"
    },
    {
      name = "received_at"
      type = "TIMESTAMP"
      mode = "REQUIRED"
    }
  ])
}
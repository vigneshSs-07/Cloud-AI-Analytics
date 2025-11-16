# -----------------------------
# Service account for function
# -----------------------------
resource "google_service_account" "fn_sa" {
  account_id   = "fn-sa-pubsub-bq"
  project      = var.project_id
  display_name = "Cloud Function Gen2 SA for Pub/Sub -> BigQuery"
}

# Grant service account permission to insert rows into BigQuery (project-level editor for simplicity).
resource "google_project_iam_member" "sa_bq_writer" {
  project = var.project_id
  role    = "roles/bigquery.dataEditor"
  member  = "serviceAccount:${google_service_account.fn_sa.email}"
}

# Logging permission
resource "google_project_iam_member" "sa_logging" {
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.fn_sa.email}"
}

# If the function will call other Google APIs (e.g., storage) grant those as needed (optional)
resource "google_project_iam_member" "sa_storage_object_viewer" {
  project = var.project_id
  role    = "roles/storage.objectViewer"
  member  = "serviceAccount:${google_service_account.fn_sa.email}"
}

# -----------------------------
# Enable required APIs
# -----------------------------
locals {
  apis = [
    "pubsub.googleapis.com",
    "cloudfunctions.googleapis.com",
    "cloudfunctions.googleapis.com", # gen2 uses Cloud Functions API
    "eventarc.googleapis.com",
    "cloudbuild.googleapis.com",
    "storage.googleapis.com",
    "bigquery.googleapis.com",
    "run.googleapis.com", # used by gen2 under the hood
    "iam.googleapis.com",
    "logging.googleapis.com"
  ]
}

resource "google_project_service" "required_apis" {
  for_each           = toset(local.apis)
  project            = var.project_id
  service            = each.value
  disable_on_destroy = false
}





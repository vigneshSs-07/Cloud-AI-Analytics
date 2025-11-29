terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# -----------------------------
# Enable required APIs
# -----------------------------
resource "google_project_service" "services" {
  for_each = toset([
    "sqladmin.googleapis.com",
    "compute.googleapis.com",
    "servicenetworking.googleapis.com"
  ])

  project            = var.project_id
  service            = each.key
  disable_on_destroy = false
}



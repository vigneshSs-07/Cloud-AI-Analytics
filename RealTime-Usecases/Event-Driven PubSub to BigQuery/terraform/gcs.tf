# -----------------------------
# Storage bucket for deployment zip
# -----------------------------
resource "random_id" "bucket_suffix" {
  byte_length = 4
}

resource "google_storage_bucket" "function_bucket" {
  name                        = "${var.project_id}-function-deploy-${random_id.bucket_suffix.hex}"
  project                     = var.project_id
  location                    = var.region
  uniform_bucket_level_access = true
  force_destroy               = true
}

# Package function into zip (archive_file)
data "archive_file" "function_zip" {
  type        = "zip"
  source_dir  = "${path.module}/function"
  output_path = "${path.module}/function.zip"
}

resource "google_storage_bucket_object" "function_zip_obj" {
  bucket = google_storage_bucket.function_bucket.name
  name   = "function-source.zip"
  source = data.archive_file.function_zip.output_path

  metadata = {
    content_hash = filesha256(data.archive_file.function_zip.output_path)
  }
}


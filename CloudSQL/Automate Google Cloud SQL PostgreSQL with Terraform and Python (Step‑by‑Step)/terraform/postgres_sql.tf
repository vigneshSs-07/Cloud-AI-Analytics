resource "random_id" "db_name_suffix" {
  byte_length = 4
}

resource "google_sql_database_instance" "postgres" {
  name             = "postgres-instance-${random_id.db_name_suffix.hex}"
  database_version = "POSTGRES_15"
  region           = var.region

  settings {
    tier    = "db-custom-1-3840"
    edition = "ENTERPRISE"

    user_labels = {
      "environment" = "production"
      "owner"       = "cloud-ai-analytics-team"
      "managed-by"  = "terraform"
    }

    activation_policy = "ALWAYS"
    availability_type = "REGIONAL"

    ip_configuration {
      ipv4_enabled = true
      # Consider adding private IP and removing public IP for production
      # private_network = var.vpc_network_id
      # ipv4_enabled    = false

      authorized_networks {
        name  = "prodsetup"
        value = var.my_public_ip
      }
    }

    # Recommended additions for production
    backup_configuration {
      enabled                        = true
      start_time                     = "03:00" # UTC time
      point_in_time_recovery_enabled = true
      transaction_log_retention_days = 7

      backup_retention_settings {
        retained_backups = 30
        retention_unit   = "COUNT"
      }
    }

    # Maintenance window to control when updates occur
    maintenance_window {
      day          = 7 # Sunday
      hour         = 3 # 3 AM UTC
      update_track = "stable"
    }

    # Enable insights for monitoring
    insights_config {
      query_insights_enabled  = true
      query_plans_per_minute  = 5
      query_string_length     = 1024
      record_application_tags = true
    }

    # Disk configuration
    disk_autoresize       = true
    disk_autoresize_limit = 0  # No limit
    disk_size             = 10 # Starting size in GB
    disk_type             = "PD_SSD"
  }

  deletion_protection = false

  depends_on = [google_project_service.services]
}


# -----------------------------
# Create Database
# -----------------------------
resource "google_sql_database" "db" {
  name     = var.database_name
  instance = google_sql_database_instance.postgres.name
}

# -----------------------------
# Create SQL User
# -----------------------------
resource "google_sql_user" "user" {
  name     = var.db_user
  password = var.db_password
  instance = google_sql_database_instance.postgres.name
}
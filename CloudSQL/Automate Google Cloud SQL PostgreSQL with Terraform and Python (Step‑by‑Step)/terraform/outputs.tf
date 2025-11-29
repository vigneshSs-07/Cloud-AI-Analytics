output "public_ip" {
  value = google_sql_database_instance.postgres.public_ip_address
}

output "db_connection_name" {
  value = google_sql_database_instance.postgres.connection_name
}

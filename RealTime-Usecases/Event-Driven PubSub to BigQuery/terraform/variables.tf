variable "project_id" {
  description = "GCP project id"
  type        = string
}

variable "region" {
  description = "GCP region for resources"
  type        = string
  default     = "us-central1"
}

variable "location" {
  description = "BigQuery location (e.g. US, EU)"
  type        = string
  default     = "US"
}

variable "topic_name" {
  description = "Pub/Sub topic name"
  type        = string
  default     = "events-topic"
}

variable "dataset_name" {
  description = "BigQuery dataset name"
  type        = string
  default     = "events_dataset"
}

variable "table_name" {
  description = "BigQuery table name"
  type        = string
  default     = "events_table"
}

variable "function_name" {
  description = "Cloud Functions (Gen2) service name"
  type        = string
  default     = "pubsub-to-bigquery-fn"
}

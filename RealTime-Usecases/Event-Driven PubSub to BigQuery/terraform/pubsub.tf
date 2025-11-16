# -----------------------------
# Pub/Sub topic
# -----------------------------
resource "google_pubsub_topic" "events" {
  name    = var.topic_name
  project = var.project_id
}

# -----------------------------
# DEAD LETTER QUEUE (DLQ)
# -----------------------------
resource "google_pubsub_topic" "events_dlq" {
  name    = "${var.topic_name}-dlq"
  project = var.project_id
}

# Create a subscription that routes failed messages to the DLQ
resource "google_pubsub_subscription" "events_subscription" {
  name  = "${var.topic_name}-sub"
  topic = google_pubsub_topic.events.name

  ack_deadline_seconds = 20

  dead_letter_policy {
    dead_letter_topic     = google_pubsub_topic.events_dlq.id
    max_delivery_attempts = 5 # after 3 failed deliveries -> DLQ
  }
}



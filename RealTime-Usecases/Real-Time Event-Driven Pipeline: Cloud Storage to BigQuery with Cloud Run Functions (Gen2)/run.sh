#!/bin/bash
# =============================================================================
# Cloud Run Function Deployment Script
# Purpose : Deploy a GCS-triggered Cloud Run Function that loads Avro files
#           from Cloud Storage into BigQuery.
# Runtime : Python 3.12
# Trigger : google.storage.object.finalize (fires on file upload to GCS)
# =============================================================================

set -euo pipefail

# -----------------------------------------------------------------------------
# 1. PROJECT & REGION CONFIGURATION
# -----------------------------------------------------------------------------
export PROJECT_ID=$(gcloud config get-value project)
export REGION="us-central1"
export PROJECT_NUMBER=$(gcloud projects describe "$PROJECT_ID" \
    --format='value(projectNumber)')

echo "Project ID     : $PROJECT_ID"
echo "Project Number : $PROJECT_NUMBER"
echo "Region         : $REGION"

gcloud config set compute/region "$REGION"
gcloud config set run/region "$REGION"
gcloud config set run/platform managed
gcloud config set eventarc/location "$REGION"

# -----------------------------------------------------------------------------
# 2. ENABLE REQUIRED GOOGLE CLOUD APIs
# -----------------------------------------------------------------------------
echo "Enabling required APIs..."

gcloud services enable \
    artifactregistry.googleapis.com \
    cloudfunctions.googleapis.com \
    cloudbuild.googleapis.com \
    eventarc.googleapis.com \
    run.googleapis.com \
    logging.googleapis.com \
    pubsub.googleapis.com

# -----------------------------------------------------------------------------
# 3. IAM PERMISSIONS
#    - Grant the default Compute Engine SA permission to receive Eventarc events.
#    - Grant the Cloud Storage service agent permission to publish to Pub/Sub.
# -----------------------------------------------------------------------------
echo "Configuring IAM permissions..."

# Allow Compute Engine SA to receive Eventarc events
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
    --role="roles/eventarc.eventReceiver"

# Initialise the GCS service agent (it may not exist yet in new projects)
gcloud services identity create --service=storage.googleapis.com --project="$PROJECT_ID" || true
sleep 5  # Allow time for the service agent to propagate

# Allow GCS service agent to publish Pub/Sub messages (required for event triggers)
GCS_SERVICE_ACCOUNT="service-${PROJECT_NUMBER}@gs-project-accounts.iam.gserviceaccount.com"

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:${GCS_SERVICE_ACCOUNT}" \
    --role="roles/pubsub.publisher"

# Initialise the Eventarc service agent and grant it the required role
gcloud services identity create --service=eventarc.googleapis.com --project="$PROJECT_ID" || true

EVENTARC_SA="service-${PROJECT_NUMBER}@gcp-sa-eventarc.iam.gserviceaccount.com"

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:${EVENTARC_SA}" \
    --role="roles/eventarc.serviceAgent"

sleep 10  # Allow time for IAM permissions to propagate

# -----------------------------------------------------------------------------
# 4. INSTALL PYTHON DEPENDENCIES (optional — for local testing in Cloud Shell)
# -----------------------------------------------------------------------------
echo "Installing Python dependencies..."
pip install -r requirements.txt

# -----------------------------------------------------------------------------
# 5. CREATE GCS BUCKET & BIGQUERY DATASET
# -----------------------------------------------------------------------------
echo "Creating GCS bucket and BigQuery dataset..."

gcloud storage buckets create "gs://${PROJECT_ID}" --location="$REGION" || \
    echo "Bucket gs://${PROJECT_ID} already exists — skipping."

bq mk -d loadavro || \
    echo "Dataset 'loadavro' already exists — skipping."

# -----------------------------------------------------------------------------
# 6. DEPLOY CLOUD RUN FUNCTION (Gen 2)
# -----------------------------------------------------------------------------
echo "Deploying Cloud Run Function..."

gcloud functions deploy load_bigquery_from_avro \
    --gen2 \
    --runtime python312 \
    --entry-point load_bigquery_from_avro \
    --source . \
    --region "$REGION" \
    --trigger-resource "gs://${PROJECT_ID}" \
    --trigger-event google.storage.object.finalize \
    --memory=512Mi \
    --timeout=540s \
    --service-account="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"

# -----------------------------------------------------------------------------
# 7. VERIFY EVENTARC TRIGGER
# -----------------------------------------------------------------------------
echo "Verifying Eventarc trigger..."
gcloud eventarc triggers list --location="$REGION"

# -----------------------------------------------------------------------------
# 8. TEST — DOWNLOAD AVRO FILE & UPLOAD TO GCS TO TRIGGER THE FUNCTION
# -----------------------------------------------------------------------------

echo "Uploading campaigns.avro to gs://${PROJECT_ID} (this triggers the function)..."
gcloud storage cp campaigns.avro "gs://${PROJECT_ID}"

echo "Deployment complete. Check BigQuery dataset 'loadavro' for the 'campaigns' table."
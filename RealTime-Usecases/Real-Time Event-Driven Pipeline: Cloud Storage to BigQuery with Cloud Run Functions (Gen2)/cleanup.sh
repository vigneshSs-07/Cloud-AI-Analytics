#!/bin/bash
# =============================================================================
# Cleanup Script
# Purpose : Delete all resources created by run.sh
# Deletes : Cloud Run Function, Eventarc trigger, BigQuery dataset,
#           GCS bucket, Artifact Registry images, Cloud Build artifacts
# Keeps   : Service accounts (IAM bindings left intact)
# =============================================================================

set -euo pipefail

# -----------------------------------------------------------------------------
# 1. PROJECT & REGION CONFIGURATION
# -----------------------------------------------------------------------------
export PROJECT_ID=$(gcloud config get-value project)
export REGION="us-central1"

echo "Project ID : $PROJECT_ID"
echo "Region     : $REGION"
echo ""
echo "This script will delete the following resources:"
echo "  - Cloud Run Function : load_bigquery_from_avro"
echo "  - Eventarc trigger   : load-bigquery-from-avro-*"
echo "  - BigQuery dataset   : loadavro (and all tables)"
echo "  - GCS bucket         : gs://${PROJECT_ID} (and all objects)"
echo "  - Artifact Registry  : gcf-artifacts docker images"
echo ""
read -p "Are you sure you want to proceed? (y/N): " CONFIRM
if [[ "$CONFIRM" != "y" && "$CONFIRM" != "Y" ]]; then
    echo "Cleanup cancelled."
    exit 0
fi

# -----------------------------------------------------------------------------
# 2. DELETE CLOUD RUN FUNCTION (Gen 2)
# -----------------------------------------------------------------------------
echo "Deleting Cloud Run Function..."
gcloud functions delete load_bigquery_from_avro \
    --gen2 \
    --region="$REGION" \
    --quiet || echo "Cloud Run Function not found — skipping."

# -----------------------------------------------------------------------------
# 3. DELETE EVENTARC TRIGGERS
# -----------------------------------------------------------------------------
echo "Deleting Eventarc triggers..."
TRIGGERS=$(gcloud eventarc triggers list \
    --location="$REGION" \
    --format="value(name)" \
    --filter="name~load-bigquery-from-avro" 2>/dev/null || true)

if [[ -n "$TRIGGERS" ]]; then
    for TRIGGER in $TRIGGERS; do
        echo "  Deleting trigger: $TRIGGER"
        gcloud eventarc triggers delete "$TRIGGER" \
            --location="$REGION" \
            --quiet || true
    done
else
    echo "  No matching triggers found — skipping."
fi

# -----------------------------------------------------------------------------
# 4. DELETE BIGQUERY DATASET (including all tables)
# -----------------------------------------------------------------------------
echo "Deleting BigQuery dataset 'loadavro'..."
bq rm -r -f -d "${PROJECT_ID}:loadavro" || \
    echo "Dataset 'loadavro' not found — skipping."

# -----------------------------------------------------------------------------
# 5. DELETE GCS BUCKET (including all objects)
# -----------------------------------------------------------------------------
echo "Deleting GCS bucket gs://${PROJECT_ID}..."
gcloud storage rm -r "gs://${PROJECT_ID}" || \
    echo "Bucket gs://${PROJECT_ID} not found — skipping."

# -----------------------------------------------------------------------------
# 6. DELETE ARTIFACT REGISTRY IMAGES (created by Cloud Build during deploy)
# -----------------------------------------------------------------------------
echo "Cleaning up Artifact Registry..."
REPOS=$(gcloud artifacts repositories list \
    --location="$REGION" \
    --format="value(name)" \
    --filter="name~gcf-artifacts" 2>/dev/null || true)

if [[ -n "$REPOS" ]]; then
    for REPO in $REPOS; do
        echo "  Deleting repository: $REPO"
        gcloud artifacts repositories delete "$REPO" \
            --location="$REGION" \
            --quiet || true
    done
else
    echo "  No gcf-artifacts repositories found — skipping."
fi

echo ""
echo "Cleanup complete. Service accounts and IAM bindings were preserved."

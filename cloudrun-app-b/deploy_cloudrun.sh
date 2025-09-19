#!/bin/bash
# Automated build and deploy script for App B to Google Cloud Run
set -e
PROJECT_ID=dsights-golden-test-99
REGION=asia-south1
SERVICE_NAME=app-b
IMAGE=asia-south1-docker.pkg.dev/$PROJECT_ID/app-a-repo/$SERVICE_NAME

# Enable Cloud Run Admin API (automated)
gcloud services enable run.googleapis.com

# Build and push Docker image
gcloud builds submit --tag $IMAGE

# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME \
  --image $IMAGE \
  --platform managed \
  --region $REGION \
  --service-account gcp-deploy-test@dsights-golden-test-99.iam.gserviceaccount.com \
  --port 8080

echo "Deployment complete. Visit your Cloud Run service URL to test endpoints."

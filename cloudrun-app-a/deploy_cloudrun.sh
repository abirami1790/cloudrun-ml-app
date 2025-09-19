#!/bin/bash
# Automated build and deploy script for App A to Google Cloud Run
set -e
PROJECT_ID=dsights-golden-test-99
REGION=asia-south1
SERVICE_NAME=app-a
IMAGE=gcr.io/$PROJECT_ID/$SERVICE_NAME
IMAGE=asia-south1-docker.pkg.dev/$PROJECT_ID/app-a-repo/$SERVICE_NAME
APP_B_URL=https://app-b-ktkg7phbqa-el.a.run.app # <-- Replace with actual deployed App B URL

# Build and push Docker image
  # Enable Cloud Run Admin API (automated)
  gcloud services enable run.googleapis.com

gcloud builds submit --tag $IMAGE

# Deploy to Cloud Run

gcloud run deploy $SERVICE_NAME \
  --image $IMAGE \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars APP_B_URL=$APP_B_URL \
  --service-account gcp-deploy-test@dsights-golden-test-99.iam.gserviceaccount.com

echo "Deployment complete. Visit your Cloud Run service URL to test endpoints."

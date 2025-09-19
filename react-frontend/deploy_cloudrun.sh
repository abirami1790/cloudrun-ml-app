#!/bin/zsh
# Automated build and deploy script for React frontend to Google Cloud Run (Artifact Registry)
set -e
PROJECT_ID=dsights-golden-test-99
REGION=asia-south1
REPO=react-frontend-repo
IMAGE=asia-south1-docker.pkg.dev/$PROJECT_ID/$REPO/react-frontend
SERVICE_NAME=react-frontend

# Enable Cloud Run Admin API (automated)
gcloud services enable run.googleapis.com

gcloud artifacts repositories describe $REPO --location=$REGION --project=$PROJECT_ID 2>/dev/null || \
  gcloud artifacts repositories create $REPO --repository-format=docker --location=$REGION --project=$PROJECT_ID

# Build and push Docker image
gcloud builds submit --tag $IMAGE

# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME \
  --image $IMAGE \
  --platform managed \
  --region $REGION \
  --port 8080 \
  --project $PROJECT_ID

echo "Deployment complete. Visit your Cloud Run service URL to test the frontend."

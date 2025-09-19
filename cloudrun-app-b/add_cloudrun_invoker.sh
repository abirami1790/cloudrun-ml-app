#!/bin/bash
# Usage: ./add_cloudrun_invoker.sh email1@example.com email2@example.com ...
SERVICE_NAME="app-b"
REGION="asia-south1"
for EMAIL in "$@"; do
  echo "Granting Cloud Run Invoker to $EMAIL..."
  gcloud run services add-iam-policy-binding $SERVICE_NAME \
    --region $REGION \
    --member="user:$EMAIL" \
    --role="roles/run.invoker"
done
echo "All specified users have been granted Cloud Run Invoker permissions."

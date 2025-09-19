#!/bin/bash
# Usage: ./secure_cloudrun.sh
# This script removes public access from Cloud Run service and verifies protection.

SERVICE_NAME="app-b"
REGION="asia-south1"
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region $REGION --format="value(status.url)")

# Remove public invoker role
echo "Removing public access (allUsers) from $SERVICE_NAME..."
gcloud run services remove-iam-policy-binding $SERVICE_NAME \
  --region $REGION \
  --member="allUsers" \
  --role="roles/run.invoker"

# Test unauthenticated access
echo "Testing unauthenticated access..."
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$SERVICE_URL/predict/iris" \
  -H "Content-Type: application/json" \
  -d '{"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2}')

if [[ "$RESPONSE" == "401" || "$RESPONSE" == "403" ]]; then
  echo "✅ Unauthenticated access is blocked (HTTP $RESPONSE)"
else
  echo "❌ Unauthenticated access is NOT blocked (HTTP $RESPONSE)"
fi

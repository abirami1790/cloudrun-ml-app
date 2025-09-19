#!/bin/bash
# Usage: ./test_cloudrun_api.sh <SERVICE_URL>
# Example: ./test_cloudrun_api.sh https://app-b-xxxx-uc.a.run.app

SERVICE_URL="$1"
if [ -z "$SERVICE_URL" ]; then
  echo "Usage: $0 <SERVICE_URL>"
  exit 1
fi

TOKEN=$(gcloud auth print-identity-token)

# Sample payload for iris prediction
PAYLOAD='{"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2}'

# Make authenticated POST request
curl -X POST "$SERVICE_URL/predict/iris" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD"

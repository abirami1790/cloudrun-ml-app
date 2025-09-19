import requests
import subprocess
import json

# Replace with your actual Cloud Run service URL
SERVICE_URL = "https://app-b-357536902999.asia-south1.run.app/predict/iris"


# Get Google identity token using gcloud
token = subprocess.check_output(["gcloud", "auth", "print-identity-token"]).decode().strip()

# JSON payload for iris prediction
payload = {
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
}

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

response = requests.post(SERVICE_URL, headers=headers, data=json.dumps(payload))
print("Status code:", response.status_code)
print("Response:", response.json())

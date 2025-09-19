
"""
Local Development Instructions:
--------------------------------
1. For local testing, set the environment variable LOCAL_DEV=1 before starting App A:
    export LOCAL_DEV=1
    uvicorn main:app --host 0.0.0.0 --port 8080

2. In production, ensure App A runs with a Google service account that has the 'Cloud Run Invoker' role for App B.
    Use gcloud to add the IAM policy:
    gcloud run services add-iam-policy-binding <app-b-service-name> \
      --member="serviceAccount:<app-a-service-account>" \
      --role="roles/run.invoker" \
      --region=<region> --project=<project>
"""
from fastapi import FastAPI, Request, HTTPException
# To automate enabling Cloud Run Admin API, run this shell command before deploying:
# gcloud services enable run.googleapis.com
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import auth, credentials
import requests
import os
import logging

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Firebase Admin SDK with explicit project ID
if not firebase_admin._apps:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {'projectId': 'dsights-golden-test-99'})

GOOGLE_METADATA_URL = "http://metadata/computeMetadata/v1/instance/service-accounts/default/identity"
GOOGLE_METADATA_HEADERS = {"Metadata-Flavor": "Google"}

APP_B_URL = os.environ.get("APP_B_URL", "https://app-b-ktkg7phbqa-el.a.run.app")
APP_C_URL = os.environ.get("APP_C_URL", "https://app-c-ktkg7phbqa-el.a.run.app")
APP_D_URL = os.environ.get("APP_D_URL", "https://app-d-ktkg7phbqa-el.a.run.app")

@app.get("/")
def root():
    return {"message": "App A Gateway is running."}

def verify_firebase_token(id_token: str):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        logging.error(f"Firebase token verification failed: {e}")
        raise HTTPException(status_code=401, detail=f"Invalid Firebase ID token: {e}")

def fetch_identity_token(audience: str):
    params = {"audience": audience}
    resp = requests.get(GOOGLE_METADATA_URL, headers=GOOGLE_METADATA_HEADERS, params=params)
    if resp.status_code == 200:
        return resp.text
    raise HTTPException(status_code=500, detail="Failed to fetch identity token from metadata server.")

import asyncio

async def route_request(target_url: str, request: Request, identity_token: str):
    try:
        body = None
        if request.method in ("POST", "PUT", "PATCH"):
            body = await request.body()
        headers = {k: v for k, v in request.headers.items() if k.lower() != "authorization"}
        headers["Authorization"] = f"Bearer {identity_token}"
        loop = asyncio.get_event_loop()
        def do_request():
            return requests.request(
                method=request.method,
                url=target_url,
                headers=headers,
                data=body,
                params=dict(request.query_params),
            )
        resp = await loop.run_in_executor(None, do_request)
        try:
            content = resp.json()
        except Exception:
            content = resp.text
        return JSONResponse(status_code=resp.status_code, content=content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error routing request: {e}")

@app.api_route("/route/{app_name}/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def gateway_route(app_name: str, path: str, request: Request):
    id_token = request.headers.get("Authorization")
    if not id_token or not id_token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header.")
    id_token = id_token.split(" ", 1)[1]
    verify_firebase_token(id_token)

    # Determine target app URL
    if app_name == "b":
        target_url = f"{APP_B_URL}/{path}"
        audience = APP_B_URL
        print(f"[DEBUG] Routing to App B: {target_url}")
    elif app_name == "c":
        target_url = f"{APP_C_URL}/{path}"
        audience = APP_C_URL
    elif app_name == "d":
        target_url = f"{APP_D_URL}/{path}"
        audience = APP_D_URL
    else:
        raise HTTPException(status_code=404, detail="Unknown app name.")

    identity_token = fetch_identity_token(audience)
    return await route_request(target_url, request, identity_token)


# Direct endpoint for App B prediction (for debugging)
@app.post("/predict")
async def call_predict(request: Request):
    id_token = request.headers.get("Authorization")
    if not id_token or not id_token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header.")
    # Validate Firebase token
    verify_firebase_token(id_token.split(" ", 1)[1])
    payload = await request.json()
    # Generate identity token for App B
    identity_token = fetch_identity_token(APP_B_URL)
    headers = {"Authorization": f"Bearer {identity_token}", "Content-Type": "application/json"}
    # Forward request to App B
    resp = requests.post(f"{APP_B_URL}/predict/iris", json=payload, headers=headers)
    try:
        content = resp.json()
    except Exception:
        content = resp.text
    return JSONResponse(status_code=resp.status_code, content=content)
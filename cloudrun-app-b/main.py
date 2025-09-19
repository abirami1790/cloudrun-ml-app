
from fastapi import FastAPI, Request
from pydantic import BaseModel
import joblib
import os
import pathlib
from fastapi.middleware.cors import CORSMiddleware

import pathlib


app = FastAPI()

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the trained model at startup
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "iris_model.pkl")
print(f"[DEBUG] Looking for model at: {MODEL_PATH}")
print(f"[DEBUG] Model exists: {pathlib.Path(MODEL_PATH).exists()}")
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    model = None
    print(f"Warning: Could not load model: {e}")

class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

@app.get("/")
def root():
    return {"message": "App B (Prediction API) is running."}

@app.post("/predict/iris")
async def predict_iris(data: IrisInput, request: Request):
    import logging
    logging.basicConfig(level=logging.INFO)
    logging.info(f"Received data: {data}")
    print("Prediction endpoint called")
    print("[DEBUG] Incoming headers:", dict(request.headers))
    print("[DEBUG] Incoming body:", await request.body())
    # Mock authentication for local development
    auth_header = request.headers.get("authorization", "")
    if auth_header == "Bearer local-dev-identity-token":
        print("[DEBUG] Local dev token accepted.")
    else:
        # In production, validate the token properly
        # For now, just check that the header exists
        if not auth_header:
            return {"error": "Missing Authorization header"}
    if model is None:
        return {"error": "Model not loaded"}
    features = [[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]]
    prediction = model.predict(features)
    iris_types = ["setosa", "versicolor", "virginica"]
    pred_class = int(prediction[0])
    pred_label = iris_types[pred_class] if 0 <= pred_class < len(iris_types) else str(pred_class)
    logging.info(f"Prediction result: {pred_label}")
    return {"prediction": pred_label}


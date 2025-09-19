from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/predict")
async def predict(request: Request):
    data = await request.json()
    return {"result": "mocked prediction", "inputs": data.get("inputs")}

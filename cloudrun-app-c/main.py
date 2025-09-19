from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "App C (Profile API) is running."}

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "App D (Logging API) is running."}

from fastapi import FastAPI

app = FastAPI(title="Simple Drive", version="1.0.0")


@app.get("/")
def root():
    return {"message": "Simple Drive API"}


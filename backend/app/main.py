from fastapi import FastAPI

@app.get("/")
def read_root():
    return {"status": "online", "message": "Backend is running!"}

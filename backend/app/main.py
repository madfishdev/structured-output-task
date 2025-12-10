from fastapi import FastAPI, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AuthCredentials(BaseModel):
    username: str
    password: str

@app.get("/")
def read_root():
    return {"status": "online", "message": "Backend Mock is running!"}

@app.post("/login")
def login_mock(creds: AuthCredentials):
    return {
        "access_token": f"mock-token-for-{creds.username}", 
        "token_type": "bearer"
    }

@app.post("/register")
def register_mock(creds: AuthCredentials):
    return {
        "access_token": f"mock-token-for-{creds.username}", 
        "token_type": "bearer"
    }

@app.post("/analyze")
async def analyze_mock(
    prompt: str = Form(...),
    fields: str = Form(...),
    file: UploadFile = File(None)
):
    time.sleep(1.5)
    return {
        "inventor_full_name": "Alan Turing",
        "birth_year": 1912,
        "shirt_number": 140,
        "achievement": "Cracked Enigma"
    }
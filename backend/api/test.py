"""
Minimal test endpoint for Vercel
"""
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "ok", "message": "minimal test works"}

@app.get("/api/health")
def health():
    return {"status": "healthy"}

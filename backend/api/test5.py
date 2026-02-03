"""
Test google.generativeai import
"""
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
@app.get("/api/health")
def test():
    try:
        import google.generativeai as genai
        return {
            "status": "success",
            "google_imported": True,
            "genai_version": getattr(genai, '__version__', 'unknown')
        }
    except Exception as e:
        import traceback
        import sys
        return {
            "status": "failed",
            "error": str(e),
            "type": type(e).__name__,
            "python_path": sys.path[:5],
            "traceback": traceback.format_exc()[-1000:]
        }

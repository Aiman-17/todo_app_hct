"""
Test if src.main can be imported
"""
import sys
from pathlib import Path
from fastapi import FastAPI

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

app = FastAPI()

@app.get("/")
@app.get("/api/health")
def test():
    try:
        # Try to import main module
        from src import main

        return {
            "status": "success",
            "main_imported": True,
            "has_app": hasattr(main, 'app'),
            "app_type": str(type(main.app)) if hasattr(main, 'app') else None
        }
    except Exception as e:
        import traceback
        return {
            "status": "failed",
            "error": str(e),
            "type": type(e).__name__,
            "traceback": traceback.format_exc()[-2000:]  # Last 2000 chars
        }

"""
Test database import specifically
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
        # Try to import database module
        from src import database
        db_status = "database imported successfully"
        has_engine = hasattr(database, 'engine')

        # Try to import config
        from src import config
        config_status = "config imported successfully"
        has_settings = hasattr(config, 'settings')

        return {
            "status": "success",
            "database": db_status,
            "has_engine": has_engine,
            "config": config_status,
            "has_settings": has_settings
        }
    except Exception as e:
        import traceback
        return {
            "status": "failed",
            "error": str(e),
            "type": type(e).__name__,
            "traceback": traceback.format_exc()
        }

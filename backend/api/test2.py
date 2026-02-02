"""
Test if main app can be imported
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from src.main import app

    # Create a simple wrapper that responds to all routes
    from fastapi import FastAPI
    test_app = FastAPI()

    @test_app.get("/")
    @test_app.get("/api/health")
    def test():
        return {"status": "import successful", "app_loaded": True}

    app = test_app
except Exception as e:
    # If import fails, create error app
    from fastapi import FastAPI
    app = FastAPI()

    @app.get("/")
    @app.get("/api/health")
    def error():
        return {"status": "import failed", "error": str(e), "type": type(e).__name__}

"""
Vercel serverless function entry point for FastAPI
"""
from src.main import app

# Vercel expects 'app' or 'application' variable
application = app

"""
Vercel serverless function entry point for FastAPI
"""
import sys
from pathlib import Path

# Add parent directory to path so we can import src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.main import app as application

# Export for Vercel - Vercel's @vercel/python expects 'app' or 'application'
app = application

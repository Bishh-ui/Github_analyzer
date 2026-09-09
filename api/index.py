import os
import sys
from pathlib import Path

# Add project root directory to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app import create_app

# Expose WSGI application instance for Vercel
app = create_app()

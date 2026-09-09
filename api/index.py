import os
import sys
from pathlib import Path

# Add project root, api directory, and current working directory to Python path
API_DIR = Path(__file__).resolve().parent
ROOT_DIR = API_DIR.parent

for p in (str(ROOT_DIR), str(API_DIR), os.getcwd()):
    if p not in sys.path:
        sys.path.insert(0, p)

from app import create_app

# Top-level WSGI application instance for Vercel
app = create_app()
application = app
handler = app

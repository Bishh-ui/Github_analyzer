import os
import sys
import traceback
from pathlib import Path

# Add project root directory to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from app import create_app
    app = create_app()
    handler = app
except Exception as e:
    from flask import Flask, Response
    err_trace = traceback.format_exc()
    print("Vercel Startup Error:\n", err_trace)
    app = Flask(__name__)
    handler = app

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        return Response(
            f"<h2>Application Startup Error on Vercel</h2><pre>{err_trace}</pre>",
            status=500,
            mimetype="text/html"
        )

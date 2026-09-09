import os
import sys
import traceback
from pathlib import Path

# Add project root, api directory, and current working directory to Python path
API_DIR = Path(__file__).resolve().parent
ROOT_DIR = API_DIR.parent

for p in (str(ROOT_DIR), str(API_DIR), os.getcwd()):
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from app import create_app
    app = create_app()
except Exception as e:
    err_trace = traceback.format_exc()
    print("Vercel Startup Error Traceback:\n", err_trace, file=sys.stderr)
    try:
        from flask import Flask, Response
        app = Flask(__name__)

        @app.route('/', defaults={'path': ''})
        @app.route('/<path:path>')
        def catch_all(path):
            return Response(
                f"<html><head><title>Vercel Startup Error</title></head>"
                f"<body style='font-family: monospace; background: #0f172a; color: #f87171; padding: 2rem;'>"
                f"<h2>Application Startup Error on Vercel</h2>"
                f"<pre style='background: #1e293b; color: #f1f5f9; padding: 1.5rem; border-radius: 8px; overflow-x: auto;'>{err_trace}</pre>"
                f"</body></html>",
                status=500,
                mimetype="text/html"
            )
    except Exception:
        def fallback_wsgi(environ, start_response):
            status = '500 Internal Server Error'
            headers = [('Content-Type', 'text/html; charset=utf-8')]
            start_response(status, headers)
            msg = (
                f"<html><head><title>Fatal Error</title></head>"
                f"<body style='font-family: monospace; background: #0f172a; color: #f87171; padding: 2rem;'>"
                f"<h2>Fatal Python Import Failure</h2>"
                f"<pre style='background: #1e293b; color: #f1f5f9; padding: 1.5rem; border-radius: 8px;'>{err_trace}</pre>"
                f"</body></html>"
            )
            return [msg.encode('utf-8')]
        app = fallback_wsgi

# Vercel WSGI entrypoint supports both 'app' and 'handler'
handler = app

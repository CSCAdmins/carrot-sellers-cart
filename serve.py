#!/usr/bin/env python3
"""
Simple static file server for MkDocs site using Starlette and Uvicorn.
"""
import os
from pathlib import Path

from starlette.applications import Starlette
from starlette.responses import FileResponse, HTMLResponse
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from starlette.middleware.gzip import GZipMiddleware

# Get the site directory
SITE_DIR = Path(os.getenv("SITE_DIR", "site"))

# Create Starlette app
app = Starlette()

# Add gzip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Serve static files
if SITE_DIR.exists():
    app.mount("/", StaticFiles(directory=str(SITE_DIR), html=True), name="static")
else:
    # If site directory doesn't exist, show error
    @app.route("/")
    async def homepage(request):
        return HTMLResponse(
            f"""
            <html>
            <body style="font-family: system-ui; padding: 2rem; max-width: 600px; margin: 0 auto;">
                <h1>Site Not Built</h1>
                <p>The MkDocs site has not been built yet.</p>
                <p>Run <code>mkdocs build</code> to generate the site.</p>
                <p style="color: #666; margin-top: 2rem;">
                    Looking for: {SITE_DIR.absolute()}
                </p>
            </body>
            </html>
            """,
            status_code=503
        )

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", "8080"))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"Starting server at http://{host}:{port}")
    print(f"Serving files from: {SITE_DIR.absolute()}")
    
    uvicorn.run(app, host=host, port=port, log_level="info")
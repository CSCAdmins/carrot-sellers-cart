#!/bin/bash
# Temporary server start script while container issues are resolved

set -e

echo "🥕 Starting Carrot Sellers site (direct mode)..."
echo ""
echo "NOTE: Container build is currently experiencing issues."
echo "Running server directly instead."
echo ""

# Check if site is built
if [ ! -d "site" ]; then
    echo "Building site first..."
    if [ -d ".venv" ]; then
        source .venv/bin/activate
    else
        uv venv
        source .venv/bin/activate
    fi
    
    uv pip install mkdocs mkdocs-material mkdocs-material-extensions mkdocs-macros-plugin pymdown-extensions Pygments uvicorn starlette
    mkdocs build
fi

# Start server
echo ""
echo "✅ Starting server at http://localhost:8080"
echo ""
echo "Press Ctrl+C to stop"
echo ""

if [ -d ".venv" ]; then
    source .venv/bin/activate
    python serve.py
else
    uv run --no-project --with uvicorn --with starlette python serve.py
fi
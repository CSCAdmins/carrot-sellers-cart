#!/bin/bash
# Run the site locally without containers

set -e

echo "🥕 Starting Carrot Sellers site locally..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    uv venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
uv pip install mkdocs mkdocs-simple-blog mkdocs-material mkdocs-material-extensions pymdown-extensions Pygments uvicorn starlette mkdocs-macros-plugin

# Build the site
echo "Building site..."
mkdocs build

# Start the server
echo ""
echo "✅ Starting server at http://localhost:8080"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python serve.py
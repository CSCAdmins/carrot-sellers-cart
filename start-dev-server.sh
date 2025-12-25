#!/bin/bash
# Start development server

echo "🥕 Starting Carrot Sellers development server..."
echo ""

# Activate virtual environment and start server
source .venv/bin/activate
exec python serve.py
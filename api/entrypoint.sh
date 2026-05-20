#!/bin/bash
# Copy source files into volume-mounted directories
# (volumes override files copied during Docker build)

# Data generation script
cp -f /app/_static/generate_data.py /app/data/generate_data.py 2>/dev/null || true
touch /app/data/__init__.py

# ML scripts
cp -rn /app/_static_ml/*.py /app/ml/ 2>/dev/null || true
touch /app/ml/__init__.py

# Ensure directories exist
mkdir -p /app/data/raw /app/data/processed /app/ml/models

# Start the API server
exec uvicorn api.main:app --host 0.0.0.0 --port 8000 --log-level info

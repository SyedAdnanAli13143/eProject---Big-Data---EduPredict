FROM python:3.11-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY api/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code to static locations (safe from volume mounts)
COPY data/generate_data.py /app/_static/generate_data.py
COPY ml/ /app/_static_ml/

# Also copy to working locations (may be overridden by volumes)
COPY ml/ /app/ml/
COPY ingestion/config.py /app/ingestion/config.py
COPY api/ /app/api/

# Create directories
RUN mkdir -p /app/data/raw /app/data/processed /app/ml/models

# Entrypoint copies static files into volumes then starts server
RUN chmod +x /app/api/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/api/entrypoint.sh"]

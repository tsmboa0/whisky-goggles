FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
COPY requirements.lock.txt .
RUN pip install -r requirements.txt

# Copy backend and model assets
COPY app/ ./app/
COPY data/ ./data/
COPY yolov8n.pt .

# Copy static frontend
COPY frontend/dist/ ./frontend/dist/

# Optionally include example env and scripts
COPY scripts/ ./scripts/
COPY .env.example .

# Expose port
EXPOSE 8000

# Launch API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

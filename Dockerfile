# Dockerfile
FROM python:3.13.0-slim

WORKDIR /app

# Install FFmpeg for yt_dlp postprocessing
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files, including cookies.txt
COPY . .
COPY cookies.txt /app/cookies.txt

# Start FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]

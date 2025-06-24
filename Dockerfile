# Dockerfile
FROM python:3.13.0-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Optional: declare env var path (for clarity)
ENV COOKIE_PATH=/app/cookies.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]

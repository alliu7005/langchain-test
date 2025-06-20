FROM python:3.11-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

ENV MODEL="gemma:2b"
ENV HOST=http://104.155.143.96

ENV AGENT_ID="music-agent-365383383851"
ENV AUTH_SERVER="https://spotify-oauth-365383383851.us-central1.run.app"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
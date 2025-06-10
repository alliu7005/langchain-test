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

ENV OLLAMA_MODEL="gemma:2b"
ENV OLLAMA_HOST=https://ollama-server-365383383851.us-central1.run.app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
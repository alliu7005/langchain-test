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
ENV OLLAMA_HOST=http://104.155.143.96

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
FROM ollama/ollama:latest

ENV OLLAMA_MODEL="gemma:2b"
ARG OLLAMA_MODEL="gemma:2b"
RUN ollama serve & \
    PID=$! && \
    echo "⏳ waiting for Ollama to start…" && \
    sleep 10 && \
    echo "⏳ pulling model ${OLLAMA_MODEL}…" && \
    ollama pull "${OLLAMA_MODEL}" && \
    echo "✅ pulled ${OLLAMA_MODEL}" && \
    kill $PID && \
    wait $PID || true
    
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
EXPOSE 8080
# Start the server when the container launches
ENTRYPOINT ["/entrypoint.sh"]
#!/usr/bin/env bash
set -e

: "${PORT:=8080}"
export OLLAMA_HOST="0.0.0.0:${PORT}"
ollama serve
#!/usr/bin/env bash
set -euo pipefail

# Start or update the shared Ollama service
docker compose -f docker-compose.ollama.yml up -d
docker ps --filter "name=ollama"

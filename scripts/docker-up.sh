#!/usr/bin/env bash
set -euo pipefail

# Ensure shared Ollama is running first (optional but nice)
pushd .. >/dev/null
./scripts/ollama-up.sh || true
popd >/dev/null

# docker compose up -d
# docker compose ps

# Bring up API and CLI services

docker compose up -d scope-api

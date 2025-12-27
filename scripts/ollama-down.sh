#!/usr/bin/env bash
set -euo pipefail

# Stop the shared Ollama container (keep models volume)
docker stop ollama || true

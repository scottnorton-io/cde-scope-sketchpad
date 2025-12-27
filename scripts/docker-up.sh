# docker-up.sh
#!/usr/bin/env bash
set -euo pipefail

# Bring up API and CLI services

docker compose up -d scope-api

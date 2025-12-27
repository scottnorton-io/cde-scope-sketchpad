# docker-up-with-web.sh
#!/usr/bin/env bash
set -euo pipefail

# Bring up API, CLI, and Web UI

docker compose -f docker-compose.yml -f docker-compose.web.yml up -d scope-api scope-web

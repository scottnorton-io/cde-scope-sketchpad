# docker-reset.sh
#!/usr/bin/env bash
set -euo pipefail

# Tear down containers and remove sessions volume contents.
# WARNING: This will delete all generated session artifacts.

docker compose -f docker-compose.yml -f docker-compose.web.yml down

rm -rf sessions/*
mkdir -p sessions

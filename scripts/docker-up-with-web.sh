#!/usr/bin/env bash
set -euo pipefail

docker compose -f docker-compose.yml -f docker-compose.web.yml down --rmi local
docker compose -f docker-compose.yml -f docker-compose.web.yml build --no-cache
docker compose -f docker-compose.yml -f docker-compose.web.yml up -d scope-api scope-web

# Bring up API, CLI, and Web UI

# docker compose -f docker-compose.yml -f docker-compose.web.yml up -d scope-api scope-web

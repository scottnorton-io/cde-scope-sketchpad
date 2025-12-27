#!/usr/bin/env bash
set -euo pipefail

# docker compose down

# Stop all containers for this project (no volume removal)

docker compose -f docker-compose.yml -f docker-compose.web.yml down

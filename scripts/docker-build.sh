#!/usr/bin/env bash
set -euo pipefail

# docker compose build --no-cache

# Build all images defined in docker-compose files

docker compose build

docker compose -f docker-compose.yml -f docker-compose.web.yml build

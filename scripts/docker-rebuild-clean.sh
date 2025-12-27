#!/usr/bin/env bash
set -euo pipefail

docker compose down --rmi local
docker compose build --no-cache
docker compose up -d

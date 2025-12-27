# docker-down.sh
#!/usr/bin/env bash
set -euo pipefail

# Stop all containers for this project (no volume removal)

docker compose -f docker-compose.yml -f docker-compose.web.yml down

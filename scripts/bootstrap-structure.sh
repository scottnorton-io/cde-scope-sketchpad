#!/usr/bin/env bash
set -euo pipefail

# Create directories
mkdir -p scope_cli scope_api scope_web sessions examples docs

# __init__.py for Python packages
touch scope_cli/__init__.py
touch scope_api/__init__.py
touch scope_web/__init__.py

# Keep docs and sessions directories in git
touch docs/.gitkeep
touch sessions/.gitkeep

# Basic .gitignore if not present
if [ ! -f .gitignore ]; then
  cat > .gitignore <<'EOF'
__pycache__/
*.py[cod]
*.log

.venv/
.env

sessions/*
!.gitkeep

.DS_Store
EOF
fi

echo "Scaffold created: packages, .gitkeep files, and .gitignore."

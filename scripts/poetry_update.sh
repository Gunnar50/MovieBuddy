#!/bin/bash
#
# Update poetry dependencies for a service.

# Set some failure conditions
set -o errexit   # Fail on any error
set -o pipefail  # Trace ERR through pipes
set -o errtrace  # Trace ERR through sub-shell commands

echo "Updating dependencies..."
poetry update

echo "Generating requirements.txt file..."
poetry export > requirements.txt
poetry export --with dev > requirements-dev.txt

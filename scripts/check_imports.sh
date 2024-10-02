#!/bin/bash
#
# Check imports for a service.

# Set some failure conditions
set -o errexit   # Fail on any error
set -o pipefail  # Trace ERR through pipes
set -o errtrace  # Trace ERR through sub-shell commands

# Check/fix the imports
./scripts/poetry_run.sh isort . --skip .pytype $@

#!/bin/bash
#
# Run tests for a service.

# Set some failure conditions
set -o errexit   # Fail on any error
set -o pipefail  # Trace ERR through pipes
set -o errtrace  # Trace ERR through sub-shell commands

 ../scripts/poetry_run.sh pytest --disable-warnings $@

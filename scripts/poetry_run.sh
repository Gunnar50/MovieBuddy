#!/bin/bash
#
# Execute a command using poetry (after checking that the env has been setup)

# Set some failure conditions
set -o errexit   # Fail on any error
set -o pipefail  # Trace ERR through pipes
set -o errtrace  # Trace ERR through sub-shell commands

if type poetry  > /dev/null 2>&1; then
  if [[ -z "$(poetry env list)" ]]; then
    echo "Setting up poetry env..."
    ../scripts/poetry_install.sh
  fi

  poetry run $@
else
  $@
fi

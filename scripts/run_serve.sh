#!/bin/bash

# Set some failure conditions
set -o errexit   # Fail on any error
set -o pipefail  # Trace ERR through pipes
set -o errtrace  # Trace ERR through sub-shell commands

export SERVE="true"

dev_appserver.py \
    app.yaml \
    --application=moviebuddy-437608 \
    --enable_console \
    --support_datastore_emulator=False

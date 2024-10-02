#!/bin/bash
#
# Install dependencies for a service.

# Set some failure conditions
set -o errexit   # Fail on any error
set -o pipefail  # Trace ERR through pipes
set -o errtrace  # Trace ERR through sub-shell commands

poetry env list | while read LINE ; do
  VERSION="${LINE%" (Activated)"}"
  echo "Removing old env... ${VERSION}"
  poetry env remove "${VERSION}"
done

echo "Upgrading virtualenv wheels (mostly for pip)..."
virtualenv --upgrade-embed-wheels

# Ensure the correct (pyenv) Python version is used
poetry config virtualenvs.prefer-active-python true

echo "Installing dependencies..."
poetry install

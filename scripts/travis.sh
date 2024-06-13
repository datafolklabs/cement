#!/bin/bash
set -e

docker-compose up -d mailpit 2>&1 >/dev/null

sleep 10

rm -f .coverage
pdm venv create $PYTHON_VERSION
pdm install
make test

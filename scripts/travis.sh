#!/bin/bash
set -e

rm -f .coverage
pip install -r requirements-dev.txt
make test

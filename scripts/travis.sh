#!/bin/bash
set -e

# removed - 3.7 is EOL: https://github.com/datafolklabs/cement/issues/658
# fix for Python 3.7 on Travis
# https://travis-ci.community/t/build-error-for-python-3-7-on-two-different-projects/12895/3
# pip install -U importlib_metadata

docker-compose up -d mailpit 2>&1 >/dev/null

sleep 10

rm -f .coverage
pip install -r requirements-dev.txt
make test

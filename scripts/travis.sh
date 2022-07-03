#!/bin/bash
set -e

# fix for Python 3.7 on Travis
# https://travis-ci.community/t/build-error-for-python-3-7-on-two-different-projects/12895/3
pip install -U importlib_metadata

rm -f .coverage
pip install -r requirements-dev.txt
make test

#!/bin/bash
set -e

export REDIS_HOST=localhost
export MEMCACHED_HOST=localhost

rm -f .coverage
pip install -r requirements-dev.txt
make test

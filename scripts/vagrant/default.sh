#!/bin/bash

sudo apt-get update && \
sudo apt-get upgrade -y && \
sudo apt-get dist-upgrade -y && \
sudo apt-get install -y \
    python \
    python-dev \
    python-pip \
    python-virtualenv \
    python3 \
    python3-dev \
    python3-pip \
    memcached \
    libmemcached-dev \
    zlib1g-dev

PY3_VER=$(python -c 'import sys; print("%s.%s" % (sys.version_info[0], sys.version_info[1]))')
virtualenv ~/.env/cement
pip-${PY3_VER} install virtualenv
virtualenv-${PY3_VER} ~/.env/cement-py3
memcached &


#!/bin/bash

cd /vagrant

sudo apt-get update && \
sudo apt-get upgrade -y && \
sudo apt-get dist-upgrade -y && \
sudo apt-get install -y \
    python \
    python-dev \
    python-pip \
    python3 \
    python3-dev \
    python3-pip \
    memcached \
    libmemcached-dev \
    zlib1g-dev \
    docker.io

sudo apt-get autoremove -y 

# for docker stuff
sudo usermod -aG docker vagrant
sudo pip install -U fig

PY3_VER=$(python3 -c 'import sys; print("%s.%s" % (sys.version_info[0], sys.version_info[1]))')
sudo pip install virtualenv
virtualenv ~/.env/cement
sudo pip3 install virtualenv
virtualenv-${PY3_VER} ~/.env/cement-py3

# for tests
killall memcached
memcached &

deactivate ||:

source ~/.env/cement/bin/activate
pip install -r requirements-dev-linux.txt
python setup.py develop

source ~/.env/cement-py3/bin/activate
pip install -r requirements-dev-py3-linux.txt
python setup.py develop


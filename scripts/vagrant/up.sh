#!/bin/bash
set -e

cd /vagrant

export DEBIAN_FRONTEND=noninteractive

sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get dist-upgrade -y

sudo apt-get install -y apt-transport-https ca-certificates software-properties-common

sudo apt-get update

sudo apt-get install -y \
    python \
    python3 \
    python-dev \
    python3-dev \
    python-pip \
    python3-pip \
    python-virtualenv \
    memcached \
    libmemcached-dev \
    zlib1g-dev

sudo apt-get autoremove -y
sudo pip3 install virtualenv

virtualenv --python=$(which python2) /vagrant/.env/cement-py2
virtualenv --python=$(which python3) /vagrant/.env/cement

# for tests
sudo /etc/init.d/memcached stop
sudo /etc/init.d/memcached start

deactivate ||:

source /vagrant/.env/cement-py2/bin/activate
pip install -r requirements-dev.txt
python setup.py develop
deactivate

source /vagrant/.env/cement/bin/activate
pip install -r requirements-dev.txt
python setup.py develop
deactivate

cat >>~/.bashrc <<EOF
export PS1="\[\e[0;33m\]\u@\h \[\e[1;35m\]\W\[\e[0m\] \[\e[0m\]\$ "
cd /vagrant
EOF

exit 0

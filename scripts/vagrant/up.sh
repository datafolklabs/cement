#!/bin/bash
set -e

cd /vagrant

export DEBIAN_FRONTEND=noninteractive

sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get dist-upgrade -y
sudo apt-get install -y apt-transport-https ca-certificates
sudo apt-key adv \
    --keyserver hkp://p80.pool.sks-keyservers.net:80 \
    --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
sudo add-apt-repository \
    -y "deb https://apt.dockerproject.org/repo ubuntu-trusty main"
sudo apt-get update
sudo apt-cache policy docker-engine

sudo apt-get install -y \
    python \
    python-pip \
    python-dev \
    python-virtualenv \
    python3 \
    python3-dev \
    python3-pip \
    memcached \
    libmemcached-dev \
    zlib1g-dev \
    docker-engine

sudo apt-get autoremove -y 
sudo pip3 install virtualenv

# for docker stuff
sudo usermod -aG docker vagrant

### fix me - install docker-compose here

python /usr/bin/virtualenv /vagrant/.env/cement-py2
python3 /usr/bin/virtualenv /vagrant/.env/cement

# for tests
sudo /etc/init.d/memcached stop
sudo /etc/init.d/memcached start

deactivate ||:

source /vagrant/.env/cement-py2/bin/activate 
pip install -r requirements-dev-linux.txt
python setup.py develop
deactivate

source /vagrant/.env/cement/bin/activate
pip install -r requirements-dev-py3-linux.txt
python setup.py develop
deactivate

cat >>~/.bashrc <<EOF
export PS1="\[\e[0;33m\]\u@\h \[\e[1;35m\]\W\[\e[0m\] \[\e[0m\]\$ "
cd /vagrant
EOF

exit 0


#!/bin/bash
set -e
set -x

cd /vagrant

function bail {
    echo $1
    exit 1
}

### first determine distro

if [ -f "/etc/os-release" ]; then
    DISTRO=$(grep "^ID=" /etc/os-release | sed 's/ID=//' | sed 's/\"//g')
elif [ -f "/etc/redhat-release" ]; then
    rel=$(cat /etc/redhat-release | awk {' print $1 '})
    if [ "$rel" = "CentOS" ]; then
        DISTRO="centos"
    elif [ "$rel" = "Red" ]; then
        DISTRO='redhat'
    else
        bail "Unsupported Distro"
    fi
else
    bail "Unsupported Distro"
fi

case "$DISTRO" in
    ubuntu|debian)
        export DEBIAN_FRONTEND=noninteractive
        DISTRO_VERSION=$(grep "^VERSION_ID=" /etc/os-release \
                        | sed 's/VERSION_ID=//' \
                        | sed 's/\"//g')
        DISTRO_MAJOR_VERSION=$(echo $DISTRO_VERSION | awk -F . {' print $1 '})
        DISTRO_MINOR_VERSION=$(echo $DISTRO_VERSION | awk -F . {' print $2 '})
        ;;

    centos|redhat|fedora)
        # Newer versions like CentOS 7+
        if [ -f "/etc/os-release" ]; then
            DISTRO_VERSION=$(grep "^VERSION_ID=" /etc/os-release \
                            | sed 's/VERSION_ID=//' \
                            | sed 's/\"//g')
            DISTRO_MAJOR_VERSION=$(echo $DISTRO_VERSION | awk -F . {' print $1 '})
            DISTRO_MINOR_VERSION=$(echo $DISTRO_VERSION | awk -F . {' print $2 '})
        else
            DISTRO_VERSION=$(cat /etc/redhat-release | awk {' print $3 '})
            DISTRO_MAJOR_VERSION=$(echo $DISTRO_VERSION | awk -F . {' print $1 '})
            DISTRO_MINOR_VERSION=$(echo $DISTRO_VERSION | awk -F . {' print $2 '})
        fi
        ;;

    *)
        DISTRO_VERSION=$(grep "^VERSION_ID=" /etc/os-release \
                        | sed 's/VERSION_ID=//' \
                        | sed 's/\"//g')
        DISTRO_MAJOR_VERSION=$(echo $DISTRO_VERSION | awk -F . {' print $1 '})
        DISTRO_MINOR_VERSION=$(echo $DISTRO_VERSION | awk -F . {' print $2 '})
        ;;
esac

export DISTRO_VERSION
export DISTRO_MAJOR_VERSION
export DISTRO_MINOR_VERSION


### do work

case "$DISTRO" in
    ubuntu|debian)
        sudo apt-get update
        sudo apt-get install -y \
            apt-transport-https \
            ca-certificates \
            software-properties-common

        sudo apt-get update
        sudo apt-get upgrade -y
        sudo apt-get dist-upgrade -y
        sudo apt-get install -y \
            python3 \
            python3-dev \
            python3-pip \
            redis-server \
            redis-tools \
            memcached \
            libmemcached-dev \
            zlib1g-dev

        sudo apt-get autoremove -y
        sudo pip3 install virtualenv
        ;;

    *)
        bail "Unsupported Distro"
        ;;

esac

# for tests

sudo systemctl restart memcached
sudo systemctl restart redis

/vagrant/env/bin/pip install -r requirements-dev.txt
/vagrant/env/bin/python setup.py develop

cat >>~/.bashrc <<EOF
export PS1="\[\e[0;33m\]\u@\h \[\e[1;35m\]\W\[\e[0m\] \[\e[0m\]\$ "
EOF

exit 0

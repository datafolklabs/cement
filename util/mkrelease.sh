#!/bin/bash

version=$(python -c "from pkg_resources import get_distribution ; print get_distribution('cement.core').version")
dir=~/cement-${version}

if [ -e "${version}" ]; then
    echo "release dir already exists $dir"
fi

mkdir $dir
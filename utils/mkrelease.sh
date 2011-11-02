#!/bin/bash

status=$(git status --porcelain)
version=$(cat src/cement2/setup.py | grep VERSION | head -n1 | awk -F \' {' print $2 '})
short=$(echo $version | awk -F . {' print $1"."$2 '})
dir=~/cement2-${version}

if [ "${status}" != "" ]; then
    echo
    echo "WARNING: not all changes committed"
fi

mkdir ${dir}
mkdir ${dir}/doc
mkdir ${dir}/downloads
mkdir ${dir}/pypi

# all
git archive HEAD --prefix=cement2-${version}/ | gzip > ${dir}/downloads/cement2-${version}.tar.gz

# individual
for i in cement2 cement2.ext.configobj cement2.ext.json cement2.ext.yaml; do
    pushd src/$i
    git archive HEAD --prefix=${i}-${version}/ | gzip > ${dir}/pypi/${i}-${version}.tar.gz
    popd
done

sphinx-build doc/source ${dir}/doc


#!/bin/bash

status=$(git status --porcelain)
version='1.0.0'
short=$(echo $version | awk -F . {' print $1"."$2 '})
dir=~/cement-${version}

if [ "${status}" != "" ]; then
    echo
    echo "WARNING: not all changes committed"
fi

mkdir ${dir}
mkdir ${dir}/doc
mkdir ${dir}/downloads
mkdir ${dir}/pypi

# all
git archive HEAD --prefix=cement-${version}/ | gzip > ${dir}/downloads/cement-${version}.tar.gz

# individual
for i in cement cement.devtools cement.test; do
    pushd src/$i
    git archive HEAD --prefix=${i}-${version}/ | gzip > ${dir}/pypi/${i}-${version}.tar.gz
    popd
done

sphinx-build doc/source ${dir}/doc


#!/bin/bash

if [ -z $1 ]; then
    echo 'a version argument is required.'
    exit 1
fi

SOURCES="cement \
         cement.ext.configobj \
         cement.ext.json \
         cement.ext.yaml \
         cement.ext.memcached \
         cement.ext.genshi"

#status=$(git status --porcelain)
#version=$(cat src/cement/setup.py | grep VERSION | head -n1 | awk -F \' {' print $2 '})
version=$1

res=$(git tag | grep $version)
if [ $? != 0 ]; then
    echo "Git tag ${version} does not exist."
    exit
fi

short=$(echo $version | awk -F . {' print $1"."$2 '})
dir=~/cement-${version}
tmpdir=$(mktemp -d -t cement-$version)

#if [ "${status}" != "" ]; then
#    echo
#    echo "WARNING: not all changes committed"
#fi

mkdir ${dir}
mkdir ${dir}/doc
mkdir ${dir}/source
mkdir ${dir}/pypi

# all
git archive ${version} --prefix=cement-${version}/ | gzip > ${dir}/source/cement-${version}.tar.gz
cp -a ${dir}/source/cement-${version}.tar.gz $tmpdir/

# individual
for i in $SOURCES; do
    pushd src/$i
    git archive ${version} --prefix=${i}-${version}/ | gzip > ${dir}/pypi/${i}-${version}.tar.gz
    popd
done

pushd $tmpdir
    tar -zxvf cement-${version}.tar.gz
    pushd cement-${version}/
        sphinx-build doc/source ${dir}/doc
    popd
popd


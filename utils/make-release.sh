#!/bin/bash

if [ -z $1 ]; then
    echo 'a version argument is required.'
    exit 1
fi

SOURCES="cement2 \
         cement2.ext.configobj \
         cement2.ext.json \
         cement2.ext.yaml \
         cement2.ext.memcached \
         cement2.ext.genshi"

#status=$(git status --porcelain)
#version=$(cat src/cement2/setup.py | grep VERSION | head -n1 | awk -F \' {' print $2 '})
version=$1

res=$(git tag | grep $version)
if [ $? != 0 ]; then
    echo "Git tag ${version} does not exist."
    exit
fi

short=$(echo $version | awk -F . {' print $1"."$2 '})
dir=~/cement2-${version}
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
git archive ${version} --prefix=cement2-${version}/ | gzip > ${dir}/source/cement2-${version}.tar.gz
cp -a ${dir}/source/cement2-${version}.tar.gz $tmpdir/

# individual
for i in $SOURCES; do
    pushd src/$i
    git archive ${version} --prefix=${i}-${version}/ | gzip > ${dir}/pypi/${i}-${version}.tar.gz
    popd
done

pushd $tmpdir
    tar -zxvf cement2-${version}.tar.gz
    pushd cement2-${version}/
        sphinx-build doc/source ${dir}/doc
    popd
popd


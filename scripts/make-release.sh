#!/bin/bash

if [ -z $1 ]; then
    echo 'a version argument is required.'
    exit 1
fi

version=$1

res=$(git tag | grep $version)
if [ $? != 0 ]; then
    echo "Git tag ${version} does not exist."
    exit
fi

short=$(echo $version | awk -F . {' print $1"."$2 '})
dir=~/cement-${version}
tmpdir=$(mktemp -d -t cement-$version)

mkdir ${dir}
mkdir ${dir}/doc
mkdir ${dir}/source

# run tests
python setup.py nosetests
if [ $? != 0 ]; then
    echo "Tests fail!"
    exit 1
fi

# all
git archive ${version} --prefix=cement-${version}/ | gzip > ${dir}/source/cement-${version}.tar.gz
cp -a ${dir}/source/cement-${version}.tar.gz $tmpdir/

pushd $tmpdir
    tar -zxvf cement-${version}.tar.gz
    pushd cement-${version}/
        sphinx-build doc/source ${dir}/doc
    popd
popd


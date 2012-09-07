#!/bin/bash

if [ -z $1 ]; then
    echo 'a version argument is required.'
    exit 1
fi

version=$1

res=$(git tag | grep $version)
if [ $? != 0 ]; then
    echo -n "Verifying Git Tag: "
    echo "FAIL"
    exit 1
fi

short=$(echo $version | awk -F . {' print $1"."$2 '})
dir=~/cement-${version}
tmpdir=$(mktemp -d -t cement-$version)

echo
echo "Generating ${dir}"
echo '-----------------------------------------------------------------------'

echo -n "Creating Destination Directory: "
if [ -e ${dir} ]; then
    echo "FAIL (already exists)"
    exit 1
else
    mkdir -p ${dir}
    mkdir -p ${dir}/doc
    mkdir -p ${dir}/source
    echo "OK"
fi

echo -n "Running Nose Tests: "
python setup.py nosetests --verbosity 0 2>/dev/null 1>/dev/null
if [ $? == 0 ]; then
    echo 'OK'
else
    echo "FAIL"
    exit 1
fi

echo -n "PEP8 Compliant: "
pep8 cement/ 2>/dev/null 1>/dev/null
if [ $? == 0 ]; then
    echo 'OK'
else
    echo 'FAIL'
    exit 1
fi
    

# all
echo -n "Generating Release Files: "
git archive ${version} --prefix=cement-${version}/ | gzip > ${dir}/source/cement-${version}.tar.gz
cp -a ${dir}/source/cement-${version}.tar.gz $tmpdir/
echo 'OK'

pushd $tmpdir >/dev/null
    tar -zxf cement-${version}.tar.gz
    pushd cement-${version}/ >/dev/null
        echo -n "Building Documentation: "
        sphinx-build -W doc/source ${dir}/doc 2>/dev/null 1>/dev/null
        if [ $? == 0 ]; then
            echo 'OK'
        else
            echo "FAIL"
            exit 1
        fi
    popd >/dev/null
popd >/dev/null

echo
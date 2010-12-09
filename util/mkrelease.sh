#!/bin/bash

status=$(git status --porcelain)
version=$(python -c "from pkg_resources import get_distribution ; print get_distribution('cement.core').version")
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
for i in core devtools test; do
    pushd src/cement.$i
    git archive HEAD --prefix=cement.${i}-${version}/ | gzip > ${dir}/pypi/cement.${i}-${version}.tar.gz
    popd
done

sphinx-build doc/source ${dir}/doc


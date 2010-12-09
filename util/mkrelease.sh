#!/bin/bash

previous=$(git describe | awk -F '-' {' print $1 '})
version=$(python -c "from pkg_resources import get_distribution ; print get_distribution('cement.core').version")
dir=~/cement-${version}
date=$(date)
tmpfile=$(mktemp /tmp/cementXXXXX)

if [ -e "${version}" ]; then
    echo "release dir already exists $dir"
fi

mkdir ${dir}/doc
mkdir ${dir}/download
mkdir ${dir}/pypi

git mv ChangeLog ChangeLog.orig
changes=$(git --no-pager log --pretty=" -  %s [%h]" ${previous}..)
cat >${tmpfile} <<EOF
#
# Tracker Issues and Commits referenced here can be viewed online as:
#
#   Commit: https://github.com/derks/cement/commit/XXXXXXX
#    Issue: https://github.com/derks/cement/issues/#issue/XX
#

${version} - $date
------------------------------------------------------------------------------
${changes}


EOF

vim ${tmpfile}
echo ${tmpfile}
#mv ${tmpfile} ChangeLog
#cat ChangeLog.orig | grep -v ^# >> ChangeLog

#!/bin/bash

previous=$(git describe | awk -F '-' {' print $1 '})
version=$(python -c "from pkg_resources import get_distribution ; print get_distribution('cement').version")
date=$(date)
tmpfile=$(mktemp /tmp/cementXXXXX)
status=$(git status --porcelain)

if [ "${status}" != "" ]; then
    echo
    echo "WARNING: not all changes committed"
fi

changes=$(git --no-pager log --pretty=" -  %s [%h]" ${previous}..)
cat <<EOF

${version} - $date
------------------------------------------------------------------------------
${changes}


EOF


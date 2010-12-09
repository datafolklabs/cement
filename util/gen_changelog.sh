#!/bin/bash

previous=$(git describe | awk -F '-' {' print $1 '})
version=$(python -c "from pkg_resources import get_distribution ; print get_distribution('cement.core').version")
date=$(date)
tmpfile=$(mktemp /tmp/cementXXXXX)
status=$(git status --porcelain)

if [ "${status}" != "" ]; then
    echo "must commit all changes first"
    exit 1
fi

changes=$(git --no-pager log --pretty=" -  %s [%h]" ${previous}..)
cat <<EOF
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


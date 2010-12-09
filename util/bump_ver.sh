#!/bin/bash

if [ -z $1 ]; then
    echo 'a version argument is required.'
    exit 1
fi

if [ -z $2 ]; then
    echo 'a release type is required (stable|dev)'
    exit 1
fi

full=$1
type=$2
major=$(echo $1 | awk -F . {' print $1"."$2 '})
uname=$(uname)

if [ "$uname" == "Darwin" ]; then
    sed -i '' "s/RELEASE = \'.*\'/RELEASE = '${full}'/g" doc/source/conf.py
    sed -i '' "s/VERSION = \'.*\'/VERSION = '${major}'/g" doc/source/conf.py
    find ./ -iname "setup.py" -exec sed -i '' "s/VERSION = '.*'/version = '${full}'/g" {} \;
elif [ "$uname" == "Linux" ]; then
    sed -i "s/RELEASE = \'.*\'/RELEASE = '${full}'/g" doc/source/conf.py
    sed -i "s/VERSION = \'.*\'/VERSION = '${major}'/g" doc/source/conf.py
    find ./ -iname "setup.py" -exec sed -i "s/VERSION = '.*'/version = '${full}'/g" {} \;
fi

mv ChangeLog ChangeLog.bak
date=$(date)

if [ "$type" == "stable" ]; then
    entry=" +  Stable Release ${full}"
else
    entry=" +  Development Release ${full}"
fi
    
cat >ChangeLog <<EOF

$full - $date
------------------------------------------------------------------------------

$entry

EOF

cat ChangeLog.bak >> ChangeLog && rm ChangeLog.bak
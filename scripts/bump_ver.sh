#!/bin/bash

if [ -z $1 ]; then
    echo 'a version argument is required.'
    exit 1
fi

full=$1
major=$(echo $1 | awk -F . {' print $1"."$2 '})
uname=$(uname)

if [ "$uname" == "Darwin" ]; then
    sed -i '' "s/RELEASE = \'.*\'/RELEASE = '${full}'/g" doc/source/conf.py
    sed -i '' "s/VERSION = \'.*\'/VERSION = '${major}'/g" doc/source/conf.py
    find ./ -iname "setup.py" -exec sed -i '' "s/VERSION = '.*'/VERSION = '${full}'/g" {} \;
elif [ "$uname" == "Linux" ]; then
    sed -i "s/RELEASE = \'.*\'/RELEASE = '${full}'/g" doc/source/conf.py
    sed -i "s/VERSION = \'.*\'/VERSION = '${major}'/g" doc/source/conf.py
    find ./ -iname "setup.py" -exec sed -i "s/VERSION = '.*'/VERSION = '${full}'/g" {} \;
fi
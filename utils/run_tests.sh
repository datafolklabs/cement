#!/bin/bash

SOURCES=" \
    src/cement2 \
    src/cement2.ext.configobj \
    src/cement2.ext.json \
    src/cement2.ext.yaml
    "

for path in $SOURCES; do
    pushd $path
        python setup.py develop
    popd
done

coverage erase
coverage run `which nosetests` --verbosity=3 $SOURCES

# This is a hack to wait for tests to run
sleep 5
echo; echo
coverage combine
coverage html

coverage report
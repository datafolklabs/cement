#!/bin/bash

rm -f .coverage
sed -i 's/with-coverage=1/with-coverage=0/g' setup.cfg

PYCHECK=$(python -c 'import sys; print(sys.version_info < (2, 7))')
if [ "$PYCHECK" == "True" ]; then
    pip install argparse
fi

PYCHECK=$(python -c 'import sys; print(sys.version_info > (3, 0))')
if [ "$PYCHECK" == "True" ]; then
    pip install -r requirements-dev-py3-linux.txt
else
    pip install -r requirements-dev-linux.txt
fi

python setup.py nosetests
exit $?

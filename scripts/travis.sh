#!/bin/bash

rm -f .coverage

PYCHECK=$(python -c 'import sys; print(sys.version_info < (2, 7))')
if [ "$PYCHECK" == "True" ]; then
    pip install argparse --use-mirrors
fi

PYCHECK=$(python -c 'import sys; print(sys.version_info > (3, 0))')
if [ "$PYCHECK" == "True" ]; then
    pip install -r requirements-dev-py3.txt --use-mirrors
else
    pip install -r requirements-dev.txt --use-mirrors
fi

python setup.py nosetests
exit $?

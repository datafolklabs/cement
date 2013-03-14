#!/bin/bash

PYCHECK=$(python -c 'import sys; print sys.version_info < (2, 7)')
if [ "$PYCHECK" == "True" ]; then
    pip install argparse --use-mirrors
fi

pip install coverage nose --use-mirrors
pip install -r requirements.txt --use-mirrors
pip install -r requirements-dev.txt --use-mirrors
python setup.py nosetests
exit $?

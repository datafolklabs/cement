#!/bin/bash

pip install argparse coverage nose --use-mirrors
pip install -r requirements.txt --use-mirrors
pip install -r requirements-dev.txt --use-mirrors
python setup.py nosetests
exit $?

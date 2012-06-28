#!/bin/bash

pip install argparse coverage nose --use-mirrors
pip install -r src/cement/requirements.txt --use-mirrors
pip install -r src/cement.ext.configobj/requirements.txt --use-mirrors
pip install -r src/cement.ext.json/requirements.txt --use-mirrors
pip install -r src/cement.ext.genshi/requirements.txt --use-mirrors
pip install -r src/cement.ext.yaml/requirements.txt --use-mirrors
pip install -r src/cement.ext.memcached/requirements.txt --use-mirrors
exit 0

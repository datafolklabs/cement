#!/bin/bash

pip install argparse coverage nose --use-mirrors
pip install -r src/cement2/requirements.txt --use-mirrors
pip install -r src/cement2.ext.configobj/requirements.txt --use-mirrors
pip install -r src/cement2.ext.json/requirements.txt --use-mirrors
pip install -r src/cement2.ext.genshi/requirements.txt --use-mirrors
pip install -r src/cement2.ext.yaml/requirements.txt --use-mirrors
pip install -r src/cement2.ext.memcached/requirements.txt --use-mirrors
exit 0
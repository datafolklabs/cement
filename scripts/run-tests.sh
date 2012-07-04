#!/bin/bash
         
pip install nose coverage
python setup.py develop

rm -rf coverage_html
coverage erase
python setup.py nosetests
RET=$?

exit $RET

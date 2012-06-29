#!/bin/bash
         
pip install nose coverage
python setup.py develop

rm -rf coverage_html
coverage erase
python setup.py nosetests

#coverage run `which nosetests` --verbosity=3
RET=$?

#coverage html
#coverage report
exit $RET


import os    
import sys
import hashlib
import shutil
import random
from tempfile import mkdtemp
from datetime import datetime
from nose.tools import raises, with_setup

from cement import namespaces
from cementtest.core.config import get_nose_config        
from cementtest.core.appmain import nose_main
from cementtest.core.exc import CementTestRuntimeError

global tempdir, config
tempdir = mkdtemp()
config = get_nose_config(tempdir)

args = []
args.append(__file__)
args.append('nose_tests')
nose_main([__file__, 'nosetests'], config)

            
def setup_func():
    "set up test fixtures"
    pass
    
def teardown_func():
    "tear down test fixtures"    
    global tempdir, config
    
    if os.path.exists(tempdir):
        shutil.rmtree(tempdir)

@with_setup(setup_func, teardown_func)
def test_initialize():    
    pass
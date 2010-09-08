
"""The purpose of this module is to test bootstrapping functionality."""

import sys
import os
import shutil
from tempfile import mkdtemp
from nose.tools import raises, with_setup, eq_, ok_

from cement import namespaces
from cement.core.namespace import get_config
from cement.core.opt import parse_options
from cement.core.controller import run_controller_command

from cementtest.core.exc import CementTestArgumentError, CementTestRuntimeError

config = get_config()
def setup_func():
    "set up test fixtures"
    config['datadir'] = mkdtemp()
    
def teardown_func():
    "tear down test fixtures"    
    if os.path.exists(config['datadir']):
        shutil.rmtree(config['datadir'])
    
@with_setup(setup_func, teardown_func)
def test_import_install_plugin():  
    # example plugin is imported in root bootstrap, so it should have
    # a place in global namespaces
    ok_(namespaces.has_key('example'))

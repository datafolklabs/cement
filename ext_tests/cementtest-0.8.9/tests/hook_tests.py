
"""The purpose of this module is to test hook functionality."""

import sys
import os
import shutil
from tempfile import mkdtemp
from nose.tools import raises, with_setup, eq_, ok_

from cement import hooks
from cement.core.hook import run_hooks
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
def test_my_example_hook():  
    ok_(hooks.has_key('my_example_hook'))
    
    hook_results = []
    
    for res in run_hooks('my_example_hook'):
        hook_results.append(res)
    
    # return results are the weight of the hook and should be in numerical
    # order
    res = hook_results = [-100, 0, 99]
    ok_(res)



"""The purpose of this module is to test controller functionality."""

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
def test_example_namespace_cmd1():  
    sys.argv = [__file__, 'example', 'cmd1']
    (opts, args) = parse_options('example', ignore_conflicts=True)
    res = run_controller_command(sys.argv[1], sys.argv[2], 
                                 cli_opts=opts, cli_args=args)
    ok_(res, {'foo' : 'bar'})
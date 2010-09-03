
import sys
import os
import shutil
from tempfile import mkdtemp
from nose.tools import raises, with_setup, eq_

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
def test_config_options():  
    eq_(config['test_option'], 'foobar')

@with_setup(setup_func, teardown_func)
def test_config_options_per_cli_opts():  
    sys.argv = [__file__, 'nosetests', '--test-option=funions']
    (opts, args) = parse_options('root', ignore_conflicts=True)
    run_controller_command('root', sys.argv[1], cli_opts=opts, cli_args=args)
    eq_(config['test_option'], 'funions')

from nose.tools import raises, with_setup, eq_, ok_
from configobj import ConfigObj

from cement import namespaces
from cement.core.namespace import get_config
from cement.core.testing import simulate
from cement.core.configuration import ensure_api_compat, validate_config
from cement.core.configuration import get_api_version
from cement.core.configuration import t_f_pass, set_config_opts_per_file
from cement.core.exc import CementRuntimeError, CementConfigError

from cement_test.core.testing import setup_func, teardown_func
from cement_test.core.exc import CementTestArgumentError, CementTestRuntimeError

config = get_config()

@with_setup(setup_func, teardown_func)
def test_config_options():  
    eq_(config['test_option'], 'foobar')

@with_setup(setup_func, teardown_func)
def test_deprecated_api_version():  
    get_api_version()

@with_setup(setup_func, teardown_func)
def test_config_options_per_cli_opts():  
    args = ['cement-test', 'nosetests', '--test-option=funions']
    simulate(args)
    eq_(config['test_option'], 'funions')

@with_setup(setup_func, teardown_func)
def test_ensure_api_compat():
    # deprecated
    ensure_api_compat(__name__, 'xxxxx')

@raises(CementConfigError)
@with_setup(setup_func, teardown_func)
def test_validate_config_bad():
    dcf = ConfigObj() # default config    
    validate_config(dcf)

@with_setup(setup_func, teardown_func)
def test_t_f_pass():
    for val in ['true', 'True', True]:
        yield check_true, val

    for val in ['false', 'False', False]:
        yield check_false, val
    
    for val in ['a', 'Blah Hah', 100]:
        yield check_pass, val
        
def check_true(val):
    assert t_f_pass(val) == True

def check_false(val):
    assert t_f_pass(val) == False

def check_pass(val):
    assert t_f_pass(val) == val
    
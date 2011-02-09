"""The purpose of this module is to test logging functionality."""

from nose.tools import raises, with_setup, eq_, ok_

from cement import namespaces, hooks
from cement.core.log import setup_logging
from cement.core.namespace import get_config
from cement.core.testing import simulate
from cement.core.exc import CementRuntimeError, CementConfigError

from cement_test.core.testing import setup_func, teardown_func
from cement_test.core.exc import CementTestArgumentError, CementTestRuntimeError

config = get_config()
    
@with_setup(setup_func, teardown_func)
def test_setup_alternate_logging():
    namespaces['root'].config['debug'] = True
    setup_logging(clear_loggers=True, level='DEBUG', to_console=True)  
    
    namespaces['root'].config['debug'] = False
    setup_logging(clear_loggers=True, level='INFO', to_console=True)  
    
    namespaces['root'].config['log_max_bytes'] = 1024000
    namespaces['root'].config['log_level'] = 'warn'
    setup_logging()  

@with_setup(setup_func, teardown_func)
def test_setup_logging_per_config_file():
    namespaces['root'].config['logging_config_file'] = './config/cement-test-logging.conf'
    setup_logging()

@raises(CementConfigError)
@with_setup(setup_func, teardown_func)
def test_setup_logging_per_bogus_config_file():
    namespaces['root'].config['logging_config_file'] = 'bollox'
    setup_logging()
    
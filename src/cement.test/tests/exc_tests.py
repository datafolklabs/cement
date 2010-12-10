"""The purpose of this module is to test exception functionality."""

from nose.tools import raises, with_setup, eq_, ok_

from cement import namespaces
from cement.core.namespace import get_config
from cement.core.controller import expose
from cement.core.testing import simulate
from cement.core.exc import CementError, CementRuntimeError, CementConfigError
from cement.core.exc import CementArgumentError

from cement_test.core.testing import setup_func, teardown_func
from cement_test.core.exc import CementTestError, CementTestRuntimeError
from cement_test.core.exc import CementTestArgumentError, CementTestConfigError

config = get_config()
    
@raises(CementError)
@with_setup(setup_func, teardown_func)
def test_error():  
    raise CementError, 'this is a cement error'

@raises(CementRuntimeError)
@with_setup(setup_func, teardown_func)
def test_runtime_error():  
    raise CementRuntimeError, 'this is a cement error'

@raises(CementConfigError)
@with_setup(setup_func, teardown_func)
def test_config_error():  
    raise CementConfigError, 'this is a cement error'
    
@raises(CementArgumentError)
@with_setup(setup_func, teardown_func)
def test_argument_error():  
    raise CementArgumentError, 'this is a cement error'

@with_setup(setup_func, teardown_func)
def test_error_str_and_unicode():  
    try:
        raise CementError, 'this is a cement error'
    except CementError, e:
        eq_(e.__str__(), 'this is a cement error')
        eq_(e.__unicode__(), u'this is a cement error')
        
@raises(CementTestError)
@with_setup(setup_func, teardown_func)
def test_app_error():  
    raise CementTestError, 'this is a cement test error'

@raises(CementTestRuntimeError)
@with_setup(setup_func, teardown_func)
def test_app_runtime_error():  
    raise CementTestRuntimeError, 'this is a cement test error'

@raises(CementTestConfigError)
@with_setup(setup_func, teardown_func)
def test_app_config_error():  
    raise CementTestConfigError, 'this is a cement test error'
    
@raises(CementTestArgumentError)
@with_setup(setup_func, teardown_func)
def test_app_argument_error():  
    raise CementTestArgumentError, 'this is a cement test error'

@with_setup(setup_func, teardown_func)
def test_app_error_str_and_unicode():  
    try:
        raise CementTestError, 'this is a cement test error'
    except CementTestError, e:
        eq_(e.__str__(), 'this is a cement test error')
        eq_(e.__unicode__(), u'this is a cement test error')
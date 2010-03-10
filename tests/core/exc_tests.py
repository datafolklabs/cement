
import os
import shutil
from tempfile import mkdtemp
from configobj import ConfigObj
from nose.tools import with_setup, raises, eq_

from cement.core.exc import CementRuntimeError, CementConfigError
from cement.core.exc import CementArgumentError, CementError
from cement.core.exc import CementInternalServerError

from cement.core.controller import CementController

tmpdir = None

def setup_func():
    "set up test fixtures"
    global tmpdir
    tmpdir = mkdtemp()
    
def teardown_func():
    "tear down test fixtures"
    global tmpdir
    shutil.rmtree(tmpdir)

@raises(CementConfigError)
@with_setup(setup_func, teardown_func)
def test_exc_config_error():
    raise CementConfigError, 'test'
    
@raises(CementRuntimeError)
@with_setup(setup_func, teardown_func)
def test_exc_runtime_error():
    raise CementRuntimeError, 'test'

@raises(CementInternalServerError)
@with_setup(setup_func, teardown_func)
def test_exc_internal_server_error():
    raise CementInternalServerError, 'test'
        
@raises(CementArgumentError)
@with_setup(setup_func, teardown_func)
def test_exc_argument_error():
    raise CementArgumentError, 'test'
    
@with_setup(setup_func, teardown_func)
def test_exc_config_code():
    try:
        raise CementConfigError, 'test'
    except CementConfigError, e:
        eq_(e.code, 1010)
        
@with_setup(setup_func, teardown_func)
def test_exc_runtime_code():
    try:
        raise CementRuntimeError, 'test'
    except CementRuntimeError, e:
        eq_(e.code, 1020)

@with_setup(setup_func, teardown_func)
def test_exc_internal_server_code():
    try:
        raise CementInternalServerError, 'test'
    except CementInternalServerError, e:
        eq_(e.code, 1030)
            
@with_setup(setup_func, teardown_func)
def test_exc_argument_code():
    try:
        raise CementArgumentError, 'test'
    except CementArgumentError, e:
        eq_(e.code, 1040)

    


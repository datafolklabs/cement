
from configobj import ConfigObj
from nose.tools import raises, with_setup

from cement import hooks, namespaces, handlers
from cement.core.exc import CementConfigError
from cement.core.app_setup import lay_cement, define_default_hooks
from cement.core.app_setup import define_default_handler_types
from cement.core.app_setup import register_default_handlers

from cement_test.core.testing import setup_func, teardown_func
    
@with_setup(setup_func, teardown_func)
def test_defined_default_hooks():
    global hooks
    expected_hooks = [
        'options_hook', 'post_options_hook', 'validate_config_hook',
        'pre_plugins_hook', 'post_plugins_hook', 'post_bootstrap_hook'
        ]
    for hook_name in expected_hooks:
        yield check_hook, hook_name
    
def check_hook(hook_name):
    assert hooks.has_key(hook_name)

@with_setup(setup_func, teardown_func)
def test_defined_default_handler_types():
    global handlers
    expected_handler_types = [
        'output'
        ]
    for handler_type in expected_handler_types:
        yield check_handler_type, handler_type
    
def check_handler_type(handler_type):
    assert handlers.has_key(handler_type)

@with_setup(setup_func, teardown_func)
def test_registered_default_handlers():
    global handlers
    expected_output = [
        'genshi', 'json'
        ]
    for handler in expected_output:
        yield check_handler, 'output', handler
    
def check_handler(type, name):
    assert handlers[type].has_key(name)
    
# FIXME: How do you test lay_cement()?  Needs a full working (and installed)
# application.

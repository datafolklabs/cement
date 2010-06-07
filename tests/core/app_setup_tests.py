
from configobj import ConfigObj
from nose.tools import raises, with_setup

from cement import hooks, namespaces
from cement.core.exc import CementConfigError
from cement.core.app_setup import lay_cement, register_default_hooks

def setup_func():
    "set up test fixtures"
    pass
    
def teardown_func():
    "tear down test fixtures"
    pass
    
@with_setup(setup_func, teardown_func)
def test_register_default_hooks():
    global hooks
    register_default_hooks()
    expected_hooks = [
        'options_hook', 'post_options_hook', 'validate_config_hook',
        'pre_plugins_hook', 'post_plugins_hook', 'post_bootstrap_hook'
        ]
    for hook_name in expected_hooks:
        yield check_hook, hook_name
    
def check_hook(hook_name):
    assert hooks.has_key(hook_name)

# FIXME: How do you test lay_cement()?  Needs a full working (and installed)
# application.

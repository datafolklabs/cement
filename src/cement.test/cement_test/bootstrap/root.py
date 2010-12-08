"""
The bootstrap module should be used to setup parts of your application
that need to exist before all controllers are loaded.  It is best used to 
define hooks, setup namespaces, and the like.  The root namespace is 
already bootstrapped by Cement, however you can extend that functionality
by importing additional bootstrap files here.
"""

from cement.core.opt import init_parser
from cement.core.hook import register_hook, define_hook

define_hook('my_example_hook')

# Register root options
@register_hook()
def options_hook(*args, **kwargs):
    # This hook allows us to append options to the root namespace
    root_options = init_parser()
    root_options.add_option('-R', '--root-option', action ='store_true', 
        dest='root_option', default=None, help='Example root option') 
    root_options.add_option('--json', action='store_true',
        dest='enable_json', default=None, 
        help='render output as json (CLI-API)')
    root_options.add_option('--debug', action='store_true',
        dest='debug', default=None, help='toggle debug output')
    root_options.add_option('--quiet', action='store_true',
        dest='quiet', default=None, help='disable console logging')
    root_options.add_option('--test-option', action='store',
        dest='test_option', default=None, help='test option')
    return ('root', root_options)

@register_hook()
def post_bootstrap_hook():
    pass
    
@register_hook()
def validate_config_hook(config):
    pass
    
@register_hook()
def pre_plugins_hook():
    pass
    
#@register_hook(name='options_hook')
#def bogus_namespace():
#    parser = init_parser()
#    parser.add_option('--bogus-option', action='store', dest='bogus_option')
#    return ('bogus_namespace', parser)
    
@register_hook()
def post_plugins_hook():
    pass
    
@register_hook()
def post_options_hook(cli_opts, cli_args):
    pass
    
# Import all additional (non-plugin) bootstrap libraries here    
# 
#   from cement_test.bootstrap import example


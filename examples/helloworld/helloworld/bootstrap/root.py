"""
The bootstrap module should be used to setup parts of your application
that need to exist before all controllers are loaded.  It is best used to 
define hooks, setup namespaces, and the like.  The root namespace is 
already bootstrapped by Cement, however you can extend that functionality
by importing additional bootstrap files here.
"""

from cement.core.opt import init_parser
from cement.core.hook import register_hook

# Register root options
@register_hook()
def options_hook(*args, **kwargs):
    # This hook allows us to append options to the root namespace
    root_options = init_parser()
    root_options.add_option('-R', '--root-option', action ='store_true', 
        dest='root_option', default=None, help='Example root option') 
    root_options.add_option('--json', action='store_true',
        dest='enable_json', default=None, 
        help='render output as json (Cement CLI-API)')
    root_options.add_option('--yaml', action='store_true',
        dest='enable_yaml', default=None,
        help='render output as yaml (Cement CLI-API)')
    root_options.add_option('--debug', action='store_true',
        dest='debug', default=None, help='toggle debug output')
    root_options.add_option('--quiet', action='store_true',
        dest='quiet', default=None, help='disable console logging')
    return ('root', root_options)

# Import all additional (non-plugin) bootstrap libraries here    
# 
#   from helloworld.bootstrap import example
#
    
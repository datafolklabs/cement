"""
This module provides any dynamically loadable code for the YAML 
Framework Extension such as hook and handler registration.  Additional 
classes and functions exist in cement2.lib.ext_yaml.
    
"""

from ..core import handler, hook
from ..lib.ext_yaml import YamlOutputHandler

handler.register(YamlOutputHandler)

@hook.register()
def cement_post_setup_hook(app):
    """
    Adds the '--yaml' argument to the argument object.
    
    """
    app.args.add_argument('--yaml', dest='output_handler', 
        action='store_const', help='toggle yaml output handler', const='yaml')

@hook.register()
def cement_pre_run_hook(app):
    if '--yaml' in app._meta.argv:
        app._meta.output_handler = 'yaml'
        app._setup_output_handler()
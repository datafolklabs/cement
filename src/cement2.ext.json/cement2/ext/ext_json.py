"""
This module provides any dynamically loadable code for the JSON 
Framework Extension such as hook and handler registration.  Additional 
classes and functions exist in cement2.lib.ext_json.
    
"""

from cement2.core import handler, hook
from cement2.lib.ext_json import JsonOutputHandler

handler.register(JsonOutputHandler)
            
@hook.register()
def cement_post_setup_hook(app):
    """
    Adds the '--json' argument to the argument object.
    
    """
    app.args.add_argument('--json', dest='output_handler', 
        action='store_const', help='toggle json output handler', const='json')


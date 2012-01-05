"""
This module provides any dynamically loadable code for the Genshi 
Framework Extension such as hook and handler registration.  Additional 
classes and functions exist in cement2.lib.ext_genshi.
    
"""

from cement2.core import handler, hook
from cement2.lib.ext_genshi import GenshiOutputHandler

handler.register(GenshiOutputHandler)

@hook.register()
def cement_post_setup_hook(app):
    """
    Sets the default [genshi] config section options.
    
    """
    defaults = dict()
    defaults['genshi'] = dict()
    defaults['genshi']['template_module'] = "%s.templates" % app.name
    app.config.merge(defaults, override=False)
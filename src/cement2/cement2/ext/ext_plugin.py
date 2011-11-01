"""
This module provides any dynamically loadable code for the Cement Plugin 
Framework Extension such as hook and handler registration.  Additional 
classes and functions exist in cement2.lib.ext_plugin.
    
"""

from cement2.core import handler
from cement2.lib.ext_plugin import CementPluginHandler

handler.register(CementPluginHandler)
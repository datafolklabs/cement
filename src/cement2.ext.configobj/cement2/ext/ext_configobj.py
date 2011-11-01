"""
This module provides any dynamically loadable code for the ConfigObj 
Framework Extension such as hook and handler registration.  Additional 
classes and functions exist in cement2.lib.ext_configobj.
    
"""

from cement2.core import handler
from cement2.lib.ext_configobj import ConfigObjConfigHandler

handler.register(ConfigObjConfigHandler)
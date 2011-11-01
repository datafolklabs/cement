"""
This module provides any dynamically loadable code for the OptParse 
Framework Extension such as hook and handler registration.  Additional 
classes and functions exist in cement2.lib.ext_optparse.
    
"""

from cement2.core import handler
from cement2.lib.ext_optparse import OptParseArgumentHandler

handler.register(OptParseArgumentHandler)
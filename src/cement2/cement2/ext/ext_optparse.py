"""
This module provides any dynamically loadable code for the OptParse 
Framework Extension such as hook and handler registration.  Additional 
classes and functions exist in cement2.lib.ext_optparse.
    
"""

from ..core import handler
from ..lib.ext_optparse import OptParseArgumentHandler

handler.register(OptParseArgumentHandler)
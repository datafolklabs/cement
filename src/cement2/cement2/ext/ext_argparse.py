"""
This module provides any dynamically loadable code for the ArgParse 
Framework Extension such as hook and handler registration.  Additional 
classes and functions exist in cement2.lib.ext_argparse.
    
"""

from cement2.core import handler
from cement2.lib.ext_argparse import ArgParseArgumentHandler

handler.register(ArgParseArgumentHandler)
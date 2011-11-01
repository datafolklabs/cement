"""
This module provides any dynamically loadable code for the NullOutput 
Framework Extension such as hook and handler registration.  Additional 
classes and functions exist in cement2.lib.ext_nulloutput.
    
"""

from cement2.core import handler
from cement2.lib.ext_nulloutput import NullOutputHandler

handler.register(NullOutputHandler)
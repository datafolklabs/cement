"""
This module provides any dynamically loadable code for the Logging 
Framework Extension such as hook and handler registration.  Additional 
classes and functions exist in cement2.lib.ext_logging.
    
"""

from ..core import handler
from ..lib.ext_logging import LoggingLogHandler

handler.register(LoggingLogHandler)
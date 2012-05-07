"""
This module provides any dynamically loadable code for the Memcached
Framework Extension such as hook and handler registration.  Additional 
classes and functions exist in cement2.lib.ext_memcached.
    
"""

from ..core import handler
from ..lib.ext_memcached import MemcachedCacheHandler

handler.register(MemcachedCacheHandler)
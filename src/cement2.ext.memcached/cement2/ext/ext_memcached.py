"""
This module provides any dynamically loadable code for the Memcached
Framework Extension such as hook and handler registration.  Additional 
classes and functions exist in cement2.lib.ext_memcached.
    
"""

from cement2.core import handler, hook
from cement2.lib.ext_memcached import MemcachedCacheHandler

handler.register(MemcachedCacheHandler)

@hook.register(name='cement_post_setup_hook')
def fix_hosts(app):
    # FIX ME: This is a bit of a hack, but works around ConfigParser
    # unable to handle lists.
    hosts = app.config.get('cache.memcached', 'hosts')
    fixed_hosts = []

    if type(hosts) == str:
        parts = hosts.split(',')
        for part in parts:
            fixed_hosts.append(part.strip())
    app.config.set('cache.memcached', 'hosts', fixed_hosts)
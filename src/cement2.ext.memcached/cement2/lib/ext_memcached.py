"""Memcached Framework Extension Library."""

import sys
import pylibmc
from ..core import cache, backend

Log = backend.minimal_logger(__name__)

class MemcachedCacheHandler(cache.CementCacheHandler):
    """
    This class implements the :ref:`ICache <cement2.core.cache>` 
    interface.  It provides a caching interface using the 
    `pylibmc <http://sendapatch.se/projects/pylibmc/>`_ library.  
    
    """
    class Meta:
        interface = cache.ICache
        label = 'memcached'
        config_defaults = dict(
            hosts=['127.0.0.1'],
            expire_time=0,
            )
        
    def __init__(self, *args, **kw):
        super(MemcachedCacheHandler, self).__init__(*args, **kw)
        self.mc = None
    
    def _setup(self, *args, **kw):
        super(MemcachedCacheHandler, self)._setup(*args, **kw)

        # Work around because ConfigParser doesn't support Python types
        hosts = self._config('hosts')
        fixed_hosts = []

        if type(hosts) == str:
            parts = hosts.split(',')
            for part in parts:
                fixed_hosts.append(part.strip())
        elif type(hosts) == list:
            fixed_hosts = hosts
        self.app.config.set(self._meta.config_section, 'hosts', fixed_hosts)
        self.mc = pylibmc.Client(self._config('hosts'))
        
    def get(self, key, fallback=None, **kw):
        Log.debug("getting cache value using key '%s'" % key)
        res = self.mc.get(key, **kw)
        if res is None:
            return fallback
        else:
            return res
    
    def _config(self, key):
        return self.app.config.get(self._meta.config_section, key)
        
    def set(self, key, value, time=None, **kw):
        if time is None:
            time = int(self._config('expire_time'))
            
        self.mc.set(key, value, time=time, **kw)
    
    def delete(self, key, **kw):
        self.mc.delete(key, **kw)
    
    def purge(self, **kw):
        self.mc.flush_all(**kw)

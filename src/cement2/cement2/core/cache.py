"""Cement core cache module."""

from ..core import backend, exc, interface, handler

Log = backend.minimal_logger(__name__)

def cache_validator(klass, obj):
    """Validates an handler implementation against the ICache interface."""
    
    members = [
        '_setup',
        'get',
        'set',
        'delete',
        'purge',
        ]
    interface.validate(ICache, obj, members)    
    
class ICache(interface.Interface):
    """
    This class defines the Cache Handler Interface.  Classes that 
    implement this handler must provide the methods and attributes defined 
    below.
    
    Implementations do *not* subclass from interfaces.
    
    Usage:
    
    .. code-block:: python
    
        from cement2.core import cache
        
        class MyCacheHandler(object):
            class Meta:
                interface = cache.ICache
                label = 'my_cache_handler'
            ...
    
    """
    class IMeta:
        label = 'cache'
        validator = cache_validator
    
    # Must be provided by the implementation
    Meta = interface.Attribute('Handler Meta-data')
    
    def _setup(app_obj):
        """
        The _setup function is called during application initialization and
        must 'setup' the handler object making it ready for the framework
        or the application to make further calls to it.
        
        Required Arguments:
        
            app_obj
                The application object. 
                                
        Returns: n/a
        
        """
    
    def get(key, fallback=None):
        """
        Get the value for a key in the cache.  If the key does not exist
        or the key/value in cache is expired, this functions must return 
        None.
        
        Required Arguments:
        
            key
                The key of the value stored in cache
                
        Optional Arguments:
        
            fallback
                The value that is returned if the cache is expired or the
                key does not exist.
                
        Return: unknown (whatever the value is in cache, or the 'fallback')
        
        """    

    def set(key, value, time=None):
        """
        Set the key/valuue in cache for 'time'.  
        
        Required Arguments:
        
            key
                The key of the value to store in cache.
            
            value
                The value of that key to store in cache.
        
        Optional Arguments:
        
            time
                A one-off expire time.  If no time is given, then a 
                default value is used (determined by the implementation).
        
        Return: None
        
        """
    
    def delete(key):
        """
        Deletes a key/value from the cache.
        
        Return: True
        
        """
        
    def purge():
        """
        Clears all data from the cache.
        
        """
        
class CementCacheHandler(handler.CementBaseHandler):
    """
    Base class that all Cache Handlers should sub-class from.
    
    """
    class Meta:
        label = None
        interface = ICache
        
    def __init__(self, *args, **kw):
        super(CementCacheHandler, self).__init__(*args, **kw)
        
    def get(self, key):
        raise NotImplementedError
        
    def set(self, key, value):
        raise NotImplementedError
        
    def delete(self, key):
        raise NotImplementedError
        
    def purge(self):
        raise NotImplementedError
        
class MemoryCacheHandler(CementCacheHandler):
    class Meta:
        label = 'memory'
    
    
    
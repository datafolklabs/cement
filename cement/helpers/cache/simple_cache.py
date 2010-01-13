
import os
import pickle

from cement import namespaces
from cement.core.log import get_logger

log = get_logger(__name__)

class SimpleCache(object):
    def __init__(self, path=None, mode=0640):
        self.cache = {}
        self.path = path
        if not self.path:
            self.path = os.path.join(namespaces['global'].config['data_dir'],
                                     'simple_cache.pickle')
        self.gen_cache(clear_existing=False, mode=mode)
        
    def gen_cache(self, clear_existing=False, mode=0640):
        """Generate a pickle cache."""
        if not os.path.exists(os.path.dirname(self.path)):
            os.makedirs(os.path.exists(os.path.dirname(self.path)))
        
        if clear_existing:
            os.remove(self.path)
            
        if not os.path.exists(self.path):
            f = open(self.path, 'wb')
            pickle.dump(self.cache, f)
            f.close()
        
        os.chmod(self.path, mode)
        
    def clear_cache(self):
        os.remove(self.path)
        
    def load(self):
        """Load the pickle cache into self.cache dict."""
        self.cache = pickle.load(open(self.path, 'rb'))
        
    def store(self, key=None, value=None):
        """Store a key/value pair, overwrite if existing."""
        
        log.debug('storing cache: %s => %s' % (key, value))
        if not key:
            log.warn('warning, no key supplied for cache.')
        else:
            self.load()
            self.cache[key] = value
            f = open(self.path, 'wb')
            pickle.dump(self.cache, f)
            f.close()
            self.load()
    
    def get(self, key=None):
        log.debug('retrieving cache: %s' % key)
        if not key:
            return None
        self.load()
        if self.cache.has_key(key):
            return self.cache[key]
        else:
            return None
    
    def drop(self, key):
        log.debug('dropping cache: %s' % key)
        self.load()
        if self.cache.has_key(key):
            self.cache.pop(key)
            return True
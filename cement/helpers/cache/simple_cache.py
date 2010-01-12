
import os
import pickle

from cement import namespaces
from cement.core.log import get_logger

log = get_logger(__name__)

class SimpleCache(object):
    def __init__(self, path=None):
        self.cache = {}
        self.path = path
        if not self.path:
            self.path = os.path.join(namespaces['global'].config['data_dir'],
                                     'simple_cache.pickle')
        if not os.path.exists(os.path.dirname(self.path)):
            os.makedirs(os.path.exists(os.path.dirname(self.path)))
        
        if not os.path.exists(self.path):
            pickle.dump(self.cache, open(self.path, 'w'))
        
        self.load()
        
    def load(self):
        self.cache = pickle.load(open(self.path, 'r'))
        
    def store(self, key=None, value=None):
        if not key:
            log.warn('warning, no key supplied for cache.')
        else:
            self.load()
            self.cache[key] = value
            pickle.dump(self.cache, open(self.path, 'w'))
    
    def get(self, key=None):
        if not key:
            return None
        self.load()
        if self.cache.has_key(key):
            return self.cache[key]
        else:
            return None
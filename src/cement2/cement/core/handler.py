"""Cement Handlers configuration."""

from cement.core.backend import handlers
from cement.core.exc import CementRuntimeError
from cement.handlers.log import LoggingLogHandler

log = LoggingLogHandler(__name__)

def get_handler(handler_type, handler_name):
    """
    Get a handler object.
    
    Required Arguments:
    
        handler_type
            The type of handler (i.e. 'output')
        
        handler_name
            The name of the handler (i.e. 'json')
            
    Usage:
    
        from cement.core.handler import get_handler
        handler = get_handler('output', 'json')(dict(foo=bar))
        handler.render()

    """
    if handler_type in handlers:
        if handler_name in handlers[handler_type]:
            return handlers[handler_type][handler_name]
    raise CementRuntimeError("handlers['%s']['%s'] does not exist!" \
                          % (handler_type, handler_name))
    
def define_handler(handler_type):
    """
    Define a handler type that plugins can register handler objects under.
    
    Required arguments:
    
        handler_type
            The type of the handler, stored as handlers['handler_type']
    
    
    Usage:
    
    .. code-block:: python
    
        from cement.core.handler import define_handler
        
        define_handler('database')
    
    """
    log.debug("defining handler type '%s'" % handler_type)
    if handlers.has_key(handler_type):
        raise CementRuntimeError("handler type '%s' already defined!" % \
                                  handler_type)
    handlers[handler_type] = {}
    
    
def register_handler(handler_type, name, handler_object):
    """
    Register a handler object to a handler.
    
    Required Options:
    
        handler_type
            The type of the handler to register
        
        name
            The name to register the handler object as
            
        handler_object
            The handler object to register
    
    Usage:
    
    .. code-block:: python
    
        from cement.core.handler import register_handler
        
        my_handler_object = SomeTypeOfObject()
        register_handler('database', 'my_database_handler', my_handler_object)
    
    """
    if handler_type not in handlers:
        raise CementRuntimeError("Handler type '%s' doesn't exist." % \
                                 handler_type)
    if handlers[handler_type].has_key(name):
        raise CementRuntimeError(
            "handlers['%s']['%s'] already exists" % \
            (handler_type, name))
    log.debug("registering handler '%s' from %s into handlers['%s']" % \
             (name, handler_object.__module__, handler_type))
    handlers[handler_type][name] = handler_object
   
class CementConfigHandler(object):
    def __init__(self, default_config, section, **kw):
        self.default_config = default_config
        self.section = section
        self.backend = None

    def parse_files(self):
        """
        Parse config file settings from self.default_config['config_files'].
        """
        for _file in self.default_config['config_files']:
            self.parse_file(_file)
    
    def parse_file(self, file_path):
        """
        Parse config file settings from file_path.
        """
        raise NotImplementedError(
            "CementConfigHandler.parse_file() must be subclassed."
            )
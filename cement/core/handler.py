"""Cement Handlers configuration."""

from cement import handlers
from cement.core.log import get_logger
from cement.core.namespace import get_config
from cement.core.exc import CementRuntimeError

log = get_logger(__name__)

def get_handler(handler_type, handler_name, *args, **kw):
    if handler_type in handlers:
        if handler_name in handlers[handler_type]:
            return handlers[handler_type][handler_name]
    raise CementRuntimeError, "The handler handlers[%s][%s] does not exist!" \
        % (handler_type, handler_name)
    
def define_handler(type):
    """
    Define a handler type that plugins can register handler objects under.
    
    Required arguments:
    
        name
            The name of the handler, stored as handlers['name']
    
    
    Usage:
    
    .. code-block:: python
    
        from cement.core.handler import define_handler
        
        define_handler('database')
    
    """
    config = get_config()
    log.debug("defining handler type '%s'", type)
    if handlers.has_key(type):
        raise CementRuntimeError, "Handler type '%s' already defined!" % type
    handlers[type] = {}
    
    
def register_handler(type, name, handler_object):
    """
    Register a handler object to a handler.
    
    Required Options:
    
        type
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
    if type not in handlers:
        raise CementRuntimeError, "Handler type '%s' doesn't exist." % type
    if handlers[type].has_key(name):
        raise CementRuntimeError, "Handler of type '%s' and name '%s' already exists" % \
                                  (type, name)
    log.debug("registering handler '%s' from %s into handlers['%s']" % \
             (name, handler_object.__module__, type))
    handlers[type][name] = handler_object
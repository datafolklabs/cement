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
    
def define_handler(handler_type, base_handler):
    """
    Define a handler type that plugins can register handler objects under.
    
    Required arguments:
    
        handler_type
            The type of the handler, stored as handlers['handler_type']
    
        base_handler
            The base handler that handlers of this class must implement.
    
    Usage:
    
    .. code-block:: python
    
        from cement.core.handler import define_handler
        
        define_handler('database', MyAppDatabaseHandler)
    
    """
    log.debug("defining handler type '%s' (%s)" % \
        (handler_type, base_handler.__name__))
    if handlers.has_key(handler_type):
        raise CementRuntimeError("handler type '%s' already defined!" % \
                                  handler_type)
    handlers[handler_type] = {'base' : base_handler}
    
    
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
    log.debug("registering handler '%s' from %s into handlers['%s']" % \
             (name, handler_object.__module__, handler_type))
    if handler_type not in handlers:
        raise CementRuntimeError("Handler type '%s' doesn't exist." % \
                                 handler_type)
    if handlers[handler_type].has_key(name):
        raise CementRuntimeError(
            "handlers['%s']['%s'] already exists" % \
            (handler_type, name))
    if not handlers[handler_type]['base'].implementedBy(handler_object):
        raise CementRuntimeError(
            "%s does not provide a '%s' handler." % (name, handler_type))
    
    handlers[handler_type][name] = handler_object
   

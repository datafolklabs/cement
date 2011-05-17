"""Cement Handlers configuration."""

from cement.core.backend import handlers, get_minimal_logger
from cement.core.exc import CementRuntimeError, CementInterfaceError

log = get_minimal_logger(__name__)

def get(handler_type, handler_name):
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
    
def define(handler_type, handler_interface):
    """
    Define a handler type that plugins can register handler objects under.
    
    Required arguments:
    
        handler_type
            The type of the handler, stored as handlers['handler_type']
    
        handler_interface
            The handler interface class that defines the interface to be 
            implemented.
    
    Usage:
    
    .. code-block:: python
    
        from cement.core.handler import define_handler

        define_handler('database', IDatabaseHandler)
    
    """
    log.debug("defining handler type '%s' (%s)" % \
        (handler_type, handler_interface.__name__))
    if handlers.has_key(handler_type):
        raise CementRuntimeError("handler type '%s' already defined!" % \
                                  handler_type)
    handlers[handler_type] = {'interface' : handler_interface}
    
    
def register(obj):
    """
    Register a handler object to a handler.
    
    Required Options:
    
        obj
            The handler object to register
    
    Usage:
    
    .. code-block:: python
    
        from zope import interface
        from cement.core.handler import register_handler
        
        class MyHandler(object):
            __handler_label__ = 'mysql'
            __handler_type__ = 'database'
            interface.implements(IDatabaseHandler)
            
            def connect(self):
            ...
            
        register_handler(MyHandler)
    
    """
    if not hasattr(obj, '__handler_label__'):
        raise CementInterfaceError, \
            "Invalid interface %s, missing '__handler_label__'." % obj
    if not hasattr(obj, '__handler_type__'):
        raise CementInterfaceError, \
            "Invalid interface %s, missing '__handler_type__'." % obj
            
    _type = obj.__handler_type__
    _label = obj.__handler_label__
    
    log.debug("registering handler '%s' into handlers['%s']['%s']" % \
             (obj, _type, _label))
             
    if _type not in handlers:
        raise CementRuntimeError("Handler type '%s' doesn't exist." % _type)
    if handlers[_type].has_key(_label):
        raise CementRuntimeError("handlers['%s']['%s'] already exists" % \
                                (_type, _label))
    if not handlers[_type]['interface'].implementedBy(obj):
        raise CementInterfaceError("%s does not provide a '%s' handler." % \
                                  (_label, _type))
                                  
    handlers[_type]['interface'].validateInvariants(obj)
    handlers[_type][_label] = obj
   
def validate(handler_type, handler_name):
    """
    Ensure that the handler name is registered to the handler type.
    
    Required Arguments:
    
        handler_type
            The type of handler
            
        handler_name
            The name of the handler
            
    """
    if not handler_type in handlers:
        raise CementRuntimeError, \
            "Handler type '%s' is not defined." % handler_type
    if not handler_name in handlers[handler_type]:
        raise CementRuntimeError, \
            "Handler name '%s' is not registered to handlers['%s']." % \
            (handler_name, handler_type)
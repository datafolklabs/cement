"""Cement core handlers module."""

from cement2.core import exc, backend

Log = backend.minimal_logger(__name__)

def get(handler_type, handler_label):
    """
    Get a handler object.
    
    Required Arguments:
    
        handler_type
            The type of handler (i.e. 'output')
        
        handler_label
            The label of the handler (i.e. 'json')
            
    Usage:
    
        from cement.core import handler
        output = handler.get('output', 'json')
        output.render(dict(foo='bar'))

    """
    if handler_type in backend.handlers:
        if handler_label in backend.handlers[handler_type]:
            return backend.handlers[handler_type][handler_label]
    raise exc.CementRuntimeError("handlers['%s']['%s'] does not exist!" \
                          % (handler_type, handler_label))
    
def defined(handler_type):
    """
    Test whether a handler type is defined.
    
    Required Arguments:
    
        handler_type
            The name or 'type' of the handler (I.e. 'logging').
    
    Returns: bool
    
    """
    if handler_type in backend.handlers:
        return True
    else:
        return False
        
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
    
        from cement.core import handler

        handler.define('database', IDatabaseHandler)
    
    """
    Log.debug("defining handler type '%s' (%s)" % \
        (handler_type, handler_interface.__name__))
    if backend.handlers.has_key(handler_type):
        raise exc.CementRuntimeError("handler type '%s' already defined!" % \
                                  handler_type)
    backend.handlers[handler_type] = {'interface' : handler_interface}
    
    
def register(obj):
    """
    Register a handler object to a handler.
    
    Required Options:
    
        obj
            The handler object to register
    
    Usage:
    
    .. code-block:: python
    
        from zope import interface
        from cement.core import handler
        
        class MyHandler(object):
            __handler_type__ = 'database'
            __handler_label__ = 'mysql'
            interface.implements(IDatabaseHandler)
            
            def connect(self):
            ...
            
        handler.register(MyHandler)
    
    """
    if not hasattr(obj, '__handler_label__'):
        raise exc.CementInterfaceError, \
            "Invalid interface %s, missing '__handler_label__'." % obj
    if not hasattr(obj, '__handler_type__'):
        raise exc.CementInterfaceError, \
            "Invalid interface %s, missing '__handler_type__'." % obj
            
    _type = obj.__handler_type__
    _label = obj.__handler_label__
    
    Log.debug("registering handler '%s' into handlers['%s']['%s']" % \
             (obj, _type, _label))
             
    if _type not in backend.handlers:
        raise exc.CementRuntimeError("Handler type '%s' doesn't exist." % _type)
    if backend.handlers[_type].has_key(_label):
        raise exc.CementRuntimeError("handlers['%s']['%s'] already exists" % \
                                (_type, _label))
    if not backend.handlers[_type]['interface'].implementedBy(obj):
        raise exc.CementInterfaceError("%s does not provide a '%s' handler." % \
                                  (_label, _type))
                                  
    backend.handlers[_type]['interface'].validateInvariants(obj)
    backend.handlers[_type][_label] = obj
   
def enabled(handler_type, handler_label):
    """
    Check if a handler is enabled.
    
    Required Arguments:
    
        handler_type
            The type of handler
            
        handler_label
            The label of the handler
          
    Returns: Boolean
    
    """
    if handler_type in backend.handlers and \
       handler_label in backend.handlers[handler_type]:
        return True

    return False
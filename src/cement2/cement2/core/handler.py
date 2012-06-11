"""
Cement core handler module.

"""

import re
from ..core import exc, backend, meta

Log = backend.minimal_logger(__name__)

class CementBaseHandler(meta.MetaMixin):
    """
    All handlers should subclass from here.
    
    Optional / Meta Options:
    
        label
            The identifier of this handler
            
        interface
            The interface that this handler implements.
        
        config_section
            A config [section] to merge config_defaults with.
            
            Default: <interface_label>.<handler_label>
            
        config_defaults
            A config dictionary that is merged into the applications config
            in the [<config_section>] block.  These are defaults and do not
            override any existing defaults under that section.
            
        """
    class Meta:
        label = None
        interface = None
        config_section = None
        config_defaults = None
        
    def __init__(self, **kw):
        super(CementBaseHandler, self).__init__(**kw)
        self.app = None
        
    def _setup(self, app_obj):
        self.app = app_obj
        if self._meta.config_section is None:
            self._meta.config_section = "%s.%s" % \
                (self._meta.interface.IMeta.label, self._meta.label)
                
        ### FIX ME: Deprecation.
        if hasattr(self._meta, 'defaults'):
            print('DEPRECATION WARNING: Handler Meta.defaults is ' + \
                  'deprecated.  Use Meta.config_defaults instead.')
            if self._meta.config_defaults is None:
                self._meta.config_defaults = self._meta.defaults
                
        if self._meta.config_defaults is not None:
            Log.debug("merging config defaults from '%s'" % self)
            dict_obj = dict()
            dict_obj[self._meta.config_section] = self._meta.config_defaults
            self.app.config.merge(dict_obj, override=False)

def get(handler_type, handler_label, *args):
    """
    Get a handler object.
    
    Required Arguments:
    
        handler_type
            The type of handler (i.e. 'output')
        
        handler_label
            The label of the handler (i.e. 'json')
            
    Optional Arguments:
    
        fallback
            A fallback value to return if handler_label doesn't exist.
            
    Usage:
    
        from cement2.core import handler
        output = handler.get('output', 'json')
        output.render(dict(foo='bar'))

    """
    if handler_type not in backend.handlers:
        raise exc.CementRuntimeError("handler type '%s' does not exist!" % \
                                     handler_type)

    if handler_label in backend.handlers[handler_type]:
        return backend.handlers[handler_type][handler_label]
    elif len(args) > 0:
        return args[0]
    else:
        raise exc.CementRuntimeError("handlers['%s']['%s'] does not exist!" % \
                                    (handler_type, handler_label))
    
def list(handler_type):
    """
    Return a list of handlers for a given type.
    
    Required Arguments:
    
        handler_type
            The type of handler (i.e. 'output')
    
    """
    if handler_type not in backend.handlers:
        raise exc.CementRuntimeError("handler type '%s' does not exist!" % \
                                     handler_type)
                                     
    res = []
    for label in backend.handlers[handler_type]:
        if label == '__interface__':
            continue
        res.append(backend.handlers[handler_type][label])
    return res
        
def define(interface):
    """
    Define a handler based on the provided interface.  Defines a handler type
    based on <interface>.IMeta.label.
    
    Required arguments:

        interface
            The handler interface class that defines the interface to be 
            implemented.
    
    Usage:
    
    .. code-block:: python
    
        from cement2.core import handler

        handler.define(IDatabaseHandler)
    
    """
    if not hasattr(interface, 'IMeta'):
        raise exc.CementInterfaceError("Invalid %s, " % interface + \
                                       "missing 'IMeta' class.")  
    if not hasattr(interface.IMeta, 'label'):
        raise exc.CementInterfaceError("Invalid %s, " % interface + \
                                       "missing 'IMeta.label' class.")  
                                       
    Log.debug("defining handler type '%s' (%s)" % \
        (interface.IMeta.label, interface.__name__))
                                                                              
    if interface.IMeta.label in backend.handlers:
        raise exc.CementRuntimeError("Handler type '%s' already defined!" % \
                                     interface.IMeta.label)
    backend.handlers[interface.IMeta.label] = {'__interface__' : interface}
    
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
        
def register(obj):
    """
    Register a handler object to a handler.  If the same object is already
    registered then no exception is raised, however if a different object
    attempts to be registered to the same name a CementRuntimeError is 
    raised.
    
    Required Options:
    
        obj
            The handler object to register
    
    Usage:
    
    .. code-block:: python
    
        from cement2.core import handler
        
        class MyDatabaseHandler(object):
            class Meta:
                interface = IDatabase
                label = 'mysql'
            
            def connect(self):
            ...
            
        handler.register(MyDatabaseHandler)
    
    """
    # This is redundant with the validator, but if we don't check for them
    # then we'll get an uncontrolled exception.
    #if not hasattr(obj, 'Meta'):
    #    raise exc.CementInterfaceError("Invalid handler %s, " % obj + \
    #                                   "missing 'Meta' class.")  
    
    orig_obj = obj

    # for checks
    obj = orig_obj()
        
    if not hasattr(obj._meta, 'label') or not obj._meta.label:
        raise exc.CementInterfaceError("Invalid handler %s, " % orig_obj + \
                                       "missing '_meta.label'.")
    if not hasattr(obj._meta, 'interface') or not obj._meta.interface:
        raise exc.CementInterfaceError("Invalid handler %s, " % orig_obj + \
                                       "missing '_meta.interface'.")

    # translate dashes to underscores
    orig_obj.Meta.label = re.sub('-', '_', obj._meta.label)
    obj._meta.label = re.sub('-', '_', obj._meta.label)
    
    handler_type = obj._meta.interface.IMeta.label
    Log.debug("registering handler '%s' into handlers['%s']['%s']" % \
             (orig_obj, handler_type, obj._meta.label))
             
    if handler_type not in backend.handlers:
        raise exc.CementRuntimeError("Handler type '%s' doesn't exist." % \
                                     handler_type)                     
    if obj._meta.label in backend.handlers[handler_type] and \
        backend.handlers[handler_type][obj._meta.label] != obj:
        raise exc.CementRuntimeError("handlers['%s']['%s'] already exists" % \
                                    (handler_type, obj._meta.label))

    interface = backend.handlers[handler_type]['__interface__']
    if hasattr(interface.IMeta, 'validator'):
        interface.IMeta().validator(obj)
    else:
        Log.debug("Interface '%s' does not have a validator() function!" % \
                 interface)
        
    backend.handlers[handler_type][obj.Meta.label] = orig_obj

def enabled(handler_type, handler_label):
    """
    Deprecated as of 1.9.5.  Use handler.registered().
    
    """   
    Log.warn("DEPRECATION WARNING: handler.enabled() is deprecated.  " + \
             "Use handler.registered() instead.")
    return registered(handler_type, handler_label)
    
def registered(handler_type, handler_label):
    """
    Check if a handler is registered.
    
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


"""Cement core output module."""

from zope import interface

from cement2.core import backend, exc

Log = backend.minimal_logger(__name__)

def output_handler_invariant(obj):
    invalid = []
    members = [
        '__init__',
        '__handler_label__',
        '__handler_type__',
        'render',
        ]
        
    for member in members:
        if not hasattr(obj, member):
            invalid.append(member)
    
    if invalid:
        raise exc.CementInterfaceError, \
            "Invalid or missing: %s in %s" % (invalid, obj)
    
class IOutputHandler(interface.Interface):
    """
    This class defines the Output Handler Interface.  Classes that 
    implement this handler must provide the methods and attributes defined 
    below.
    
    """
    # internal mechanism for handler registration
    __handler_type__ = interface.Attribute('Handler Type Identifier')
    __handler_label__ = interface.Attribute('Handler Label Identifier')
    interface.invariant(output_handler_invariant)
    
    def __init__(config_obj, *args, **kw):
        """
        The __init__ function emplementation of Cement handlers acts as a 
        wrapper for initialization.  In general, the implementation simply
        needs to accept the config object as its first argument.  If the 
        implementation subclasses from something else it will need to
        handle passing the proper args/keyword args to that classes __init__
        function, or you can easily just pass *args, **kw directly to it.
        
        Required Arguments:
        
            config
                 The application configuration object after it has been parsed
                and processed.  This is *not* a defaults dictionary, though
                some config handler implementations may work as a dict.
        
        
        Optional Arguments:
        
            *args
                Additional positional arguments.
                
            **kw
                Additional keyword arguments.
                
        """
    
    def render(self, data_dict, template=None):
        """
        Render the data_dict into output in some fashion.
        
        Required Arguments:
        
            data_dict
                The dictionary whose data we need to render into output.
                
        Optional Paramaters:
        
            template
                A template to use for rendering (in module form).  I.e.
                myapp.templates.some_command
                
                
        Returns: string or unicode string or None
        
        """        

class CementOutputHandler(object):
    """
    This class implements the IOutputHandler interface.  It literally does
    nothing to generate output.
    
    """
    __handler_type__ = 'output'
    __handler_label__ = 'cement'
    
    interface.implements(IOutputHandler)
    
    def __init__(self, config_obj, *args, **kw):
        pass
        
    def render(self, data_dict, template=None):
        """
        Take a data dictionary and render it as nothing. 
        
        Required Arguments:
        
            data_dict
                The data dictionary to render.
                
        Optional Arguments:
        
            template
                A template to not render anything from.
                
        Returns: None
        
        """
        Log.debug("not rendering any output")
        return None
        
"""Cement core output module."""

from cement2.core import backend, exc, interface

Log = backend.minimal_logger(__name__)

def output_validator(klass, obj):
    """Validates an handler implementation against the IOutput interface."""
    
    members = [
        'setup',
        'render',
        ]
    interface.validate(IOutput, obj, members)    
    
class IOutput(interface.Interface):
    """
    This class defines the Output Handler Interface.  Classes that 
    implement this handler must provide the methods and attributes defined 
    below.
    
    Implementations do *not* subclass from interfaces.
    
    Usage:
    
    .. code-block:: python
    
        from cement2.core import output
        
        class MyOutputHandler(object):
            class Meta:
                interface = output.IOutput
                label = 'my_output_handler'
            ...
    
    """
    class IMeta:
        label = 'output'
        validator = output_validator
    
    # Must be provided by the implementation
    Meta = interface.Attribute('Handler Meta-data')
    
    def setup(config_obj):
        """
        The setup function is called during application initialization and
        must 'setup' the handler object making it ready for the framework
        or the application to make further calls to it.
        
        Required Arguments:
        
            config_obj
                The application configuration object.  This is a config object 
                that implements the :ref:`IConfig` <cement2.core.config>` 
                interface and not a config dictionary, though some config 
                handler implementations may also function like a dict 
                (i.e. configobj).
                
        Returns: n/a
        
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

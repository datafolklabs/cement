"""Cement core output module."""

from ..core import backend, exc, interface, handler

LOG = backend.minimal_logger(__name__)

def output_validator(klass, obj):
    """Validates an handler implementation against the IOutput interface."""
    
    members = [
        '_setup',
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
    
        from cement.core import output
        
        class MyOutputHandler(object):
            class Meta:
                interface = output.IOutput
                label = 'my_output_handler'
            ...
    
    """
    # pylint: disable=W0232, C0111, R0903
    class IMeta:
        """Interface meta-data."""
        
        label = 'output'
        """The string identifier of the interface."""
        
        validator = output_validator
        """The interface validator function."""
    
    # Must be provided by the implementation
    Meta = interface.Attribute('Handler meta-data')
    
    def _setup(app_obj):
        """
        The _setup function is called during application initialization and
        must 'setup' the handler object making it ready for the framework
        or the application to make further calls to it.
        
        :param app_obj: The application object. 
                                
        """
    
    def render(data_dict, template=None):
        """
        Render the data_dict into output in some fashion.
        
        :param data_dict: The dictionary whose data we need to render into 
            output.
        :param template: A template to use for rendering (in module form).  
            I.e ``myapp.templates.some_command``.
        :returns: string or unicode string or None
        
        """    

class CementOutputHandler(handler.CementBaseHandler):
    """
    Base class that all Output Handlers should sub-class from.
    
    """
    class Meta:
        """
        Handler meta-data (can be passed as keyword arguments to the parent 
        class).
        """
        
        label = None
        """The string identifier of this handler."""
        
        interface = IOutput
        """The interface that this class implements."""
        
    def __init__(self, *args, **kw):
        super(CementOutputHandler, self).__init__(*args, **kw)
    

"""Cement basic output handler extension."""

from zope import interface

from cement2.core import backend, handler, output

Log = backend.minimal_logger(__name__)

class CementOutputHandler(object):
    """
    This class implements the IOutputHandler interface.  It literally does
    nothing to generate output.
    
    """
    __handler_type__ = 'output'
    __handler_label__ = 'cement'
    file_suffix = None
    
    interface.implements(output.IOutputHandler)
    
    def setup(self, config_obj):
        self.config = config_obj
        
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
        
handler.register(CementOutputHandler)
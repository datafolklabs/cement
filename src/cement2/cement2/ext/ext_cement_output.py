"""Cement basic output handler extension."""

from cement2.core import backend, handler, output

Log = backend.minimal_logger(__name__)

class CementOutputHandler(object):
    """
    This class implements the IOutputHandler interface.  It literally does
    nothing to generate output.
    
    """
    file_suffix = None
    
    class meta:
        interface = output.IOutput
        label = 'cement'
        
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
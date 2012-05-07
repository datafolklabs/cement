"""Null Output Framework Extension Library."""

from ..core import backend, output

Log = backend.minimal_logger(__name__)

class NullOutputHandler(output.CementOutputHandler):
    """
    This class is an internal implementation of the 
    :ref:`IOutput <cement2.core.output>` interface. It does not take any 
    parameters on initialization.
    
    """
    class Meta:
        interface = output.IOutput
        label = 'null'
        
    def render(self, data_dict, template=None):
        """
        This implementation does not actually render anything to output, but
        rather logs it to the debug facility.
        
        Required Arguments:
        
            data_dict
                The data dictionary to render.
                
        Optional Arguments:
        
            template
                The template parameter is not used by this implementation at
                all.
                
        Returns: None
        
        """
        Log.debug("not rendering any output to console")
        Log.debug("DATA: %s" % data_dict)
        return None
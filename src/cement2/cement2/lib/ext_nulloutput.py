"""Null Output Framework Extension Library."""

from cement2.core import backend, output

Log = backend.minimal_logger(__name__)

class NullOutputHandler(object):
    """
    This class is an internal implementation of the 
    :ref:`IOutput <cement2.core.output>` interface. It does not take any 
    parameters on initialization.
    
    """
    class meta:
        interface = output.IOutput
        label = 'null'
        
    def setup(self, config_obj):
        """
        Sets up the class for use by the framework.  Little is done here in
        this implementation.
        
        Required Arguments:
        
            config_obj
                The application configuration object.  This is a config object 
                that implements the :ref:`IConfig <cement2.core.config>` 
                interface and not a config dictionary, though some config 
                handler implementations may also function like a dict 
                (i.e. configobj).
                
        Returns: n/a
        
        """
        self.config = config_obj
        
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
"""Yaml Framework Extension for Cement."""

import sys
import yaml
from zope import interface

from cement2.core import handler, hook, output, backend
Log = backend.minimal_logger(__name__)

class YamlOutputHandler(object):
    __handler_type__ = 'output'
    __handler_label__ = 'yaml'
    
    interface.implements(output.IOutputHandler)
    
    def __init__(self):
        """
        This handler implements the IOutputHandler interface.  It provides
        Yaml output from a return dictionary and uses the yaml library to dump 
        it to STDOUT.
        
        Note: The cement framework detects the '--yaml' option and suppresses
        output (same as if passing --quiet).  Therefore, if debugging or 
        troubleshooting issues you must pass the --debug option to see whats
        going on .
        
        """
        self.config = None
        
    def setup(self, config_obj):
        """
        Setup the handler for future use.
        
        Required Arguments:
        
            config_obj
                The application configuration object.  This is a config object 
                that implements the IConfigHandler interface and not a config 
                dictionary, though some config handler implementations may 
                also function like a dict (i.e. configobj).
        
        Returns: N/A
        
        """
        self.config = config_obj
        
    def render(self, data_dict, template=None):
        """
        Take a data dictionary and render it as Yaml output.  Note that the
        template option is received here per the interface, however this 
        handler just ignores it.
        
        Required Arguments:
        
            data_dict
                The data dictionary to render.
                
        Optional Arguments:
        
            template
                This option is completely ignored.
                
            unpicklable
                Whether or not the object is unpicklable (default: False)
                
        Returns: string (yaml)
        
        """
        Log.debug("rendering output as Yaml via %s" % self.__module__)
        sys.stdout = backend.STDOUT
        sys.stderr = backend.STDERR
        return yaml.dump(data_dict).strip()
            
handler.register(YamlOutputHandler)

@hook.register()
def cement_add_args_hook(config, arg_obj):
    """
    Adds the '--yaml' argument to the argument object.
    
    """
    arg_obj.minimal_add_argument('--yaml', dest='output_handler', 
        action='store_const', help='toggle yaml output handler', const='yaml')
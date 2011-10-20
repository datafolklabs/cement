"""Yaml Framework Extension for Cement."""

import sys
import yaml
from cement2.core import handler, hook, output, backend

Log = backend.minimal_logger(__name__)

class YamlOutputHandler(object):
    """
    This class implements the :ref:`IOutput <cement2.core.output>` 
    interface.  It provides YAML output from a data dictionary and uses 
    `pyYAML <http://pyyaml.org/wiki/PyYAMLDocumentation>`_ to dump it to STDOUT.  
    
    Note: The cement framework detects the '--json' option and suppresses
    output (same as if passing --quiet).  Therefore, if debugging or 
    troubleshooting issues you must pass the --debug option to see whats
    going on.
    
    """
    class meta:
        interface = output.IOutput
        label = 'yaml'
        
    def __init__(self):
        self.config = None
        
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
        Take a data dictionary and render it as YAML output.  Note that the
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
        sys.stdout = backend.SAVED_STDOUT
        sys.stderr = backend.SAVED_STDERR
        return yaml.dump(data_dict).strip()
            
handler.register(YamlOutputHandler)

@hook.register()
def cement_add_args_hook(config, arg_obj):
    """
    Adds the '--yaml' argument to the argument object.
    
    """
    arg_obj.add_argument('--yaml', dest='output_handler', 
        action='store_const', help='toggle yaml output handler', const='yaml')
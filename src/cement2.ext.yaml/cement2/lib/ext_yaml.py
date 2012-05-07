"""YAML Framework Extension Library."""

import sys
import yaml
from ..core import output, backend

Log = backend.minimal_logger(__name__)

class YamlOutputHandler(output.CementOutputHandler):
    """
    This class implements the :ref:`IOutput <cement2.core.output>` 
    interface.  It provides YAML output from a data dictionary and uses 
    `pyYAML <http://pyyaml.org/wiki/PyYAMLDocumentation>`_ to dump it to STDOUT.  
    
    Note: The cement framework detects the '--json' option and suppresses
    output (same as if passing --quiet).  Therefore, if debugging or 
    troubleshooting issues you must pass the --debug option to see whats
    going on.
    
    """
    class Meta:
        interface = output.IOutput
        label = 'yaml'
        
    def __init__(self, *args, **kw):
        super(YamlOutputHandler, self).__init__(*args, **kw)
        self.config = None
        
    def _setup(self, app_obj):
        self.app = app_obj
        
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
        return yaml.dump(data_dict)

"""ConfigObj Framework Extension for Cement."""

import os
import yaml
from zope import interface

from cement2.core import handler, output, backend

Log = backend.minimal_logger(__name__)

class YamlOutputHandler(object):
    __handler_type__ = 'output'
    __handler_label__ = 'yaml'
    
    interface.implements(output.IOutputHandler)
    
    def __init__(self):
        self.config = None
        
    def setup(self, config_obj):
        self.config = config_obj
        
    def render(self, data_dict, template=None):
        """
        Take a data dictionary and render it as Yaml output.
        
        Required Arguments:
        
            data_dict
                The data dictionary to render.
                
        Ignored Parameters:
        
            template
                Not applicable for this extension.
                
        Returns: string (yaml)
        
        """
        Log.debug("rendering yaml output")
        
        data_dict['stdout'] = backend.buf_stdout.buffer
        data_dict['stderr'] = backend.buf_stderr.buffer
        return yaml.dump(data_dict).strip()
            
handler.register(YamlOutputHandler)

# FIX ME: Add an 'options' hook here to add the --yaml option and override
# the config['base']['output_handler'].
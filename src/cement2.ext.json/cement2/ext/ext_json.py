"""ConfigObj Framework Extension for Cement."""

import os
import sys
import jsonpickle
from zope import interface

from cement2.core import handler, output, backend, hook

Log = backend.minimal_logger(__name__)

class JsonOutputHandler(object):
    __handler_type__ = 'output'
    __handler_label__ = 'json'
    
    interface.implements(output.IOutputHandler)
    
    def __init__(self):
        self.config = None
        
    def setup(self, config_obj):
        self.config = config_obj
        
    def render(self, data_dict, template=None, unpicklable=False):
        """
        Take a data dictionary and render it as Json output.
        
        Required Arguments:
        
            data_dict
                The data dictionary to render.
                
        Optional Arguments:
        
            unpicklable
                Whether or not the object is unpicklable (default: False)
                
        Returns: string (json)
        
        """
        Log.debug("rendering json output")
        sys.stdout = backend.SAVED_STDOUT
        sys.stderr = backend.SAVED_STDERR
        return jsonpickle.encode(data_dict, unpicklable=unpicklable)
            
handler.register(JsonOutputHandler)

@hook.register()
def cement_add_args_hook(config, arg_obj):
    arg_obj.minimal_add_argument('--json', dest='output_handler', 
        action='store_const', help='toggle json output handler', const='json')

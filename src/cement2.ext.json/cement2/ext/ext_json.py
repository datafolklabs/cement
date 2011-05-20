"""ConfigObj Framework Extension for Cement."""

import os
import jsonpickle
from zope import interface

from cement2.core import handler, output, backend

Log = backend.minimal_logger(__name__)

class JsonOutputHandler(object):
    __handler_type__ = 'output'
    __handler_label__ = 'json'
    
    interface.implements(output.IOutputHandler)
    
    def __init__(self, config_obj, *args, **kw):
        pass
        
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
        
        data_dict['stdout'] = backend.buf_stdout.buffer
        data_dict['stderr'] = backend.buf_stderr.buffer
        return jsonpickle.encode(data_dict, unpicklable=unpicklable)
            
handler.register(JsonOutputHandler)

# FIX ME: Add an 'options' hook here to add the --json option and override
# the config['base']['output_handler'].
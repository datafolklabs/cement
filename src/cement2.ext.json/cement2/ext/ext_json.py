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
        """
        This handler implements the IOutputHandler interface.  It provides
        JSON output from a return dictionary and uses jsonpickle to dump it
        to STDOUT.
        
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
        
    def render(self, data_dict, template=None, unpicklable=False):
        """
        Take a data dictionary and render it as Json output.  Not that the
        template option is received here per the interface, however this 
        handler just ignores it.
        
        Required Arguments:
        
            data_dict
                The data dictionary to render.
                
        Optional Arguments:
        
            templates
                This option is completely ignored.
                
            unpicklable
                Whether or not the object is unpicklable (default: False)
                
        Returns: string (json)
        
        """
        Log.debug("rendering output as JSON via %s" % self.__module__)
        sys.stdout = backend.STDOUT
        sys.stderr = backend.STDERR
        return jsonpickle.encode(data_dict, unpicklable=unpicklable)
            
handler.register(JsonOutputHandler)

@hook.register()
def cement_add_args_hook(config, arg_obj):
    """
    Adds the '--json' argument to the argument object.
    
    """
    arg_obj.minimal_add_argument('--json', dest='output_handler', 
        action='store_const', help='toggle json output handler', const='json')

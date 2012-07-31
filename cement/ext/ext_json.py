"""JSON Framework Extension"""

import sys
import json
from ..core import output, backend, hook, handler

LOG = backend.minimal_logger(__name__)

class JsonOutputHandler(output.CementOutputHandler):
    """
    This class implements the :ref:`IOutput <cement.core.output>` 
    interface.  It provides JSON output from a data dictionary and uses 
    `jsonpickle <http://jsonpickle.github.com/>`_ to dump it to STDOUT.  
    
    Note: The cement framework detects the '--json' option and suppresses
    output (same as if passing --quiet).  Therefore, if debugging or 
    troubleshooting issues you must pass the --debug option to see whats
    going on.
    
    """
    class Meta:
        interface = output.IOutput
        label = 'json'
        
    def __init__(self, *args, **kw):
        super(JsonOutputHandler, self).__init__(*args, **kw)
        self.app = None
        
    def _setup(self, app_obj):
        self.app = app_obj
        
    def render(self, data_dict, template=None):
        """
        Take a data dictionary and render it as Json output.  Note that the
        template option is received here per the interface, however this 
        handler just ignores it.
        
        Required Arguments:
        
            data_dict
                The data dictionary to render.
                
        Optional Arguments:
        
            template
                This option is completely ignored.
                
        Returns: string (json)
        
        """
        LOG.debug("rendering output as Json via %s" % self.__module__)
        sys.stdout = backend.SAVED_STDOUT
        sys.stderr = backend.SAVED_STDERR
        return json.dumps(data_dict)
            
def add_json_option(app):
    """
    Adds the '--json' argument to the argument object.
    
    """
    app.args.add_argument('--json', dest='output_handler', 
        action='store_const', help='toggle json output handler', const='json')

def set_output_handler(app):
    if '--json' in app._meta.argv:
        app._meta.output_handler = 'json'
        app._setup_output_handler()

def load():
    hook.register('post_setup', add_json_option)
    hook.register('pre_run', set_output_handler)
    handler.register(JsonOutputHandler)
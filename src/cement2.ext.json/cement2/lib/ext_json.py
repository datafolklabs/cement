"""JSON Framework Extension Library."""

import sys
from ..core import output, backend, hook

if sys.version_info[0] >= 3:
    raise SkipTest('jsonpickle does not support Python 3') # pragma: no cover
    
import jsonpickle

Log = backend.minimal_logger(__name__)

class JsonOutputHandler(output.CementOutputHandler):
    """
    This class implements the :ref:`IOutput <cement2.core.output>` 
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
        
    def render(self, data_dict, template=None, unpicklable=False):
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
                
            unpicklable
                Whether or not the object is unpicklable (default: False)
                
        Returns: string (json)
        
        """
        Log.debug("rendering output as Json via %s" % self.__module__)
        sys.stdout = backend.SAVED_STDOUT
        sys.stderr = backend.SAVED_STDERR
        return jsonpickle.encode(data_dict, unpicklable=unpicklable)

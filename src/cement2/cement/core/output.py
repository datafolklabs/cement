
from cement.core.handler import get_handler
from cement.core.exc import CementRuntimeError

class CementOutputHandler(object):
    """
    This is the standard class for output handling.  All output handlers
    should subclass from here.

    Required Arguments:
    
        data
            The dictionary returned from a controller function.   
                     
    """
    def __init__(self, config, data):
        self.config = config
        self.data = data
        self.log = get_handler('log', config['log_handler'])(__name__)
        self._verify_data()
        
    def _verify_data(self):
        """
        Verify the data to ensure it is in the proper format.
        """
        self.log.debug('verifying output data')
        try:
            assert type(self.data) == dict, "data must be of type dict."
        except AssertionError, e:
            raise CementRuntimeError, e.args[0]
            
    def render(self):
        """
        Using the self.data dictionary, render output.  Must return the 
        rendered output (and not actually display it).
        """
        self.log.debug('rendering output using CementOutputHandler')
        raise NotImplementedError, \
            "CementOutputHandler.render() must be subclassed."
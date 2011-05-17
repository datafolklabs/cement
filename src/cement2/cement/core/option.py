
from cement.core.handler import get_handler

class CementOptionHandler(object):
    def __init__(self, config):
        self.config = config
        self.log = get_handler('log', config['log_handler'])(__name__)
    
    def add_option(self, *args, **kw):
        """
        Add a command line option.
        
        Optional Arguments:
        
            short_name
                A short name reference.  I.e. '-h'.
                
            long_name
                A long name reference.  I.e. '--help'.
            
        Option Keyword Arguments:
        
            action
                The action to be taken when this argument is encountered.
                
            default
                The default value of the option.
                
            help
                A brief description of the option.
            
            metavar
                A name for the argument in usage messages.
                
            dest
                The destination variable to use for this opton.
                
        """
        raise NotImplementedError, \
            "CementOptionHandler.add_option() must be subclassed."
    
    def parse_options(self, argv):
        """
        Parse the command line options.  Must return a tuple of 
        (options, args).
        
        Required Arguments:
        
            argv
                List of arguments to parse.
                
        """
        raise NotImplementedError, \
            "CementOptionHandler.add_option() must be subclassed."

    

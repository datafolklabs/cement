"""
ArgParse Framework Extension Library.
    
"""
            
from argparse import ArgumentParser
from ..core import backend, arg

Log = backend.minimal_logger(__name__)
    
class ArgParseArgumentHandler(arg.CementArgumentHandler, ArgumentParser):
    """
    This class implements the :ref:`IArgument <cement2.core.arg>` 
    interface, and sub-classes from `argparse.ArgumentParser <http://docs.python.org/dev/library/argparse.html>`_.
    Please reference the argparse documentation for full usage of the
    class.

    Arguments and Keyword arguments are passed directly to ArgumentParser
    on initialization.
    """
    
    parsed_args = None
    class Meta:
        interface = arg.IArgument
        label = 'argparse'
    
    def __init__(self, *args, **kw):
        super(ArgParseArgumentHandler, self).__init__(*args, **kw)
        self.config = None
        
    def parse(self, arg_list):
        """
        Parse a list of arguments, and store them as self.parsed_args which
        is an object.  Meaning an argument name of 'foo' will be stored as
        self.parsed_args.foo.
        
        Required Arguments:
        
            arg_list
                A list of arguments (generally sys.argv) to be parsed.
        
        Returns: self.parsed_args (object)
        
        """
        self.parsed_args = self.parse_args(arg_list)
        return self.parsed_args
        
    def add_argument(self, *args, **kw):
        """
        Add an argument to the parser.  Arguments and keyword arguments are
        passed directly to ArgumentParser.add_argument().
        
        """
        return super(ArgumentParser, self).add_argument(*args, **kw)            

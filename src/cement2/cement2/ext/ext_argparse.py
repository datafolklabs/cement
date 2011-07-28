"""ArgParse framework extension."""

from zope import interface
from argparse import ArgumentParser
from cement2.core import backend, handler, arg

Log = backend.minimal_logger(__name__)

    
class ArgParseArgumentHandler(ArgumentParser):
    interface.implements(arg.IArgumentHandler)
    result = None
    class meta:
        type = 'arg'
        label = 'argparse'
    
    def __init__(self, *args, **kw):
        ArgumentParser.__init__(self, *args, **kw)
        self.config = None
        
    def setup(self, config_obj):
        self.config = config_obj
        
    def parse(self, args):
        self.result = self.parse_args(args)
        return self.result
        
    def minimal_add_argument(self, *args, **kw):
        return self.add_argument(*args, **kw)            

handler.register(ArgParseArgumentHandler)
    
    

"""OptParse framework extension."""

from zope import interface
from optparse import OptionParser
from cement2.core import backend, handler, arg

Log = backend.minimal_logger(__name__)
    
class OptParseArgumentHandler(OptionParser):
    __handler_type__ = 'arg'
    __handler_label__ = 'optparse'
    interface.implements(arg.IArgumentHandler)
    result = None
    
    def __init__(self, *args, **kw):
        OptionParser.__init__(self, *args, **kw)
        self.config = None
        
    def setup(self, config_obj):
        self.config = config_obj
        
    def parse(self, args):
        self.result = self.parse_args(args)
        return self.result
        
    def minimal_add_argument(self, *args, **kw):
        return self.add_option(*args, **kw)            

handler.register(OptParseArgumentHandler)
    
    

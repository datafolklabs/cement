"""Example framework extension."""

from zope import interface

from cement2.core import output, handler

class ExampleOutputHandler(object):
    __handler_type__ = 'output'
    __handler_label__ = 'example'
    interface.implements(output.IOutputHandler)
    
    def __init__(config_obj, *args, **kw):
        self.config_obj = config_obj
    
    def render(self, data_dict, template=None):
        # do something to render output text from data_dict
        text = "Example output handler"
        return text

handler.register(ExampleOutputHandler)

from cement2.core import backend, foundation, handler

def reset_backend():
    for _handler in backend.handlers.copy():
        del backend.handlers[_handler]
    for _hook in backend.hooks.copy():
        del backend.hooks[_hook]
            
def register_all_extensions(import_modules=True):
    if import_modules:
        from cement2.ext import ext_argparse
        from cement2.ext import ext_cement_output
        from cement2.ext import ext_cement_plugin
        from cement2.ext import ext_configparser
        from cement2.ext import ext_logging
        from cement2.ext import ext_optparse
        
    handler.register(ext_argparse.ArgParseArgumentHandler)
    handler.register(ext_cement_output.CementOutputHandler)
    handler.register(ext_cement_plugin.CementPluginHandler)
    handler.register(ext_configparser.ConfigParserConfigHandler)
    handler.register(ext_logging.LoggingLogHandler)
    handler.register(ext_optparse.OptParseArgumentHandler)
    
def prep(app_name='test', *args, **kw):
    reset_backend()
    dummy_app = foundation.lay_cement(app_name, *args, **kw)
    register_all_extensions()
    return dummy_app


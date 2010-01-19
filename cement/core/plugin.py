"""Methods and classes to handle Cement plugin support."""

import os
        
from cement import namespaces
from cement.core.exc import CementConfigError, CementRuntimeError
from cement.core.log import get_logger
from cement.core.hook import run_hooks
from cement.core.configuration import set_config_opts_per_file
from cement.core.namespace import CementNamespace, define_namespace
from cement.core.configuration import ensure_api_compat

log = get_logger(__name__)

class CementPlugin(CementNamespace):
    """Wrapper for CementNamespace."""
    def __init__(self, *args, **kwargs):
        CementNamespace.__init__(self, *args, **kwargs)
        
def register_plugin(**kwargs):
    """
    Decorator function to register plugin namespace.  Used as:
    
    @register_plugin()
    class MyPlugin(CementPlugin):
        ...
    """
    def decorate(func):
        """
        Decorate a plugin class and add the namespace to global namespaces.
        """
        nms = func.__module__.split('.')

        ensure_api_compat(func.__name__, func().required_api)
        if kwargs.get('name', None):
            plugin_name = kwargs['name']
        else:
            plugin_name = nms[-1]
        define_namespace(plugin_name, func())
        return func
    return decorate
    
    
def load_plugin(plugin):
    """
    Load a cement type plugin.  
    
    Arguments:
    
    plugin  => Name of the plugin to load.
    """
    config = namespaces['global'].config
    log.debug("loading plugin '%s'" % plugin)
    if config.has_key('show_plugin_load') and config['show_plugin_load']:
        print 'loading %s plugin' % plugin
    
    try: 
        __import__(config['app_module'])
    except ImportError, e:
        raise CementConfigError, e
        
    loaded = False
    while True:
        # simple style : myapp/plugins/myplugin.py
        try:
            plugin_module = __import__('%s.plugins' % config['app_module'], 
                globals(), locals(), [plugin], -1)
            getattr(plugin_module, plugin)
            if namespaces.has_key(plugin):
                loaded = True
                log.debug("loaded '%s' plugin from %s.plugins.%s" % \
                    (plugin, config['app_module'], plugin))
                break
        except AttributeError, e:
            log.debug("AttributeError => %s" % e)
                
#        try:
#            plugin_module = __import__('%s.plugins.%s' % (config['app_module'], plugin), globals(), locals(),
#                   [plugin], -1)            
#            getattr(plugin_module, plugin)
#
#            if namespaces.has_key(plugin):
#                loaded = True
#                log.debug("loaded %s from %s.plugins.%s.%s.py" % \
#                    (plugin, config['app_module'], plugin, plugin))
#                break
#        except AttributeError, e:
#            log.debug("AttributeError => %s" % e)
#        except ImportError, e:
#            log.debug("ImportError => %s" % e)
            
        # load from cement plugins
        try:
            plugin_module = __import__('cement.plugins', globals(), locals(),
                   [plugin], -1)
            getattr(plugin_module, plugin)
            if namespaces.has_key(plugin):
                loaded = True
                log.debug("loaded %s from cement.plugins.%s.py" % \
                    (plugin, plugin))
                break
        except AttributeError, e:
            log.debug("AttributeError => %s" % e)
                    
        break
    
    if not loaded:
        raise CementRuntimeError, \
            "Failed loading plugin '%s', is it installed?" % plugin
        
    plugin_config_file = os.path.join(
        namespaces['global'].config['plugin_config_dir'], '%s.plugin' % plugin
        )
        
    set_config_opts_per_file(plugin, plugin, plugin_config_file)
                           
def load_all_plugins():
    """
    Attempt to load all enabled plugins.  Passes the existing config and 
    options object to each plugin and allows them to add/update each.
    """
    for res in run_hooks('pre_plugins_hook'):
        pass
        
    for plugin in namespaces['global'].config['enabled_plugins']:
        load_plugin(plugin)
        
    for (namespace, res) in run_hooks('options_hook'):
        for opt in res._get_all_options(): 
            if opt.get_opt_string() == '--help':
                pass
            else:
                namespaces[namespace].options.add_option(opt)
    
    for res in run_hooks('post_plugins_hook'):
        pass

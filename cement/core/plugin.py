
import os
        
from cement import namespaces
from cement.core.exc import *
from cement.core.hook import run_hooks
from cement.core.configuration import set_config_opts_per_file
from cement.core.namespace import CementNamespace, define_namespace
from cement.core.configuration import ensure_abi_compat

class CementPlugin(CementNamespace):
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
        nms = func.__module__.split('.')

        ensure_abi_compat(func.__name__, func().required_abi)
        if kwargs.get('name', None):
            plugin_name = kwargs['name']
        elif nms[-1] == 'pluginmain':
            plugin_name = nms[-2:][0]
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
    global namespaces
    config = namespaces['global'].config
    
    if config.has_key('show_plugin_load') and config['show_plugin_load']:
        print 'loading %s plugin' % plugin
    
    try: 
        app_module = __import__(config['app_module'])
    except ImportError, e:
        raise CementConfigError, e
    
    loaded = False
    while True:
        # simple style : myapp/plugins/myplugin.py
        try:
            plugin_module = __import__('%s.plugins' % config['app_module'], globals(), locals(),
                   [plugin], -1)
            getattr(plugin_module, plugin)
            if namespaces.has_key(plugin):
                loaded = True
                break
        except AttributeError, e:
            pass
        
        # complex style : myapp/plugins/myplugin/pluginmain.py
        try:
            plugin_module = __import__('%s.plugins.%s' % (config['app_module'], plugin), globals(), locals(),
                   ['pluginmain'], -1)
            getattr(plugin_module, 'pluginmain')

            if namespaces.has_key(plugin):
                loaded = True
                break
        except AttributeError, e:
            pass
        except ImportError, e:
            pass
            
        # load from cement plugins
        try:
            plugin_module = __import__('cement.plugins', globals(), locals(),
                   [plugin], -1)
            getattr(plugin_module, plugin)
            if namespaces.has_key(plugin):
                loaded = True
                break
        except AttributeError, e:
            pass
        
    if not loaded:
        raise CementRuntimeError, "Failed loading plugin '%s', is it installed?" % plugin
        
    plugin_config_file = os.path.join(
        namespaces['global'].config['plugin_config_dir'], '%s.plugin' % plugin
        )
        
    set_config_opts_per_file(plugin, plugin, plugin_config_file)
    
                       
def load_all_plugins():
    """
    Attempt to load all enabled plugins.  Passes the existing config and 
    options object to each plugin and allows them to add/update each.
    """
    global namespaces

    for plugin in namespaces['global'].config['enabled_plugins']:
        load_plugin(plugin)
        
    for (namespace, res) in run_hooks('options_hook'):
        for opt in res._get_all_options(): 
            if opt.get_opt_string() == '--help':
                pass
            else:
                namespaces[namespace].options.add_option(opt)
"""Methods and classes to handle Cement plugin support."""

import os
import re
        
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
    Decorator function to register plugin namespace.  
    
    Usage:    
    
    .. code-block:: python

        from cement.core.plugin import register_plugin
            
        @register_plugin()
        class ExamplePlugin(CementPlugin):
            def __init__(self):
                CementPlugin.__init__(self,
                    label='example',
                    version='0.1',
                    description='Example plugin',
                    required_api='0.5-0.6:20100115',
                    controller = 'ExampleController'
                    )    
    
    *Note: 'ExampleController' should match up with the controller object in
    myapp.controllers.example.ExampleController.*
    
    """
    def decorate(func):
        """
        Decorate a plugin class and add the namespace to global namespaces
        dictionary.
        
        """
        nms = func.__module__.split('.')
        inst_func = func()
        ensure_api_compat(func.__name__, inst_func.required_api)
        if kwargs.get('name', None):
            plugin_name = kwargs['name']
        else:
            plugin_name = nms[-1]
        
        define_namespace(plugin_name, inst_func)
        
        # Extract the actual controller object from the namespace
        (base, plugins, plugin) = func.__module__.split('.')
        mymod = __import__("%s.controllers.%s" % (base, plugin), globals(), 
                           locals(), [inst_func.controller], -1)
        controller = getattr(mymod, inst_func.controller)  
        namespaces[plugin_name].controller = controller
        
        return func
    return decorate
    
    
def load_plugin(plugin):
    """
    Load a cement plugin.  
    
    Required arguments:
    
        plugin
            Name of the plugin to load.  Should be accessible from the module
            path of 'myapp.plugins.myplugin'.
    
    """
    config = namespaces['root'].config
    m = re.match('(.*)\.plugins\.(.*)', plugin)
    if m:
        provider = m.group(1)
        plugin = m.group(2)
    else:
        provider = config['app_module']
        
    log.debug("loading plugin '%s'" % plugin)
    if config.has_key('show_plugin_load') and config['show_plugin_load']:
        print 'loading %s plugin' % plugin
    
    try: 
        __import__(provider)
    except ImportError, e:
        raise CementConfigError, 'unable to load plugin provider: %s' % e
        
    loaded = False
    try:
        plugin_module = __import__('%s.plugins' % provider, 
            globals(), locals(), [plugin], -1)
        getattr(plugin_module, plugin)
        if namespaces.has_key(plugin):
            loaded = True
            log.debug("loaded '%s' plugin from %s.plugins.%s" % \
                (plugin, provider, plugin))
    except AttributeError, e:
        log.debug('AttributeError => %s' % e)
                                
    if not loaded:
        raise CementRuntimeError, \
            "Plugin '%s' is not installed or is broken. Try --debug?" % plugin
        
    plugin_config_file = os.path.join(
        namespaces['root'].config['plugin_config_dir'], '%s.conf' % plugin
        )

    set_config_opts_per_file(plugin, plugin, plugin_config_file)
                           
def load_all_plugins():
    """
    Attempt to load all enabled plugins.  Passes the existing config and 
    options object to each plugin and allows them to add/update each.
    
    """
    for res in run_hooks('pre_plugins_hook'):
        pass # No result expected
        
    for plugin in namespaces['root'].config['enabled_plugins']:
        load_plugin(plugin)
        
    for (namespace, res) in run_hooks('options_hook'):
        for opt in res._get_all_options(): 
            if opt.get_opt_string() == '--help':
                pass
            elif opt.get_opt_string() == '--json':
                pass
            else:
                if namespaces.has_key(namespace):
                    namespaces[namespace].options.add_option(opt)
    
    for res in run_hooks('post_plugins_hook'):
        pass # No result expected

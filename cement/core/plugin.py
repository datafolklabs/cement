"""Methods and classes to handle Cement plugin support."""

import os
import re
from configobj import ConfigObj

from cement import namespaces
from cement.core.exc import CementConfigError, CementRuntimeError
from cement.core.log import get_logger
from cement.core.hook import run_hooks
from cement.core.configuration import set_config_opts_per_file, t_f_pass
from cement.core.namespace import CementNamespace, define_namespace, \
                                  get_config
from cement.core.configuration import ensure_api_compat

log = get_logger(__name__)

class CementPlugin(CementNamespace):
    """Wrapper for CementNamespace."""
    def __init__(self, *args, **kwargs):
        CementNamespace.__init__(self, *args, **kwargs)
     
def get_enabled_plugins():
    """
    Open plugin config files from plugin_config_dir and determine if they are
    enabled.  If so, append them to 'enabled_plugins' in the root config.
    Uses the namespaces['root'].config dictionary.
    
    """
    config = get_config()
    enabled_plugins = []
    # determine enabled plugins
    
    # first from config files
    for file in config['config_files']:    
        cnf = ConfigObj(file)
        for sect in cnf.sections:
            if sect != 'root' and cnf[sect].has_key('enable_plugin') \
                              and t_f_pass(cnf[sect]['enable_plugin']) == True \
                              and not sect in enabled_plugins:
                if not cnf[sect].has_key('provider'):
                    provider = config['app_module']
                else:
                    provider = cnf[sect]['provider']
                plugin = "%s.plugins.%s" % (provider, sect)
                enabled_plugins.append(plugin)

    # Then for plugin config files
    for file in os.listdir(config['plugin_config_dir']):
        path = os.path.join(config['plugin_config_dir'], file)
        if not path.endswith('.conf'):
            continue
            
        cnf = ConfigObj(path)
        for sect in cnf.sections:
            if sect != 'root' and cnf[sect].has_key('enable_plugin') \
                              and t_f_pass(cnf[sect]['enable_plugin']) == True \
                              and not sect in enabled_plugins:
                if not cnf[sect].has_key('provider'):
                    provider = config['app_module']
                else:
                    provider = cnf[sect]['provider']
                plugin = "%s.plugins.%s" % (provider, sect)
                enabled_plugins.append(plugin)
    return enabled_plugins
    
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
        plugin_module = __import__('%s.bootstrap' % provider, 
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

    for file in namespaces['root'].config['config_files']:
        set_config_opts_per_file(plugin, plugin, file)
    set_config_opts_per_file(plugin, plugin, plugin_config_file)
                           
def load_all_plugins():
    """
    Attempt to load all enabled plugins.  Passes the existing config and 
    options object to each plugin and allows them to add/update each.
    
    """
    for res in run_hooks('pre_plugins_hook'):
        pass # No result expected
       
    namespaces['root'].config['enabled_plugins'] = get_enabled_plugins()

    for plugin in namespaces['root'].config['enabled_plugins']:
        load_plugin(plugin)
        
    for (namespace, res) in run_hooks('options_hook'):
        for opt in res._get_all_options(): 
            if opt.get_opt_string() == '--help':
                pass
            else:
                if namespaces.has_key(namespace):
                    namespaces[namespace].options.add_option(opt)
                else:
                    log.warning("namespace '%s' doesn't exist!" % namespace)
    
    for res in run_hooks('post_plugins_hook'):
        pass # No result expected

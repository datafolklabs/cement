def load_plugin(config, options, plugin):
    if config['show_plugin_load']:
        print 'loading %s plugin' % plugin
    full_plugin = '%s.plugins.%s' % (config['app_name'], plugin)
    import_string = "import %s" % config['app_name']
    try:
        exec(import_string)
    except ImportError, e:
        raise CementConfigError, '%s unable to import base app!' % config['app_name']
        
    # try from 'app_name' first, then cement name space    
    import_string = "from %s.plugins import %s" % (config['app_name'], plugin)
    try:
        exec(import_string)
        setup_string = "res = %s.plugins.%s.register(config, options)" % \
            (config['app_name'], plugin)
        module_path = '%s.plugins.%s' % (config['app_name'], plugin)
    except ImportError, e:
        try:
            import_string = "from cement.plugins import %s" % plugin
            exec(import_string)
            setup_string = "res = cement.plugins.%s.register(config, options)" % \
                plugin
            module_path = 'cement.plugins.%s' % plugin
        except ImportError, e:
            raise cementConfigError, \
                'failed to load %s plugin: %s' % (plugin, e)    
    exec(setup_string)

    (plugin_config, plugin_commands, plugin_exposed, options) = res
    plugin_config_file = os.path.join(
        config['plugin_config_dir'], '%s.plugin' % plugin
        )
    plugin_config = set_config_opts_per_file(
        plugin_config, plugin, plugin_config_file
        )

    # update the config
    config['plugin_configs'][full_plugin] = plugin_config
        
    # handler hook
    try:
        handler_string = "handler = %s.get_handler_hook(config)" % module_path
        exec(handler_string)
    except AttributeError, e:
        handler = None
        
    return (config, plugin_commands, plugin_exposed, options, handler)
    
    
def load_plugins(config, options, handlers):
    p = config['enabled_plugins'][:] # make a copy
    all_plugin_commands = {}
    all_plugin_exposed = {}
                
    for plugin in p:
        full_plugin = '%s.plugins.%s' % (config['app_name'], plugin)
        res = load_plugin(config, options, plugin)
        (config, plugin_commands, plugin_exposed, options, handler) = res
        all_plugin_commands.update(plugin_commands)
        if len(plugin_exposed) > 0:
            all_plugin_exposed[full_plugin] = plugin_exposed
        if handler:
            if handler[0] in handlers:
                raise ShakedownPluginError, 'handler[%s] already provided by %s' % \
                    (handler[0], handlers[handler[0]].__module__)
            handlers[handler[0]] = handler[1]
    return (config, all_plugin_commands, all_plugin_exposed, options, handlers)
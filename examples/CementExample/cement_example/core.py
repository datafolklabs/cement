"""An example application using the Cement framework."""

from cement.core.log import get_logger
from cement.core.app_setup import lay_cement
from cement.core.exc import CementArgumentError

def main():
    dcf = {} # default config
    dcf['config_source'] = ['defaults']
    dcf['app_name'] = 'cement-example' 
    dcf['app_module'] = 'cement_example'
    dcf['config_file'] = './etc/%s/%s.conf' % (dcf['app_name'], dcf['app_name'])
    dcf['enabled_plugins'] = [] # no default plugins, add via the config file
    dcf['debug'] = False
    dcf['statedir'] = './var/lib/%s' % dcf['app_name']
    dcf['datadir'] = '%s/data' % dcf['statedir']
    dcf['tmpdir'] = '%s/tmp' % dcf['statedir']
    dcf['log_file'] = '%s/log/%s.log' % (dcf['statedir'], dcf['app_name'])
    dcf['plugin_config_dir'] = './etc/%s/plugins.d' % dcf['app_name']
    dcf['plugin_dir'] = '%s/plugins.d' % dcf['statedir']
    dcf['plugins'] = {}
    
    (config, cli_opts, cli_args, commands) = lay_cement(dcf)
    
    log = get_logger(__name__)
    log.debug("Cement Framework Initialized!")
    
    # react to passed commands, we add a 'getconfig' by default to easily 
    # spit out the config dict after all the plugins, cli options, etc
    # have been merged together.
    try:
        if not len(cli_args) > 0:
            raise CementArgumentError, "A command is required. See --help?"
            
        if commands.has_key(cli_args[0]):
            # commands are all the plugin commands that have been registered.
            # if cli_args[0] matches a plugin command then we execute it.
            commands[cli_args[0]](config, cli_opts, cli_args)
            
        else:
            raise CementArgumentError, "Unknown command, see --help?"
            
    except CementArgumentError, e:
        print("CementArgumentError > %s" % e)
        
if __name__ == '__main__':
    main()
    

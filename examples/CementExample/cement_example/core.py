
from cement.core.log import get_logger
from cement.core.app_setup import lay_cement
from cement.core.exc import CementArgumentError

def main():
    dcf = {} # default config
    dcf['config_source'] = ['defaults']
    dcf['app_name'] = 'cement-example' 
    dcf['app_module'] = 'cement_example'
    dcf['config_file'] = './etc/%s.conf' % dcf['app_name']
    dcf['enabled_plugins'] = []
    dcf['debug'] = False
    dcf['statedir'] = './var/lib/%s' % dcf['app_name']
    dcf['datadir'] = '%s/data' % dcf['statedir']
    dcf['tmpdir'] = '%s/tmp' % dcf['statedir']
    dcf['log_file'] = '%s/log/%s.log' % (dcf['statedir'], dcf['app_name'])
    dcf['plugin_config_dir'] = './etc/plugins.d'
    dcf['plugin_dir'] = '%s/plugins.d' % dcf['statedir']
    dcf['plugins'] = []
    
    (config, cli_opts, cli_args) = lay_cement(dcf)
    
    log = get_logger(__name__)
    log.debug("Cement Framework Initialized!")
    
    # react to passed commands
    cmd = cli_args[0]
    try:
        if cmd == 'getconfig':
            if len(cli_args) == 2:
                config_key = cli_args[1]
                if config.has_key(config_key):
                    print()
                    print('config[%s] => %s' % (config_key, config[config_key]))
                    print()
            else:
                for i in config:
                    print("config[%s] => %s" % (i, config[i]))
        else:
            raise CementArgumentError, "unknown command, see --help?"
            
    except CementArgumentError, e:
        print("CementArgumentError > %s" % e)
        
if __name__ == '__main__':
    main()
    
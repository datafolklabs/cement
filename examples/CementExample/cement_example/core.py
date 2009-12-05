
from cement.core.log import get_logger
from cement.core.app_setup import lay_cement

def main():
    default_config = {
        'app_module' : 'cement_example',
        'app_script' : 'cement-example',
        'log_file' : './cement_example.log',
        'config_file' : './etc/cement-example.conf'
        }
        
    (config, cli_opts, cli_args) = lay_cement(default_config)
    
    log = get_logger(__name__)
    log.info("Logging initialized.")
    
    cmd = cli_args[0]

    try:
        if cmd == 'getconfig':
            if len(cli_args) == 2:
                config_key = cli_args[1]
                if config.has_key(config_key):
                    print
                    print 'config[%s] => %s' % (config_key, config[config_key])
                    print
            else:
                for i in config:
                    print "config[%s] => %s" % (i, config[i])
        else:
            raise CementArgumentError, "unknown command, see --help?"
    except CementArgumentError, e:
        print CementArgumentError
        
if __name__ == '__main__':
    main()
    
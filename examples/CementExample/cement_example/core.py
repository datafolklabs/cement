"""An example application using the Cement framework."""

import sys, os
import re

from cement import config
from cement.core.log import get_logger
from cement.core.app_setup import lay_cement, ensure_abi_compat
from cement.core.exc import CementArgumentError

REQUIRED_CEMENT_ABI = '20091207'

def main():
    ensure_abi_compat(__name__, REQUIRED_CEMENT_ABI)
    
    dcf = {} # default config
    dcf['config_source'] = ['defaults']
    dcf['app_name'] = 'cement-example' 
    dcf['app_egg_name'] = 'CementExample'
    dcf['app_module'] = 'cement_example'
    dcf['config_files'] = [
        os.path.join('/etc', dcf['app_name'], '%s.conf' % dcf['app_name']),
        os.path.join(os.environ['HOME'], '.%s.conf' % dcf['app_name']),
        os.path.join('./etc', dcf['app_name'], '%s.conf' % dcf['app_name']),
        ]
    dcf['enabled_plugins'] = [] # no default plugins, add via the config file
    dcf['debug'] = False
    dcf['statedir'] = './var/lib/%s' % dcf['app_name']
    dcf['datadir'] = '%s/data' % dcf['statedir']
    dcf['tmpdir'] = '%s/tmp' % dcf['statedir']
    dcf['log_file'] = '%s/log/%s.log' % (dcf['statedir'], dcf['app_name'])
    dcf['plugin_config_dir'] = './etc/%s/plugins.d' % dcf['app_name']
    dcf['plugin_dir'] = '%s/plugins.d' % dcf['statedir']
    dcf['plugins'] = {}
    
    (cli_opts, cli_args, commands, handlers) = lay_cement(dcf)

    log = get_logger(__name__)
    log.debug("Cement Framework Initialized!")
    
    # react to the passed command
    try:
        if not len(cli_args) > 0:
            raise CementArgumentError, "A command is required. See --help?"
        
        m = re.match('(.*)-help', cli_args[0])
        if m:
            # command matches a plugin command help, run help()
            if commands.has_key(m.group(1)):
                cmd = commands[m.group(1)](cli_opts, cli_args)
                cmd.help()
            else:
                raise CementArgumentError, "Unknown command, see --help?"
                
        elif commands.has_key(cli_args[0]):
            # commands are all the plugin commands that have been registered.
            # if cli_args[0] matches a plugin command then we execute it.
            cmd = commands[cli_args[0]](cli_opts, cli_args, handlers)
            cmd.run()
            
        else:
            raise CementArgumentError, "Unknown command, see --help?"
            
    except CementArgumentError, e:
        print("CementArgumentError > %s" % e)
        
if __name__ == '__main__':
    main()
    

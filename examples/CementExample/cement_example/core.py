"""An example application using the Cement framework."""

import sys, os
import re

from cement import config, commands, options
from cement.core.log import get_logger
from cement.core.app_setup import lay_cement, ensure_abi_compat, run_command
from cement.core.exc import CementArgumentError

REQUIRED_CEMENT_ABI = '20091211'

def main():
    ensure_abi_compat(__name__, REQUIRED_CEMENT_ABI)
    
    # FIX ME: Default configurations will probably need to be modified

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


    # Warning: You shouldn't modify below this point unless you know what 
    # you're doing.
    
    lay_cement(dcf)

    log = get_logger(__name__)
    log.debug("Cement Framework Initialized!")
    
    # react to the passed command.  command should be the first arg always
    try:
        if not len(sys.argv) > 0:
            raise CementArgumentError, "A command is required. See --help?"
        
        run_command(sys.argv[1])
            
    except CementArgumentError, e:
        print("CementArgumentError > %s" % e)
        
if __name__ == '__main__':
    main()
    

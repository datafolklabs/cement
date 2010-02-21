"""
This is the applications default configuration.  You can feel free to alter
this file to your needs, however it should be noted that all these variables
are overridden by settings in /etc/helloworld/helloworld.conf and/or
~/.helloworld.conf (by default) and therefore, any default configurations
you want to make obvious to your users should be set in your default config
file as packaged with the software.
"""

import os
from configobj import ConfigObj

from cement.core.exc import CementConfigError
    
# This is a sane default for development/no config    
prefix = os.path.join(os.environ['HOME'], '.helloworld')
    
dcf = ConfigObj() # default config
dcf['config_source'] = ['defaults']
dcf['app_name'] = 'helloworld' # name for cli like /etc/<app_name>
dcf['app_egg_name'] = 'helloworld' # name from setup.py
dcf['app_module'] = 'helloworld' # name of the library dir
dcf['app_basepath'] = os.path.dirname(__file__)

dcf['enabled_plugins'] = [] # no default plugins, add via the config file
dcf['debug'] = False
dcf['datadir'] = '%s/data' % prefix
dcf['tmpdir'] = '%s/tmp' % prefix
dcf['log_file'] = '%s/log/%s.log' % (prefix, dcf['app_name'])
dcf['plugin_config_dir'] = '%s/etc/plugins.d' % prefix
dcf['log_to_console'] = True
dcf['output_engine'] = 'genshi'

# By default look in /etc and ~/ for config files.  You should probably
# symlink /etc/<your_app> => ./etc/<your_app> for easy development.
dcf['config_files'] = [
    os.path.join('/etc', dcf['app_name'], '%s.conf' % dcf['app_name']),
    os.path.join(prefix, 'etc', '%s.conf' % dcf['app_name']),
    os.path.join(os.environ['HOME'], '.%s.conf' % dcf['app_name']),
    ]
    
found_config = False
for c in dcf['config_files']:
    if os.path.exists(c):
        found_config = True
        break

if not found_config:
    print "WARNING: Config not found."

default_config = dcf
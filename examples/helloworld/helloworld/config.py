"""
This is the applications default configuration.  You can feel free to alter
this file to your needs, however it should be noted that all these variables
are overridden by settings in /etc/helloworld/helloworld.conf and/or
~/.helloworld.conf (by default) and therefore, any default configurations
you want to make obvious to your users should be set in your default config
file as packaged with the software.
"""

import os
from cement.core.exc import CementConfigError
    
dcf = {} # default config
dcf['config_source'] = ['defaults']
dcf['app_name'] = 'helloworld' # name for cli like /etc/<app_name>
dcf['app_egg_name'] = 'helloworld' # name from setup.py
dcf['app_module'] = 'helloworld' # name of the library dir
dcf['app_basepath'] = os.path.dirname(__file__)

# By default look in /etc and ~/ for config files.  You should probably
# symlink /etc/<your_app> => ./etc/<your_app> for easy development.
dcf['config_files'] = [
    os.path.join('/etc', dcf['app_name'], '%s.conf' % dcf['app_name']),
    os.path.join(os.environ['HOME'], '.%s.conf' % dcf['app_name']),
    ]
dcf['enabled_plugins'] = [] # no default plugins, add via the config file
dcf['debug'] = False
dcf['statedir'] = './var/lib/%s' % dcf['app_name']
dcf['datadir'] = '%s/data' % dcf['statedir']
dcf['tmpdir'] = '%s/tmp' % dcf['statedir']
dcf['log_file'] = '%s/log/%s.log' % (dcf['statedir'], dcf['app_name'])
dcf['plugin_config_dir'] = '%s/etc/%s/plugins.d' % (dcf['statedir'], dcf['app_name'])
dcf['plugin_dir'] = '%s/plugins.d' % dcf['statedir']
dcf['plugins'] = {}
dcf['log_to_console'] = True

found_config = False
for c in dcf['config_files']:
    if os.path.exists(c):
        found_config = True
        break

if not found_config:
    print "WARNING: Config not found."

default_config = dcf
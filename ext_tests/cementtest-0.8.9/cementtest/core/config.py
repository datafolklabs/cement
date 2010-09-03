"""
This is the applications default configuration.  You can feel free to alter
this file to your needs, however it should be noted that all these variables
are overridden by settings in /etc/cementtest/cementtest.conf and/or
~/.cementtest.conf (by default) and therefore, any default configurations
you want to make obvious to your users should be set in your default config
file as packaged with the software.
"""

import os
from configobj import ConfigObj

from cement.core.exc import CementConfigError
    
# This is a sane default for development/no config    
prefix = os.path.join(os.environ['HOME'], '.cementtest')
    
dcf = ConfigObj() # default config
dcf['config_source'] = ['defaults']
dcf['app_name'] = 'cementtest' # name for cli like /etc/<app_name>
dcf['app_egg_name'] = 'cementtest' # name from setup.py
dcf['app_module'] = 'cementtest' # name of the library dir

dcf['enabled_plugins'] = [] # no default plugins, add via the config file
dcf['debug'] = False
dcf['datadir'] = '%s/data' % prefix
dcf['tmpdir'] = '%s/tmp' % prefix
dcf['log_file'] = '%s/log/%s.log' % (prefix, dcf['app_name'])
dcf['plugin_config_dir'] = '%s/etc/plugins.d' % prefix
dcf['log_to_console'] = True
dcf['output_engine'] = 'genshi'
dcf['show_plugin_load'] = False

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

def get_nose_config(prefix):
    tcf = ConfigObj() # test config
    tcf['config_files'] = [os.path.abspath('./etc/cementtest.conf-test')]
    tcf['config_source'] = ['defaults']
    tcf['app_name'] = 'cementtest' 
    tcf['app_egg_name'] = 'cementtest'
    tcf['app_module'] = 'cementtest' 
    tcf['app_basepath'] = os.path.dirname(__file__)
    tcf['nosetests'] = True
    tcf['enabled_plugins'] = [] 
    tcf['debug'] = False
    tcf['datadir'] = '%s/data' % prefix
    tcf['tmpdir'] = '%s/tmp' % prefix
    tcf['log_file'] = '%s/log/%s.log' % (prefix, tcf['app_name'])
    tcf['plugin_config_dir'] = '%s/etc/plugins.d' % prefix
    tcf['log_to_console'] = False
    tcf['output_engine'] = 'genshi'
    tcf['show_plugin_load'] = False
    return tcf
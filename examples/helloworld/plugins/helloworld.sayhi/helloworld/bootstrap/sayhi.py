"""
This bootstrap module should be used to setup parts of the sayhi plugin
that need to exist before all controllers are loaded.  It is best used to 
define/register hooks, setup namespaces, and the like.  

"""

from pkg_resources import get_distribution
from cement.core.namespace import CementNamespace, register_namespace

VERSION = get_distribution('helloworld.sayhi').version

# Setup the 'sayhi' namespace object
sayhi = CementNamespace(
    label='sayhi', 
    description='Sayhi Plugin for Helloworld',
    version=VERSION,
    controller='SayhiController',
    provider='helloworld'
    )

# Add a config option to the sayhi namespace.  This is effectively the
# default setting for the config option.  Overridden by config files, and then
# cli options.
sayhi.config['foo'] = 'bar'

# Add a cli option to the sayhi namespace.  This overrides the 
# coresponding config option if passed
sayhi.options.add_option('-F', '--foo', action='store', dest='foo',
    help='example sayhi option')

# Officialize and register the namespace
register_namespace(sayhi)


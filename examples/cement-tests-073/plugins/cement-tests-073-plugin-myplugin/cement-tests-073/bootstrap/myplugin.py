"""
This bootstrap module should be used to setup parts of the myplugin plugin
that need to exist before all controllers are loaded.  It is best used to 
define/register hooks, setup namespaces, and the like.  

"""

from cement.core.hook import define_hook
from cement.core.namespace import CementNamespace, register_namespace

define_hook('my_myplugin_hook')

# Setup the 'myplugin' namespace object
myplugin = CementNamespace('myplugin', controller='mypluginController')

# myplugin namespace default configurations, overwritten by the [myplugin] 
# section in the applications config file(s) *or* the plugin config located
# in the 'plugins.d' directory.  Once registered, this dict is accessible as:
#
#   namespaces['myplugin'].config
#
myplugin.config['foo'] = 'bar'

# myplugin namespace options.  These options show up under:
#
#   $ cementtests073pluginmyplugin myplugin --help
#
myplugin.options.add_option('-F', '--foo', action='store',
    dest='foo', default=None, help='myplugin Foo Option'
    )

# Officialize and register the namespace
register_namespace(myplugin)


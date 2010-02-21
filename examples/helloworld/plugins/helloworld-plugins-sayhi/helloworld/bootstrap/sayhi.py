"""
This bootstrap module should be used to setup parts of the sayhi plugin
that need to exist before all controllers are loaded.  It is best used to 
define/register hooks, setup namespaces, and the like.  

"""

from cement.core.hook import define_hook
from cement.core.namespace import CementNamespace, register_namespace

define_hook('my_sayhi_hook')

# Setup the 'sayhi' namespace object
sayhi = CementNamespace('sayhi', controller='sayhiController')

# sayhi namespace default configurations, overwritten by the [sayhi] 
# section in the applications config file(s) *or* the plugin config located
# in the 'plugins.d' directory.  Once registered, this dict is accessible as:
#
#   namespaces['sayhi'].config
#
sayhi.config['foo'] = 'bar'

# sayhi namespace options.  These options show up under:
#
#   $ helloworldpluginssayhi sayhi --help
#
sayhi.options.add_option('-F', '--foo', action='store',
    dest='foo', default=None, help='sayhi Foo Option'
    )

# Officialize and register the namespace
register_namespace(sayhi)


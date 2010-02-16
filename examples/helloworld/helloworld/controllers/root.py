"""
This is the RootController for the HelloWorld application.  This can be used
to expose commands to the root namespace, as well as define/register other
non-plugin namespaces for controllers to use.  
"""

from cement import namespaces
from cement.core.namespace import CementNamespace, register_namespace
from cement.core.controller import CementController, expose
from cement.core.log import get_logger

log = get_logger(__name__)

# This is an example of how to register a namespace, which should always be
# done here before the root controller.  This namespace is tied
# to the following files:
#
#   helloworld/controllers/example.py
#   helloworld/model/example.py
#   helloworld/templates/example/
#
register_namespace('example', 'ExampleController')           
    
class RootController(CementController):
    @expose('helloworld.templates.root.error', is_hidden=True)
    def error(self, *args, **kw):
        if kw.get('errors', None):
            return dict(errors=kw['errors'])
    
    @expose(is_hidden=True)
    def default(self, cli_opts, cli_args):
        """
        This is the default command method.  If no commands are passed to
        helloworld, this one will be executed.  By default it does nothing
        and does not have a template tied to it.
        
        """
        return dict()
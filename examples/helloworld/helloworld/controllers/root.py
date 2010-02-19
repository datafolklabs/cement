"""
This is the RootController for the helloworld application.  This can be used
to expose commands to the root namespace, as well as define/register other
non-plugin namespaces for controllers to use.  
"""

from cement import namespaces
from cement.core.exc import CementArgumentError
from cement.core.controller import CementController, expose
from cement.core.log import get_logger

log = get_logger(__name__)

class RootController(CementController):
    @expose('helloworld.templates.root.error', is_hidden=True)
    def error(self, *args, **kw):
        if kw.get('errors', None):
            return dict(errors=kw['errors'])
    
    @expose(is_hidden=True)
    def default(self, cli_opts, cli_args):
        """
        This is the default command method.  If no commands are passed to
        helloworld, this one will be executed.  By default it raises an
        exception.
        
        """
        raise CementArgumentError, "A command is required. See --help?"
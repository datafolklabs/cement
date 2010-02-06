"""
This is the RootController for the helloworld application.  Usually this
file will remain pretty sparse, however it is a good place for miscellaneous
commands that might not need there own namespace or controller.  
"""

from cement.core.controller import CementController, expose
from cement.core.log import get_logger

log = get_logger(__name__)

class RootController(CementController):
    @expose('helloworld.templates.root.error', is_hidden=True)
    def error(self, errors={}):
        return dict(errors=errors)
"""
This is the ExampleController for the cement_test application.  This can be used
to expose commands to the example namespace which will be accessible under:

    $ cement_test example --help
  
"""

import sys

from cement.core.namespace import get_config
from cement.core.log import get_logger
from cement.core.controller import CementController, expose
from cement.core.hook import run_hooks

log = get_logger(__name__)

class ExampleFiveController(CementController):
    @expose(namespace='example_five', is_hidden=False)
    def cmd1(self):
        foo='bar'
        print foo
        return dict(foo=foo)
        
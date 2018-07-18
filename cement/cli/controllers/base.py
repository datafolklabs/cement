
import sys
import platform
from cement import Controller
from cement.utils.version import get_version

VERSION = get_version()
PYTHON_VERSION = '.'.join([str(x) for x in sys.version_info[0:3]])
PLATFORM = platform.platform()

BANNER = """
Cement Framework %s
Python %s
Platform %s
""" % (VERSION, PYTHON_VERSION, PLATFORM)

class Base(Controller):
    class Meta:
        label = 'base'
        description = 'Cement Framework Developer Tools'
        epilog = 'Example: cement generate app /path/to/myapp'

        arguments = [
            (['-v', '--version'], {'action': 'version', 'version': BANNER}),
        ]

    def _default(self):
        self.app.args.print_help()

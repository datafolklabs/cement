"""JSON Framework Extension"""

import sys
import json
from ..core import output, backend, hook, handler
from ..utils.misc import minimal_logger

LOG = minimal_logger(__name__)


class JsonOutputHandler(output.CementOutputHandler):

    """
    This class implements the :ref:`IOutput <cement.core.output>`
    interface.  It provides JSON output from a data dictionary using the
    `json <http://docs.python.org/library/json.html>`_ module of the standard
    library.

    Note: The cement framework detects the '--json' option and suppresses
    output (same as if passing --quiet).  Therefore, if debugging or
    troubleshooting issues you must pass the --debug option to see whats
    going on.

    """
    class Meta:

        """Handler meta-data"""

        interface = output.IOutput
        """The interface this class implements."""

        label = 'json'
        """The string identifier of this handler."""

    def __init__(self, *args, **kw):
        super(JsonOutputHandler, self).__init__(*args, **kw)

    def render(self, data_dict, template=None):
        """
        Take a data dictionary and render it as Json output.  Note that the
        template option is received here per the interface, however this
        handler just ignores it.

        :param data_dict: The data dictionary to render.
        :param template: This option is completely ignored.
        :returns: A JSON encoded string.
        :rtype: str

        """
        LOG.debug("rendering output as Json via %s" % self.__module__)
        sys.stdout = backend.__saved_stdout__
        sys.stderr = backend.__saved_stderr__
        return json.dumps(data_dict)


def add_json_option(app):
    """
    This is a ``post_setup`` hook that adds the ``--json`` argument to the
    argument object.

    :param app: The application object.

    """
    app.args.add_argument('--json', dest='output_handler',
                          action='store_const',
                          help='toggle json output handler',
                          const='json')


def set_output_handler(app):
    """
    This is a ``pre_run`` hook that overrides the configured output handler
    if ``--json`` is passed at the command line.

    :param app: The application object.

    """
    if '--json' in app._meta.argv:
        app._meta.output_handler = 'json'
        app._setup_output_handler()


def load():
    """Called by the framework when the extension is 'loaded'."""
    hook.register('post_setup', add_json_option)
    hook.register('pre_run', set_output_handler)
    handler.register(JsonOutputHandler)

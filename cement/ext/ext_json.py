"""
Cement json extension module.
"""

from ..core import output
from ..utils.misc import minimal_logger
from ..ext.ext_configparser import ConfigParserConfigHandler

LOG = minimal_logger(__name__)


def suppress_output_before_run(app):
    """
    This is a ``post_argument_parsing`` hook that suppresses console output if
    the ``JsonOutputHandler`` is triggered via command line.

    :param app: The application object.

    """
    if not hasattr(app.pargs, 'output_handler_override'):
        return
    elif app.pargs.output_handler_override == 'json':
        app._suppress_output()


def unsuppress_output_before_render(app, data):
    """
    This is a ``pre_render`` that unsuppresses console output if
    the ``JsonOutputHandler`` is triggered via command line so that the JSON
    is the only thing in the output.

    :param app: The application object.

    """
    if not hasattr(app.pargs, 'output_handler_override'):
        return
    elif app.pargs.output_handler_override == 'json':
        app._unsuppress_output()


def suppress_output_after_render(app, out_text):
    """
    This is a ``post_render`` hook that suppresses console output again after
    rendering, only if the ``JsonOutputHandler`` is triggered via command
    line.

    :param app: The application object.

    """
    if not hasattr(app.pargs, 'output_handler_override'):
        return
    elif app.pargs.output_handler_override == 'json':
        app._suppress_output()


class JsonOutputHandler(output.OutputHandler):

    """
    This class implements the :ref:`Output <cement.core.output>` Handler
    interface.  It provides JSON output from a data dictionary using the
    `json <http://docs.python.org/library/json.html>`_ module of the standard
    library.  Please see the developer documentation on
    :cement:`Output Handling <dev/output>`.

    This handler forces Cement to suppress console output until
    ``app.render`` is called (keeping the output pure JSON).  If
    troubleshooting issues, you will need to pass the ``--debug`` option in
    order to unsuppress output and see what's happening.

    """
    class Meta:

        """Handler meta-data"""

        label = 'json'
        """The string identifier of this handler."""

        #: Whether or not to include ``json`` as an available choice
        #: to override the ``output_handler`` via command line options.
        overridable = False

        #: Backend JSON library module to use (`json`, `ujson`)
        json_module = 'json'

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._json = None

    def _setup(self, app):
        super()._setup(app)
        self._json = __import__(self._meta.json_module,
                                globals(), locals(), [], 0)

    def render(self, data_dict, template=None, **kw):
        """
        Take a data dictionary and render it as Json output.  Note that the
        template option is received here per the interface, however this
        handler just ignores it.  Additional keyword arguments passed to
        ``json.dumps()``.

        Args:
            data_dict (dict): The data dictionary to render.

        Keyword Args:
            template: This option is completely ignored.

        Returns:
            str: A JSON encoded string.

        """
        LOG.debug("rendering output as Json via %s" % self.__module__)
        return self._json.dumps(data_dict, **kw)


class JsonConfigHandler(ConfigParserConfigHandler):

    """
    This class implements the :ref:`Config <cement.core.config>` Handler
    interface, and provides the same functionality of
    :ref:`ConfigParserConfigHandler <cement.ext.ext_configparser>`
    but with JSON configuration files.

    """
    class Meta:

        """Handler meta-data."""

        label = 'json'

        #: Backend JSON library module to use (`json`, `ujson`).
        json_module = 'json'

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._json = None

    def _setup(self, app):
        super()._setup(app)
        self._json = __import__(self._meta.json_module,
                                globals(), locals(), [], 0)

    def _parse_file(self, file_path):
        """
        Parse JSON configuration file settings from file_path, overwriting
        existing config settings.  If the file does not exist, returns False.

        Args:
            file_path (str): The file system path to the JSON configuration
            file.

        Returns:
            bool

        """
        with open(file_path, 'r') as f:
            content = f.read()
            if content is not None and len(content) > 0:
                self.merge(self._json.loads(content))

        return True


def load(app):
    app.hook.register('post_argument_parsing', suppress_output_before_run)
    app.hook.register('pre_render', unsuppress_output_before_render)
    app.hook.register('post_render', suppress_output_after_render)
    app.handler.register(JsonOutputHandler)
    app.handler.register(JsonConfigHandler)

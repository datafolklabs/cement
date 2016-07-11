"""

The JSON Extension adds the :class:`JsonOutputHandler` to render
output in pure JSON, as well as the :class:`JsonConfigHandler` that allows
applications to use JSON configuration files as a drop-in replacement of
the default :class:`cement.ext.ext_configparser.ConfigParserConfigHandler`.

Requirements
------------

 * No external dependencies.


Configuration
-------------

This extension does not support any configuration settings.


Usage
_____

**myapp.conf**

.. code-block:: json

    {
        "myapp": {
            "foo": "bar"
        }
    }

**myapp.py**

.. code-block:: python

    from cement.core.foundation import CementApp

    class MyApp(CementApp):
        class Meta:
            label = 'myapp'
            extensions = ['json']
            config_handler = 'json'

            # you probably don't want this to be json by default.. but you can
            # output_handler = 'json'

    with MyApp() as app:
        app.run()

        # create some data
        data = dict(foo=app.config.get('myapp', 'foo'))

        app.render(data)


In general, you likely would not set ``output_handler`` to ``json``, but
rather another type of output handler that display readable output to the
end-user (i.e. Mustache, Genshi, or Tabulate).  By default Cement
adds the ``-o`` command line option to allow the end user to override the
output handler.  For example: passing ``-o json`` will override the default
output handler and set it to ``JsonOutputHandler``.

See ``CementApp.Meta.handler_override_options``.

.. code-block:: console

    $ python myapp.py -o json
    {"foo": "bar"}


What if I Want To Use UltraJson or Something Else?
--------------------------------------------------

It is possible to override the backend ``json`` library module to use, for
example if you wanted to use UltraJson (``ujson``) or another
**drop-in replacement** library.  The recommended solution would be to
override the ``JsonOutputHandler`` with you're own sub-classed version, and
modify the ``json_module`` meta-data option.

.. code-block:: python

    from cement.ext.ext_json import JsonOutputHandler

    class MyJsonHandler(JsonOutputHandler):
        class Meta:
            json_module = 'ujson'

    # then, the class must be replaced via a 'post_setup' hook

    def override_json(app):
        app.handler.register(MyJsonHandler, force=True)

    app.hook.register('post_setup', override_json)

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


class JsonOutputHandler(output.CementOutputHandler):

    """
    This class implements the :ref:`IOutput <cement.core.output>`
    interface.  It provides JSON output from a data dictionary using the
    `json <http://docs.python.org/library/json.html>`_ module of the standard
    library.  Please see the developer documentation on
    :ref:`Output Handling <dev_output_handling>`.

    This handler forces Cement to suppress console output until
    ``app.render`` is called (keeping the output pure JSON).  If
    troubleshooting issues, you will need to pass the ``--debug`` option in
    order to unsuppress output and see what's happening.

    """
    class Meta:

        """Handler meta-data"""

        interface = output.IOutput
        """The interface this class implements."""

        label = 'json'
        """The string identifier of this handler."""

        #: Whether or not to include ``json`` as an available choice
        #: to override the ``output_handler`` via command line options.
        overridable = True

        #: Backend JSON library module to use (`json`, `ujson`)
        json_module = 'json'

    def __init__(self, *args, **kw):
        super(JsonOutputHandler, self).__init__(*args, **kw)
        self._json = None

    def _setup(self, app):
        super(JsonOutputHandler, self)._setup(app)
        self._json = __import__(self._meta.json_module,
                                globals(), locals(), [], 0)

    def render(self, data_dict, template=None, **kw):
        """
        Take a data dictionary and render it as Json output.  Note that the
        template option is received here per the interface, however this
        handler just ignores it.  Additional keyword arguments passed to
        ``json.dumps()``.

        :param data_dict: The data dictionary to render.
        :keyword template: This option is completely ignored.
        :returns: A JSON encoded string.
        :rtype: ``str``

        """
        LOG.debug("rendering output as Json via %s" % self.__module__)
        return self._json.dumps(data_dict, **kw)


class JsonConfigHandler(ConfigParserConfigHandler):

    """
    This class implements the :ref:`IConfig <cement.core.config>`
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
        super(JsonConfigHandler, self).__init__(*args, **kw)
        self._json = None

    def _setup(self, app):
        super(JsonConfigHandler, self)._setup(app)
        self._json = __import__(self._meta.json_module,
                                globals(), locals(), [], 0)

    def _parse_file(self, file_path):
        """
        Parse JSON configuration file settings from file_path, overwriting
        existing config settings.  If the file does not exist, returns False.

        :param file_path: The file system path to the JSON configuration file.
        :returns: boolean

        """
        self.merge(self._json.load(open(file_path)))

        # FIX ME: Should check that file was read properly, however if not it
        # will likely raise an exception anyhow.
        return True


def load(app):
    app.hook.register('post_argument_parsing', suppress_output_before_run)
    app.hook.register('pre_render', unsuppress_output_before_render)
    app.hook.register('post_render', suppress_output_after_render)
    app.handler.register(JsonOutputHandler)
    app.handler.register(JsonConfigHandler)

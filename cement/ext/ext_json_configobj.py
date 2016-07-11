"""
The JSON ConfigObj Extension is a combination of the
:class:`JsonConfigHandler` and :class:`ConfigObjConfigHandler` which allows
the application to read JSON configuration files into a ConfigObj based
configuration handler.

Requirements
------------

 * ConfigObj (``pip install configobj``)


Configuration
-------------

This extension does not support any configuration settings.


Usage
-----

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
            extensions = ['json_configobj']
            config_handler = 'json_configobj'

    with MyApp() as app:
        app.run()

        # get config settings
        app.config['myapp']['foo']

        # set config settings
        app.config['myapp']['foo'] = 'bar2'

        # etc...


"""

from ..utils.misc import minimal_logger
from ..ext.ext_configobj import ConfigObjConfigHandler

LOG = minimal_logger(__name__)


class JsonConfigObjConfigHandler(ConfigObjConfigHandler):

    """
    This class implements the :ref:`IConfig <cement.core.config>`
    interface, and provides the same functionality of
    :ref:`ConfigObjConfigHandler <cement.ext.ext_configobj>`
    but with JSON configuration files.

    **Note** This extension has an external dependency on ``ConfigObj``.  You
    must include ``configobj`` in your application's dependencies as Cement
    explicitly does *not* include external dependencies for optional
    extensions.

    """

    class Meta:

        """Handler meta-data."""

        #: The string identifier of this handler.
        label = 'json_configobj'

        #: Backend JSON module to use (``json``, ``ujson``, etc)
        json_module = 'json'

    def __init__(self, *args, **kw):
        super(JsonConfigObjConfigHandler, self).__init__(*args, **kw)
        self._json = None

    def _setup(self, app):
        super(JsonConfigObjConfigHandler, self)._setup(app)
        self._json = __import__(self._meta.json_module,
                                globals(), locals(), [], 0)

    def _parse_file(self, file_path):
        """
        Parse JSON configuration file settings from ``file_path``, overwriting
        existing config settings.  If the file does not exist, returns
        ``False``.

        :param file_path: The file system path to the JSON configuration file.
        :returns: boolean

        """
        self.merge(self._json.load(open(file_path)))

        # FIX ME: Should check that file was read properly, however if not it
        # will likely raise an exception anyhow.
        return True


def load(app):
    app.handler.register(JsonConfigObjConfigHandler)

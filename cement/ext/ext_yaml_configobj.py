"""
The Yaml ConfigObj Extension is a combination of the
:class:`YamlConfigHandler` and :class:`ConfigObjConfigHandler` which allows
the application to read Yaml configuration files into a ConfigObj based
configuration handler.

Requirements
------------

 * ConfigObj (``pip install configobj``)
 * pyYaml (``pip install pyYaml``)


Configuration
-------------

This extension does not honor any application configuration settings.


Usage
-----

**myapp.conf**

.. code-block:: yaml

    ---
        myapp:
            foo: bar

**myapp.py**

.. code-block:: python

    from cement.core.foundation import CementApp

    class MyApp(CementApp):
        class Meta:
            label = 'myapp'
            extensions = ['yaml_configobj']
            config_handler = 'yaml_configobj'

    with MyApp() as app:
        app.run()

        # get config settings
        app.config['myapp']['foo']

        # set config settings
        app.config['myapp']['foo'] = 'bar2'

        # etc...

"""

import yaml
from ..utils.misc import minimal_logger
from ..ext.ext_configobj import ConfigObjConfigHandler

LOG = minimal_logger(__name__)


class YamlConfigObjConfigHandler(ConfigObjConfigHandler):

    """
    This class implements the :ref:`IConfig <cement.core.config>`
    interface, and provides the same functionality of
    :ref:`ConfigObjConfigHandler <cement.ext.ext_configobj>`
    but with YAML configuration files.  See
    `pyYAML <http://pyyaml.org/wiki/PyYAMLDocumentation>`_ for more
    information on pyYAML

    **Note** This extension has an external dependency on `pyYAML` and
    `ConfigObj`.  You must include `pyYAML` and `configobj` in your
    application's dependencies as Cement explicitly does *not* include
    external dependencies for optional extensions.

    """

    class Meta:

        """Handler meta-data."""

        label = 'yaml_configobj'

    def __init__(self, *args, **kw):
        super(YamlConfigObjConfigHandler, self).__init__(*args, **kw)

    def _parse_file(self, file_path):
        """
        Parse YAML configuration file settings from file_path, overwriting
        existing config settings.  If the file does not exist, returns False.

        :param file_path: The file system path to the YAML configuration file.
        :returns: boolean

        """
        self.merge(yaml.load(open(file_path)))

        # FIX ME: Should check that file was read properly, however if not it
        # will likely raise an exception anyhow.
        return True


def load(app):
    app.handler.register(YamlConfigObjConfigHandler)

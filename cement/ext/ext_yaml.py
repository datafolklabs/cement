"""
The Yaml Extension adds the :class:`YamlOutputHandler` to render
output in pure Yaml, as well as the :class:`YamlConfigHandler` that allows
applications to use Yaml configuration files as a drop-in replacement of
the default :class:`cement.ext.ext_configparser.ConfigParserConfigHandler`.

Requirements
------------

 * pyYaml (``pip install pyYaml``)


Configuration
-------------

This extension does not honor any application configuration settings.


Usage
_____

**myapp.conf**

.. code-block:: Yaml

    ---
    myapp:
        foo: bar

**myapp.py**

.. code-block:: python

    from cement.core.foundation import CementApp

    class MyApp(CementApp):
        class Meta:
            label = 'myapp'
            extensions = ['Yaml']
            config_handler = 'Yaml'

            # you probably don't want to do this.. but you can
            # output_handler = 'Yaml'

    with MyApp() as app:
        app.run()

        # create some data
        data = dict(foo=app.config.get('myapp', 'foo'))

        app.render(data)


In general, you likely would not set ``output_handler`` to ``Yaml``, but
rather another type of output handler that displays readable output to the
end-user (i.e. Mustache, Genshi, or Tabulate).  By default Cement
adds the ``-o`` command line option to allow the end user to override the
output handler.  For example: passing ``-o Yaml`` will override the default
output handler and set it to ``YamlOutputHandler``.

See ``CementApp.Meta.handler_override_options``.

.. code-block:: console

    $ python myapp.py -o Yaml
    {foo: bar}

"""

import os
import sys
import yaml
from ..core import backend, output, config
from ..utils.misc import minimal_logger
from ..ext.ext_configparser import ConfigParserConfigHandler

LOG = minimal_logger(__name__)


def suppress_output_before_run(app):
    """
    This is a ``post_argument_parsing`` hook that suppresses console output if
    the ``YamlOutputHandler`` is triggered via command line.

    :param app: The application object.

    """
    if not hasattr(app.pargs, 'output_handler_override'):
        return
    elif app.pargs.output_handler_override == 'yaml':
        app._suppress_output()


def unsuppress_output_before_render(app, data):
    """
    This is a ``pre_render`` that unsuppresses console output if
    the ``YamlOutputHandler`` is triggered via command line so that the Yaml
    is the only thing in the output.

    :param app: The application object.

    """
    if not hasattr(app.pargs, 'output_handler_override'):
        return
    elif app.pargs.output_handler_override == 'yaml':
        app._unsuppress_output()


def suppress_output_after_render(app, out_text):
    """
    This is a ``post_render`` hook that suppresses console output again after
    rendering, only if the ``YamlOutputHandler`` is triggered via command
    line.

    :param app: The application object.

    """
    if not hasattr(app.pargs, 'output_handler_override'):
        return
    elif app.pargs.output_handler_override == 'yaml':
        app._suppress_output()


class YamlOutputHandler(output.CementOutputHandler):

    """
    This class implements the :ref:`IOutput <cement.core.output>`
    interface.  It provides Yaml output from a data dictionary and uses
    `pyYaml <http://pyYaml.org/wiki/PyYamlDocumentation>`_ to dump it to
    STDOUT.  Please see the developer documentation on
    :ref:`Output Handling <dev_output_handling>`.

    This handler forces Cement to suppress console output until
    ``app.render`` is called (keeping the output pure Yaml).  If
    troubleshooting issues, you will need to pass the ``--debug`` option in
    order to unsuppress output and see what's happening.

    """

    class Meta:

        """Handler meta-data."""

        interface = output.IOutput
        label = 'yaml'

        #: Whether or not to include ``Yaml`` as an available to choice
        #: to override the ``output_handler`` via command line options.
        overridable = True

    def __init__(self, *args, **kw):
        super(YamlOutputHandler, self).__init__(*args, **kw)
        self.config = None

    def _setup(self, app_obj):
        self.app = app_obj

    def render(self, data_dict, **kw):
        """
        Take a data dictionary and render it as Yaml output.  Note that the
        template option is received here per the interface, however this
        handler just ignores it.

        :param data_dict: The data dictionary to render.
        :returns: A Yaml encoded string.
        :rtype: ``str``

        """
        LOG.debug("rendering output as yaml via %s" % self.__module__)
        return yaml.dump(data_dict)


class YamlConfigHandler(ConfigParserConfigHandler):

    """
    This class implements the :ref:`IConfig <cement.core.config>`
    interface, and provides the same functionality of
    :ref:`ConfigParserConfigHandler <cement.ext.ext_configparser>`
    but with Yaml configuration files.  See
    `pyYaml <http://pyYaml.org/wiki/PyYamlDocumentation>`_ for more
    information on pyYaml.

    **Note** This extension has an external dependency on `pyYaml`.  You must
    include `pyYaml` in your application's dependencies as Cement explicitly
    does *not* include external dependencies for optional extensions.

    """
    class Meta:
        label = 'yaml'

    def __init__(self, *args, **kw):
        super(YamlConfigHandler, self).__init__(*args, **kw)

    def _parse_file(self, file_path):
        """
        Parse Yaml configuration file settings from file_path, overwriting
        existing config settings.  If the file does not exist, returns False.

        :param file_path: The file system path to the Yaml configuration file.
        :returns: boolean

        """
        self.merge(yaml.load(open(file_path)))

        # FIX ME: Should check that file was read properly, however if not it
        # will likely raise an exception anyhow.
        return True


def load(app):
    app.hook.register('post_argument_parsing', suppress_output_before_run)
    app.hook.register('pre_render', unsuppress_output_before_render)
    app.hook.register('post_render', suppress_output_after_render)
    app.handler.register(YamlOutputHandler)
    app.handler.register(YamlConfigHandler)

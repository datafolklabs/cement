"""
Cement yaml extension module.
"""

import yaml
from ..core import output
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


class YamlOutputHandler(output.OutputHandler):

    """
    This class implements the :ref:`Output <cement.core.output>` Handler
    interface.  It provides Yaml output from a data dictionary and uses
    `pyYaml <http://pyYaml.org/wiki/PyYamlDocumentation>`_ to dump it to
    STDOUT.  Please see the developer documentation on
    :cement:`Output Handling <dev/output>`.

    This handler forces Cement to suppress console output until
    ``app.render`` is called (keeping the output pure Yaml).  If
    troubleshooting issues, you will need to pass the ``--debug`` option in
    order to unsuppress output and see what's happening.

    """

    class Meta:

        """Handler meta-data."""

        label = 'yaml'

        #: Whether or not to include ``yaml`` as an available choice
        #: to override the ``output_handler`` via command line options.
        overridable = False

    def __init__(self, *args, **kw):
        super(YamlOutputHandler, self).__init__(*args, **kw)
        self.config = None

    def _setup(self, app_obj):
        self.app = app_obj

    def render(self, data_dict, template=None, **kw):
        """
        Take a data dictionary and render it as Yaml output.  Note that the
        template option is received here per the interface, however this
        handler just ignores it.  Additional keyword arguments passed to
        ``yaml.dump()``.

        Args:
            data_dict (dict): The data dictionary to render.

        Keyword Args:
            template (str): Ignored in this output handler implementation.

        Returns:
            str: A Yaml encoded string.

        """
        LOG.debug("rendering output as yaml via %s" % self.__module__)
        return yaml.dump(data_dict, **kw)


class YamlConfigHandler(ConfigParserConfigHandler):

    """
    This class implements the :ref:`Config <cement.core.config>` Handler
    interface, and provides the same functionality of
    :ref:`ConfigParserConfigHandler <cement.ext.ext_configparser>`
    but with Yaml configuration files.  See
    `pyYaml <http://pyYaml.org/wiki/PyYamlDocumentation>`_ for more
    information on pyYaml.

    **Note** This extension has an external dependency on `pyYaml`.  You must
    include `pyYaml` in your application's dependencies as Cement explicitly
    does *not* include external dependencies for optional extensions.

    Due to changes in pyYaml version 5.1 to deprecate `yaml.load` without
    specifying a `Loader=...`, this class will attempt to parse the yaml
    content with the 5.1 sugar method `full_load`, falling back to the
    "unsafe" call for versions prior to 5.1.  The `full_load` method uses
    the FullLoader, which is the default Loader when none is provided.  See
    the pyYaml message on this deprecation: https://msg.pyyaml.org/load

    """
    class Meta:
        label = 'yaml'

    def __init__(self, *args, **kw):
        super(YamlConfigHandler, self).__init__(*args, **kw)

    def _parse_file(self, file_path):
        """
        Parse Yaml configuration file settings from file_path, overwriting
        existing config settings.  If the file does not exist, returns False.

        Args:
            file_path (str): The file system path to the Yaml configuration
                             file.

        """
        yaml_load = yaml.full_load if hasattr(yaml, 'full_load') else yaml.load

        with open(file_path, 'r') as f:
            content = f.read()
            if content is not None and len(content) > 0:
                self.merge(yaml_load(content))

        return True


def load(app):
    app.hook.register('post_argument_parsing', suppress_output_before_run)
    app.hook.register('pre_render', unsuppress_output_before_render)
    app.hook.register('post_render', suppress_output_after_render)
    app.handler.register(YamlOutputHandler)
    app.handler.register(YamlConfigHandler)

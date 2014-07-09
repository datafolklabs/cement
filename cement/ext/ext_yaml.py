"""YAML Framework Extension"""

import os
import sys
import yaml
from ..core import backend, output, hook, handler
from ..utils.misc import minimal_logger
import cement.ext.ext_configparser

LOG = minimal_logger(__name__)


class YamlOutputHandler(output.CementOutputHandler):
    """
    This class implements the :ref:`IOutput <cement.core.output>`
    interface.  It provides YAML output from a data dictionary and uses
    `pyYAML <http://pyyaml.org/wiki/PyYAMLDocumentation>`_ to dump it to
    STDOUT.

    Note: The cement framework detects the '--yaml' option and suppresses
    output (same as if passing --quiet).  Therefore, if debugging or
    troubleshooting issues you must pass the --debug option to see whats
    going on.

    """
    class Meta:
        interface = output.IOutput
        label = 'yaml'

    def __init__(self, *args, **kw):
        super(YamlOutputHandler, self).__init__(*args, **kw)
        self.config = None

    def _setup(self, app_obj):
        self.app = app_obj

    def render(self, data_dict, template=None):
        """
        Take a data dictionary and render it as Yaml output.  Note that the
        template option is received here per the interface, however this
        handler just ignores it.

        :param data_dict: The data dictionary to render.
        :param template: This option is completely ignored.
        :returns: A Yaml encoded string.
        :rtype: str

        """
        LOG.debug("rendering output as Yaml via %s" % self.__module__)
        sys.stdout = backend.__saved_stdout__
        sys.stderr = backend.__saved_stderr__
        return yaml.dump(data_dict)


def add_yaml_option(app):
    """
    This is a ``post_setup`` hook that adds the ``--yaml`` argument to the
    command line.

    :param app: The application object.

    """
    app.args.add_argument('--yaml',
                          dest='output_handler',
                          action='store_const',
                          help='toggle yaml output handler',
                          const='yaml')


def set_output_handler(app):
    """
    This is a ``pre_run`` hook that overrides the configured output handler
    if ``--yaml`` is passed at the command line.

    :param app: The application object.

    """
    if '--yaml' in app._meta.argv:
        app._meta.output_handler = 'yaml'
        app._setup_output_handler()


class YamlConfigHandler(cement.ext.ext_configobj.ConfigObjConfigHandler):
    class Meta:
        interface = cement.core.config.IConfig
        label = 'yaml'

    def parse_file(self, file_path):
        file_path = os.path.abspath(os.path.expanduser(file_path))
        if os.path.exists(file_path):
            LOG.debug("config file '%s' exists, loading settings..." %
                    file_path)
            self.merge(dict(yaml.load(open(file_path))))
            return True
        else:
            LOG.debug("config file '%s' does not exist, skipping..." %
                      file_path)
            return False


def load():
    """Called by the framework when the extension is 'loaded'."""
    handler.register(YamlOutputHandler)
    handler.register(YamlConfigHandler)
    hook.register('post_setup', add_yaml_option)
    hook.register('pre_run', set_output_handler)

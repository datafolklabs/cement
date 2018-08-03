"""
Cement handlebars extension module.
"""

import pybars._compiler
from cement.core.output import OutputHandler
from cement.core.template import TemplateHandler
from cement.utils.misc import minimal_logger

# Monkey patch so we don't escape HTML (not clear how else to do this)
# See: https://github.com/wbond/pybars3/issues/25
original_prepare = pybars._compiler.prepare


def my_prepare(value, escape):
    return original_prepare(value, False)


pybars._compiler.prepare = my_prepare

from pybars import Compiler  # noqa


LOG = minimal_logger(__name__)


class HandlebarsOutputHandler(OutputHandler):

    """
    This class implements the :ref:`IOutput <cement.core.output>`
    interface.  It provides text output from template and uses the
    `Handlebars Templating Language <http://handlebarsjs.com/>`_ for Python
    via the ``pybars`` library.  Please see the developer documentation on
    :cement:`Output Handling <dev/output>`.

    **Note** This extension has an external dependency on ``pybars3``.  You
    must include ``pybars3`` in your applications dependencies as Cement
    explicitly does **not** include external dependencies for optional
    extensions.
    """

    class Meta:

        """Handler meta-data."""

        #: The string identifier of the handler.
        label = 'handlebars'

        #: Whether or not to include ``handlebars`` as an available to choice
        #: to override the ``output_handler`` via command line options.
        overridable = False

    def __init__(self, *args, **kw):
        super(HandlebarsOutputHandler, self).__init__(*args, **kw)
        self.templater = None

    def _setup(self, app):
        super(HandlebarsOutputHandler, self)._setup(app)
        self.templater = self.app.handler.resolve('template', 'handlebars',
                                                  setup=True)

    def render(self, data, template):
        """
        Take a data dictionary and render it using the given template file.

        Args:
            data (dict): The data dictionary to render.

        Keyword Args:
            template (str): The path to the template, after the
                ``template_module`` or ``template_dirs`` prefix as defined in
                the application.

        Returns:
            str: The rendered template text

        """
        LOG.debug("rendering output using '%s' as a template." % template)
        content, _type, _path = self.templater.load(template)
        res = self.templater.render(content, data)
        return res


class HandlebarsTemplateHandler(TemplateHandler):

    """
    This class implements the :ref:`Template <cement.core.template>` Handler
    interface.  It renders content as template, and supports copying entire
    source template directories using the
    `Handlebars Templating Language <http://handlebarsjs.com/>`_ for Python
    via the ``pybars`` library.  Please see the developer documentation on
    :cement:`Template Handling <dev/template>`.

    **Note** This extension has an external dependency on ``pybars3``.  You
    must include ``pybars3`` in your applications dependencies as Cement
    explicitly does **not** include external dependencies for optional
    extensions.
    """

    class Meta:

        """Handler meta-data."""

        #: Handler label
        label = 'handlebars'

        #: Custom helpers
        helpers = {}

        #: List of partials to preload
        partials = []

    def __init__(self, *args, **kw):
        super(HandlebarsTemplateHandler, self).__init__(*args, **kw)
        self._raw_partials = {}

    def _setup(self, app):
        super(HandlebarsTemplateHandler, self)._setup(app)
        if hasattr(self.app._meta, 'handlebars_helpers'):
            self._meta.helpers = self.app._meta.handlebars_helpers
        if hasattr(self.app._meta, 'handlebars_partials'):
            self._meta.partials = self.app._meta.handlebars_partials
        for partial in self._meta.partials:
            self._raw_partials[partial], _type, _path = self.load(partial)

    def _clean_content(self, content):
        if not isinstance(content, str):
            content = content.decode('utf-8')

        return content

    def render(self, content, data):
        """
        Render the given ``content`` as template with the ``data`` dictionary.

        Args:
            content (str): The template content to render.
            data (dict): The data dictionary to render.

        Returns:
            str: The rendered template text

        """

        bars = Compiler()
        content = bars.compile(self._clean_content(content))

        # need to render partials
        partials = {}
        for key, val in self._raw_partials.items():
            partials[key] = bars.compile(self._clean_content(val))

        return content(data, helpers=self._meta.helpers, partials=partials)


def load(app):
    app.handler.register(HandlebarsOutputHandler)
    app.handler.register(HandlebarsTemplateHandler)

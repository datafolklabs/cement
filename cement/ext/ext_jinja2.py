"""
Cement jinja2 extension module.

**Note** This extension has an external dependency on ``jinja2``. Cement
explicitly does **not** include external dependencies for optional
extensions.

* In Cement ``>=3.0.8`` you must include ``cement[jinja2]`` in your
  applications dependencies.
* In Cement ``<3.0.8`` you must include ``jinja2`` in your applications
  dependencies.
"""

from ..core.output import OutputHandler
from ..core.template import TemplateHandler
from ..utils.misc import minimal_logger
from jinja2 import Environment, FileSystemLoader, PackageLoader

LOG = minimal_logger(__name__)


class Jinja2OutputHandler(OutputHandler):

    """
    This class implements the :ref:`OutputHandler <cement.core.output>`
    interface.  It provides text output from template and uses the
    `Jinja2 Templating Language
    <http://jinja.pocoo.org/>`_.
    Please see the developer documentation on
    :cement:`Output Handling <dev/output>`.

    """

    class Meta:

        """Handler meta-data."""

        label = 'jinja2'

    def __init__(self, *args, **kw):
        super(Jinja2OutputHandler, self).__init__(*args, **kw)
        self.templater = None

    def _setup(self, app):
        super(Jinja2OutputHandler, self)._setup(app)
        self.templater = self.app.handler.resolve('template', 'jinja2',
                                                  setup=True)

    def render(self, data, template=None, **kw):
        """
        Take a data dictionary and render it using the given template file.
        Additional keyword arguments are ignored.

        Args:
            data (dict): The data dictionary to render.

        Keyword Args:
            template (str): The path to the template, after the
                ``template_module`` or ``template_dirs`` prefix as defined in
                the application.

        Returns:
            str: The rendered template text

        """

        LOG.debug("rendering content using '%s' as a template." % template)
        content, _type, _path = self.templater.load(template)
        return self.templater.render(content, data)


class Jinja2TemplateHandler(TemplateHandler):

    """
    This class implements the :ref:`Template <cement.core.template>` Handler
    interface.  It renders content as template, and supports copying entire
    source template directories using the
    `Jinja2 Templating Language <http://jinja.pocoo.org/>`_.  Please
    see the developer documentation on
    :cement:`Template Handling <dev/template>`.
    """

    class Meta:

        """Handler meta-data."""

        label = 'jinja2'

    def __init__(self, *args, **kw):
        super(Jinja2TemplateHandler, self).__init__(*args, **kw)

        # expose Jinja2 Environment instance so that we can manipulate it
        # higher in application code if necessary
        self.env = Environment(keep_trailing_newline=True)

    def load(self, *args, **kw):
        """
        Loads a template file first from ``self.app._meta.template_dirs`` and
        secondly from ``self.app._meta.template_module``.  The
        ``template_dirs`` have presedence.

        Args:
            template_path (str): The secondary path of the template **after**
                either ``template_module`` or ``template_dirs`` prefix (set via
                ``App.Meta``)

        Returns:
            tuple: The content of the template (``str``), the type of template
            (``str``: ``directory``, or ``module``), and the path (``str``) of
            the directory or module)

        Raises:
            cement.core.exc.FrameworkError: If the template does not exist in
                either the ``template_module`` or ``template_dirs``.
        """
        content, _type, _path = super(Jinja2TemplateHandler, self).load(*args,
                                                                        **kw)

        if _type == 'directory':
            self.env.loader = FileSystemLoader(self.app._meta.template_dirs)
        elif _type == 'module':
            parts = self.app._meta.template_module.rsplit('.', 1)
            self.env.loader = PackageLoader(parts[0], package_path=parts[1])

        return content, _type, _path

    def render(self, content, data, *args, **kw):
        """
        Render the given ``content`` as template with the ``data`` dictionary.

        Args:
            content (str): The template content to render.
            data (dict): The data dictionary to render.

        Returns:
            str: The rendered template text

        """
        LOG.debug("rendering content as text via %s" % self.__module__)

        if not isinstance(content, str):
            content = content.decode('utf-8')

        tmpl = self.env.from_string(content)
        res = tmpl.render(**data)
        return res


def load(app):
    app.handler.register(Jinja2OutputHandler)
    app.handler.register(Jinja2TemplateHandler)

"""Genshi extension module."""

import sys
from ..core import output, exc, handler
from ..utils.misc import minimal_logger

if sys.version_info[0] >= 3:
    raise exc.CementRuntimeError('Genshi does not support Python 3.') \
        # pragma: no cover

from genshi.template import NewTextTemplate
LOG = minimal_logger(__name__)


class GenshiOutputHandler(output.TemplateOutputHandler):
    """
    This class implements the :ref:`IOutput <cement.core.output>`
    interface.  It provides text output from template and uses the
    `Genshi Text Templating Language
    <http://genshi.edgewall.org/wiki/Documentation/text-templates.html>`_.
    **Note** This extension has an external dependency on ``genshi``.  You
    must include ``genshi`` in your applications dependencies as Cement
    explicitly does *not* include external dependencies for optional
    extensions.

    Usage:

    .. code-block:: python

        from cement.core import foundation

        class MyApp(foundation.CementApp):
            class Meta:
                label = 'myapp'
                extensions = ['genshi']
                output_handler = 'genshi'
                template_module = 'myapp.templates'
                template_dir = '/usr/lib/myapp/templates'
        # ...

    From here, you would then put a Genshi template file in
    ``myapp/templates/my_template.genshi`` and then render a data dictionary
    with it:

    .. code-block:: python

        # via the app object
        myapp.render(some_data_dict, 'my_template.genshi')

        # or from within a controller or handler
        self.app.render(some_data_dict, 'my_template.genshi')



    Configuration:

    This extension honors the ``template_dir`` configuration option under the
    base configuration section of any application configuration file.  It
    also honors the ``template_module`` and ``template_dir`` meta options
    under the main application object.

    """

    class Meta:
        interface = output.IOutput
        label = 'genshi'

    def render(self, data_dict, template):
        """
        Take a data dictionary and render it using the given template file.

        Required Arguments:

        :param data_dict: The data dictionary to render.
        :param template: The path to the template, after the
            ``template_module`` or ``template_dir`` prefix as defined in the
            application.
        :returns: str (the rendered template text)

        """
        LOG.debug("rendering output using '%s' as a template." % template)
        content = self.load_template(template)
        tmpl = NewTextTemplate(content)
        return tmpl.generate(**data_dict).render()


def load():
    handler.register(GenshiOutputHandler)

"""Mustache extension module."""

import sys
import pystache
from ..core import output, exc, handler
from ..utils.misc import minimal_logger

LOG = minimal_logger(__name__)


class MustacheOutputHandler(output.TemplateOutputHandler):
    """
    This class implements the :ref:`IOutput <cement.core.output>`
    interface.  It provides text output from template and uses the
    `Mustache Templating Language <http://mustache.github.com>`_.  Please
    see the developer documentation on
    :ref:`Output Handling <dev_output_handling>`.

    **Note** This extension has an external dependency on ``pystache``.  You
    must include ``pystache`` in your applications dependencies as Cement
    explicitly does **not** include external dependencies for optional
    extensions.

    Usage:

    .. code-block:: python

        from cement.core import foundation

        class MyApp(foundation.CementApp):
            class Meta:
                label = 'myapp'
                extensions = ['mustache']
                output_handler = 'mustache'
                template_module = 'myapp.templates'
                template_dirs = [
                    '~/.myapp/templates',
                    '/usr/lib/myapp/templates',
                    ]
        # ...

    Note that the above ``template_module`` and ``template_dirs`` are the
    auto-defined defaults but are added here for clarity.  From here, you
    would then put a Mustache template file in
    ``myapp/templates/my_template.mustache`` and then render a data dictionary
    with it:

    .. code-block:: python

        # via the app object
        myapp.render(some_data_dict, 'my_template.mustache')

        # or from within a controller or handler
        self.app.render(some_data_dict, 'my_template.mustache')



    Configuration:

    To **prepend** a directory to the ``template_dirs`` list defined by the
    application/developer, an end-user can add the configuration option
    ``template_dir`` to their application configuration file under the main
    config section:

    .. code-block:: text

        [myapp]
        template_dir = /path/to/my/templates


    """

    class Meta:
        interface = output.IOutput
        label = 'mustache'

    def render(self, data_dict, template):
        """
        Take a data dictionary and render it using the given template file.

        Required Arguments:

        :param data_dict: The data dictionary to render.
        :param template: The path to the template, after the
         ``template_module`` or ``template_dirs`` prefix as defined in the
         application.
        :returns: str (the rendered template text)

        """
        LOG.debug("rendering output using '%s' as a template." % template)
        content = self.load_template(template)
        return pystache.render(content, data_dict)


def load(app):
    handler.register(MustacheOutputHandler)

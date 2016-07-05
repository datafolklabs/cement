"""
The Jinja2 Extension module provides output templating based on the
`Jinja2 Templating Language \
<http://jinja.pocoo.org/>`_.


Requirements
------------

 * Jinja2 (``pip install Jinja2``)


Configuration
-------------

To **prepend** a directory to the ``template_dirs`` list defined by the
application/developer, an end-user can add the configuration option
``template_dir`` to their application configuration file under the main
config section:

.. code-block:: text

    [myapp]
    template_dir = /path/to/my/templates


Usage
-----

.. code-block:: python

    from cement.core.foundation import CementApp

    class MyApp(CementApp):
        class Meta:
            label = 'myapp'
            extensions = ['jinja2']
            output_handler = 'jinja2'
            template_module = 'myapp.templates'
            template_dirs = [
                '~/.myapp/templates',
                '/usr/lib/myapp/templates',
                ]

    with MyApp() as app:
        app.run()

        # create some data
        data = dict(foo='bar')

        # render the data to STDOUT (default) via a template
        app.render(data, 'my_template.jinja2')


Note that the above ``template_module`` and ``template_dirs`` are the
auto-defined defaults but are added here for clarity.  From here, you
would then put a Jinja2 template file in
``myapp/templates/my_template.jinja2`` or
``/usr/lib/myapp/templates/my_template.jinja2``.

"""

from ..core import output
from ..utils.misc import minimal_logger
from jinja2 import Environment

LOG = minimal_logger(__name__)


class Jinja2OutputHandler(output.TemplateOutputHandler):

    """
    This class implements the :ref:`IOutput <cement.core.output>`
    interface.  It provides text output from template and uses the
    `Jinja2 Templating Language
    <http://jinja.pocoo.org/>`_.
    Please see the developer documentation on
    :ref:`Output Handling <dev_output_handling>`.

    """

    class Meta:

        """Handler meta-data."""

        interface = output.IOutput
        label = 'jinja2'

    def render(self, data_dict, **kw):
        """
        Take a data dictionary and render it using the given template file.

        Required Arguments:

        :param data_dict: The data dictionary to render.
        :keyword template: The path to the template, after the
         ``template_module`` or ``template_dirs`` prefix as defined in the
         application.
        :returns: str (the rendered template text)

        """
        template = kw.get('template', None)

        LOG.debug("rendering output using '%s' as a template." % template)
        content = self.load_template(template)
        env = Environment(keep_trailing_newline=True)
        tmpl = env.from_string(content.decode('utf-8'))
        return tmpl.render(**data_dict)


def load(app):
    app.handler.register(Jinja2OutputHandler)

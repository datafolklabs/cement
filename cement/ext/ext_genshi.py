"""
The Genshi Extension module provides output templating based on the
`Genshi Text Templating Language \
<http://genshi.edgewall.org/wiki/Documentation/text-templates.html>`_.


Requirements
------------

 * Genshi (``pip install genshi``)


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
            extensions = ['genshi']
            output_handler = 'genshi'
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
        app.render(data, 'my_template.genshi')


Note that the above ``template_module`` and ``template_dirs`` are the
auto-defined defaults but are added here for clarity.  From here, you
would then put a Genshi template file in
``myapp/templates/my_template.genshi`` or
``/usr/lib/myapp/templates/my_template.genshi``.

"""

from ..core import output
from ..utils.misc import minimal_logger
from genshi.template import NewTextTemplate

LOG = minimal_logger(__name__)


class GenshiOutputHandler(output.TemplateOutputHandler):

    """
    This class implements the :ref:`IOutput <cement.core.output>`
    interface.  It provides text output from template and uses the
    `Genshi Text Templating Language
    <http://genshi.edgewall.org/wiki/Documentation/text-templates.html>`_.
    Please see the developer documentation on
    :ref:`Output Handling <dev_output_handling>`.

    """

    class Meta:

        """Handler meta-data."""

        interface = output.IOutput
        label = 'genshi'

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
        tmpl = NewTextTemplate(content)
        return tmpl.generate(**data_dict).render()


def load(app):
    app.handler.register(GenshiOutputHandler)

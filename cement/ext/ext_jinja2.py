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

import sys
from ..core import output
from ..utils.misc import minimal_logger
from jinja2 import Environment, FileSystemLoader, PackageLoader

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

    def __init__(self, *args, **kw):
        super(Jinja2OutputHandler, self).__init__(*args, **kw)

        # expose Jinja2 Environment instance so that we can manipulate it
        # higher in application code if necessary
        self.env = Environment(keep_trailing_newline=True)

    def render(self, data_dict, template=None, **kw):
        """
        Take a data dictionary and render it using the given template file.
        Additional keyword arguments are ignored.

        Required Arguments:

        :param data_dict: The data dictionary to render.
        :keyword template: The path to the template, after the
         ``template_module`` or ``template_dirs`` prefix as defined in the
         application.
        :returns: str (the rendered template text)

        """

        LOG.debug("rendering output using '%s' as a template." % template)
        content, _type, path = self.load_template_with_location(template)

        if _type == 'directory':
            self.env.loader = FileSystemLoader(self.app._meta.template_dirs)
        elif _type == 'module':
            parts = self.app._meta.template_module.rsplit('.', 1)
            self.env.loader = PackageLoader(parts[0], package_path=parts[1])

        if sys.version_info[0] >= 3:
            if not isinstance(content, str):
                content = content.decode('utf-8')
        else:
            if not isinstance(content, unicode):     # pragma: nocover  # noqa
                content = content.decode('utf-8')    # pragma: nocover

        tmpl = self.env.from_string(content)

        return tmpl.render(**data_dict)


def load(app):
    app.handler.register(Jinja2OutputHandler)

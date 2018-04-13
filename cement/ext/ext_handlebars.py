"""
The Handlebars Extension provides output templating based on the
`Handlebars Templating Language <https://github.com/wbond/pybars3>`_.

Requirements
------------

 * pybars3 (``pip install pybars3``)


Configuration
-------------

Application Meta-data
^^^^^^^^^^^^^^^^^^^^^

This extension supports the following application meta-data via
``CementApp.Meta``:

 * **handlebars_helpers** - A dictionary of helper functions to register
   with the compiler. Will **override**
   ``HandlebarsOutputHandler.Meta.helpers``.
 * **handlebars_partials** - A list of partials (template file names) to
   search for, and pre-load before rendering templates.  Will **override**
   ``HandlebarsOutputHandler.Meta.partials``.


Template Directories
^^^^^^^^^^^^^^^^^^^^

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

    class MyApp(CementApp):
        class Meta:
            label = 'myapp'
            extensions = ['handlebars']
            output_handler = 'handlebars'
            template_module = 'myapp.templates'
            template_dirs = [
                '~/.myapp/templates',
                '/usr/lib/myapp/templates',
                ]
    # ...

Note that the above ``template_module`` and ``template_dirs`` are the
auto-defined defaults but are added here for clarity.  From here, you
would then put a Handlebars template file in
``myapp/templates/my_template.handlebars`` or
``/usr/lib/myapp/templates/my_template.handlebars`` and then render a data
dictionary with it:

.. code-block:: python

    app.render(some_data, 'my_template.handlebars')


Helpers
^^^^^^^

Custom helper functions can easily be registered with the compiler via
``CementApp.Meta.handlebars_helpers`` and/or
``HandlebarsOutputHandler.Meta.helpers``.

.. code-block:: python

    def my_custom_helper(this, arg1, arg2):
        # do something with arg1 and arg2
        if arg1 == arg2:
            return True
        else:
            return False


    class MyApp(CementApp):
        class Meta:
            label = 'myapp'
            extensions = ['handlebars']
            output_handler = 'handlebars'
            handlebars_helpers = {
                'myhelper' : my_custom_helper
            }
    # ...

You would then access this in your template as:

.. code-block:: console

    This is my template

    {{#if (myhelper this that)}}
    This will only appear if myhelper returns True
    {{/if}}


See the `Handlebars Documentation <https://github.com/wbond/pybars3>`_ for
more information on helpers.


Partials
^^^^^^^^

Though partials are supported by the library, there is no good way of
automatically loading them in the context and workflow of a typical Cement
application.  Therefore, the extension needs a list of partial
template names to know what to preload, in order to make partials work.
Future versions will hopefully automate this.

Example:

.. code-block:: python

    class MyApp(CementApp):
        class Meta:
            label = 'myapp'
            extensions = ['handlebars']
            output_handler = 'handlebars'
            handlebars_partials = [
                'header.bars',
                'footer.bars',
            ]

Where ``header.bars`` and ``footer.bars`` are template names that will be
searched for, and loaded just like other templates loaded from template dirs.
These are then referenced in templates as:

.. code-block:: console

    {{> "header.bars"}}
    This is my template
    {{> "footer.bars}}

See the `Handlebars Documentation <https://github.com/wbond/pybars3>`_ for
more information on partials.

"""

import sys
import pybars._compiler
from cement.core import output, handler
from cement.utils.misc import minimal_logger

# Monkey patch so we don't escape HTML (not clear how else to do this)
# See: https://github.com/wbond/pybars3/issues/25
original_prepare = pybars._compiler.prepare


def my_prepare(value, escape):
    return original_prepare(value, False)


pybars._compiler.prepare = my_prepare


from pybars import Compiler  # noqa


LOG = minimal_logger(__name__)


class HandlebarsOutputHandler(output.TemplateOutputHandler):

    """
    This class implements the :ref:`IOutput <cement.core.output>`
    interface.  It provides text output from template and uses the
    `Handlebars Templating Language <http://handlebarsjs.com/>`_ for Python
    via the ``pybars`` library.  Please see the developer documentation on
    :ref:`Output Handling <dev_output_handling>`.

    **Note** This extension has an external dependency on ``pybars3``.  You
    must include ``pybars3`` in your applications dependencies as Cement
    explicitly does **not** include external dependencies for optional
    extensions.
    """

    class Meta:

        """Handler meta-data."""

        interface = output.IOutput
        label = 'handlebars'

        #: Whether or not to include ``handlebars`` as an available to choice
        #: to override the ``output_handler`` via command line options.
        overridable = False

        #: Custom helpers
        helpers = {}

        #: List of partials to preload
        partials = []

    def __init__(self, *args, **kw):
        super(HandlebarsOutputHandler, self).__init__(*args, **kw)
        self._raw_partials = {}

    def _setup(self, app):
        super(HandlebarsOutputHandler, self)._setup(app)
        if hasattr(self.app._meta, 'handlebars_helpers'):
            self._meta.helpers = self.app._meta.handlebars_helpers
        if hasattr(self.app._meta, 'handlebars_partials'):
            self._meta.partials = self.app._meta.handlebars_partials
        for partial in self._meta.partials:
            self._raw_partials[partial] = self.load_template(partial)

    def _clean_content(self, content):
        if sys.version_info[0] >= 3:
            if not isinstance(content, str):
                content = content.decode('utf-8')
        else:
            if not isinstance(content, unicode):     # pragma: nocover  # noqa
                content = content.decode('utf-8')    # pragma: nocover
        return content

    def render_content(self, data, content):
        bars = Compiler()
        content = bars.compile(self._clean_content(content))

        # need to render partials
        partials = {}
        for key, val in self._raw_partials.items():
            partials[key] = bars.compile(self._clean_content(val))

        return content(data, helpers=self._meta.helpers, partials=partials)

    def render(self, data, template):
        """
        Take a data dictionary and render it using the given template file.

        Required Arguments:

        :param data: The data dictionary to render.
        :keyword template: The path to the template, after the
         ``template_module`` or ``template_dirs`` prefix as defined in the
         application.
        :returns: str (the rendered template text)

        """
        LOG.debug("rendering output using '%s' as a template." % template)
        res = self.render_content(data, self.load_template(template))
        return res


def load(app):
    handler.register(HandlebarsOutputHandler)

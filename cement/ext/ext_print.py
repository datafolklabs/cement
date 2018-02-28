"""

The Print Extension adds the :class:`PrintOutputHandler` and
:class:`PrintDictOutputHandler` to render
output in pure text.  It is mostly intended for development, but also supports
the additional ``app.print()`` extended function which can be used in place of
the standard ``print()`` so that apps can continue to utilitize features of the
framework consistently (such as honoring ``pre_render`` and ``post_render``
hooks, etc).

Requirements
------------

 * No external dependencies.


Configuration
-------------

This extension does not support any configuration settings.


Usage
_____


**myapp.py**

.. code-block:: python

    from cement import App


    class MyApp(App):
        class Meta:
            label = 'myapp'
            extensions = ['print']


    with MyApp() as app:
        app.run()

        ### will print the text using PrintOutputHandler (honors render hooks)

        app.print('This is an output message')


        ### using PrintOutputHandler directly (not likely, but for reference)

        data = {}
        data['out'] = 'This is an output message'
        app.render(data)


.. code-block:: console

    $ python myapp.py
    This is an output message


Alternatively, you can use the ``print_dict`` output handler that can be useful
in development as it simply just prints out a string representation of the data
dict.

**myapp.py**

.. code-block:: python

    from cement import App


    class MyApp(App):
        class Meta:
            label = 'myapp'
            extensions = ['print_dict']


    with MyApp() as app:
        app.run()

        data = {'foo' : 'bar'}
        app.render(data)


.. code-block:: console

    $ python myapp.py
    foo: bar

"""

from ..core import output
from ..utils.misc import minimal_logger

LOG = minimal_logger(__name__)


def extend_print(app):
    def _print(text):
        app.render({'out' : text}, handler='print')
    app.extend('print', _print)


class PrintOutputHandler(output.OutputHandler):

    """
    This class implements the :ref:`Output <cement.core.output>` Handler
    interface.  It takes a dict and only prints out the ``out`` key. It is
    primarily used by the ``app.print()`` extended function in order to replace
    ``print()`` so that framework features like ``pre_render`` and
    ``post_render`` hooks are honored. Please see the developer documentation
    on :cement:`Output Handling <dev/output>`.

    """
    class Meta:

        """Handler meta-data"""

        label = 'print'
        """The string identifier of this handler."""

        #: Whether or not to include ``json`` as an available choice
        #: to override the ``output_handler`` via command line options.
        overridable = False


    def render(self, data_dict, template=None, **kw):
        """
        Take a data dictionary and render only the ``out`` key as text output.
        Note that the template option is received here per the interface,
        however this handler just ignores it.

        Args:
            data_dict (dict): The data dictionary to render.

        Keyword Args:
            template: This option is completely ignored.

        Returns:
            str: A text string.

        """
        if 'out' in data_dict.keys():
            LOG.debug("rendering output as text via %s" % self.__module__)
            return data_dict['out'] + '\n'
        else:
            LOG.debug("no 'out' key found in data dict. not rendering output via %s" % self.__module__)
            return None


class PrintDictOutputHandler(output.OutputHandler):

    """
    This class implements the :ref:`Output <cement.core.output>` Handler
    interface.  It is intended primarily for development where printing out a
    string reprisentation of the data dictionary would be useful.  Please see
    the developer documentation on :cement:`Output Handling <dev/output>`.

    """
    class Meta:

        """Handler meta-data"""

        label = 'print_dict'
        """The string identifier of this handler."""

        #: Whether or not to include ``json`` as an available choice
        #: to override the ``output_handler`` via command line options.
        overridable = False


    def render(self, data_dict, template=None, **kw):
        """
        Take a data dictionary and render it as text output.  Note that the
        template option is received here per the interface, however this
        handler just ignores it.

        Args:
            data_dict (dict): The data dictionary to render.

        Keyword Args:
            template: This option is completely ignored.

        Returns:
            str: A text string.

        """
        LOG.debug("rendering output as text via %s" % self.__module__)
        out = ''
        for key,val in data_dict.items():
            out = out + '%s: %s\n' % (key, val)

        return out


def load(app):
    app.handler.register(PrintDictOutputHandler)
    app.handler.register(PrintOutputHandler)
    app.hook.register('pre_argument_parsing', extend_print)

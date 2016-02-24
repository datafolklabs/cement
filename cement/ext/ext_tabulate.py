"""
The Tabulate Extension provides output handling based on the
`Tabulate <https://pypi.python.org/pypi/tabulate>`_ library.  It's format is
familiar to users of MySQL, Postgres, etc.

Requirements
------------

 * Tabulate (``pip install tabulate``)


Configuration
-------------

This extension does not support any configuration settings.


Usage
-----

.. code-block:: python

    from cement.core import foundation

    class MyApp(foundation.CementApp):
        class Meta:
            label = 'myapp'
            extensions = ['tabulate']
            output_handler = 'tabulate'

    with MyApp() as app:
        app.run()

        # create a dataset
        headers = ['NAME', 'AGE', 'ADDRESS']
        data = [
            ["Krystin Bartoletti", 47, "PSC 7591, Box 425, APO AP 68379"],
            ["Cris Hegan", 54, "322 Reubin Islands, Leylabury, NC 34388"],
            ["George Champlin", 25, "Unit 6559, Box 124, DPO AA 25518"],
            ]

        app.render(data, headers=headers)


Looks like:

.. code-block:: console

    | NAME               | AGE | ADDRESS                                 |
    |--------------------+-----+-----------------------------------------|
    | Krystin Bartoletti |  47 | PSC 7591, Box 425, APO AP 68379         |
    | Cris Hegan         |  54 | 322 Reubin Islands, Leylabury, NC 34388 |
    | George Champlin    |  25 | Unit 6559, Box 124, DPO AA 25518        |

"""

import sys
from tabulate import tabulate
from ..core import output, exc
from ..utils.misc import minimal_logger

LOG = minimal_logger(__name__)


class TabulateOutputHandler(output.CementOutputHandler):

    """
    This class implements the :ref:`IOutput <cement.core.output>`
    interface.  It provides tabularized text output using the
    `Tabulate <https://pypi.python.org/pypi/tabulate>`_ module.  Please
    see the developer documentation on
    :ref:`Output Handling <dev_output_handling>`.

    **Note** This extension has an external dependency on ``tabulate``.  You
    must include ``tabulate`` in your applications dependencies as Cement
    explicitly does **not** include external dependencies for optional
    extensions.
    """

    class Meta:

        """Handler meta-data."""

        interface = output.IOutput
        label = 'tabulate'

        #: Whether or not to pad the output with an extra pre/post '\n'
        padding = True

        #: Default template format.  See the ``tabulate`` documentation for
        #: all supported template formats.
        format = 'orgtbl'

        #: Default headers to use.
        headers = []

        #: Default alignment for string columns.  See the ``tabulate``
        #: documentation for all supported ``stralign`` options.
        string_alignment = 'left'

        #: Default alignment for numeric columns.  See the ``tabulate``
        #: documentation for all supported ``numalign`` options.
        numeric_alignment = 'decimal'

        #: String format to use for float values.
        float_format = 'g'

        #: Default replacement for missing value.
        missing_value = ''

        #: Whether or not to include ``tabulate`` as an available to choice
        #: to override the ``output_handler`` via command line options.
        overridable = False

    def render(self, data, **kw):
        """
        Take a data dictionary and render it into a table.  Additional
        keyword arguments are passed directly to ``tabulate.tabulate``.


        Required Arguments:

        :param data_dict: The data dictionary to render.
        :returns: str (the rendered template text)

        """
        headers = kw.get('headers', self._meta.headers)

        out = tabulate(data, headers,
                       tablefmt=kw.get('tablefmt', self._meta.format),
                       stralign=kw.get(
                           'stralign', self._meta.string_alignment),
                       numalign=kw.get(
                           'numalign', self._meta.numeric_alignment),
                       missingval=kw.get(
                           'missingval', self._meta.missing_value),
                       floatfmt=kw.get('floatfmt', self._meta.float_format),
                       )
        out = out + '\n'

        if self._meta.padding is True:
            out = '\n' + out + '\n'

        return out


def load(app):
    app.handler.register(TabulateOutputHandler)

.. _dev_output_handling:

Output Handling
===============

Cement defines an output interface called :class:`cement.core.output.IOutput`,
as well as the default :class:`cement.ext.ext_dummy.DummyOutputHandler`
that implements the interface.  This handler is part of Cement, and actually
does nothing to produce output.  Therefore it can be said that by default
a Cement application does not handle rendering output to the console, but
can if another output handler be used.

Please note that there may be other handler's that implement the ``IOutput``
interface.  The documentation below only references usage based on the
interface and not the full capabilities of the implementation.

The following output handlers are included and maintained with Cement:

    * :class:`cement.ext.ext_dummy.DummyOutputHandler`
    * :class:`cement.ext.ext_json.JsonOutputHandler`
    * :class:`cement.ext.ext_yaml.YamlOutputHandler`
    * :class:`cement.ext.ext_genshi.GenshiOutputHandler`
    * :class:`cement.ext.ext_handlebars.HandlebarsOutputHandler`
    * :class:`cement.ext.ext_jinja2.Jinja2OutputHandler`
    * :class:`cement.ext.ext_mustache.MustacheOutputHandler`
    * :class:`cement.ext.ext_tabulate.TabulateOutputHandler`


Please reference the :class:`cement.core.output.IOutput` interface
documentation for writing your own output handler.

Rending Output
--------------

Cement applications do not need to use an output handler by any means.  Most
small applications can get away with simple ``print()`` statements.  However,
anyone who has ever built a bigger application that produces a lot of output
will know that this can get ugly very quickly in your code.

Using an output handler allows the developer to keep their logic clean, and
offload the display of relevant data to an output handler, possibly by
templates or other means (GUI?).

An output handler has a ``render()`` function that takes a data dictionary
to produce output.  Some output handlers may also accept a ``template``
or other parameters that define how output is rendered.  This is easily
accessible by the application object.

.. code-block:: python

    from cement.core import foundation, output

    # Create the application
    app = foundation.CementApp('myapp')

    # Setup the application
    app.setup()

    # Run the application
    app.run()

    # Add application logic
    data = dict(foo='bar')
    app.render(data)

    # Close the application
    app.close()


The above example uses the default output handler, therefore nothing is
displayed on screen.  That said, if we write our own quickly we can see
something happen:

.. code-block:: python

    from cement.core import foundation, handler, output

    # Create a custom output handler
    class MyOutput(output.CementOutputHandler):
        class Meta:
            label = 'myoutput'

        def render(self, data):
            for key in data:
                print "%s => %s" % (key, data[key])

    app = foundation.CementApp('myapp', output_handler=MyOutputHandler)
    ...

Which looks like:

.. code-block:: text

    $ python test.py
    foo => bar


Rendering Output Via Templates
------------------------------

An extremely powerful feature of Cement is the ability to offload console
output to a template output handler.  Several are inluded with Cement but not
enabled by default (listed above).  The following example shows the use of
the Mustache templating langugage, as well as Json output handling.

**myapp.py**

.. code-block:: python

    from cement.core.foundation import CementApp
    from cement.core.controller import CementBaseController, expose


    class MyBaseController(CementBaseController):
        class Meta:
            label = 'base'
            description = 'MyApp Does Amazing Things'

        @expose(hide=True)
        def default(self):
            data = dict(foo='bar')
            self.app.render(data, 'default.m')

            # always return the data, some output handlers require this
            # such as Json/Yaml (which don't use templates)
            return data


    class MyApp(CementApp):
        class Meta:
            label = 'myapp'
            base_controller = MyBaseController
            extensions = ['mustache', 'json']

            # default output handler
            output_handler = 'mustache'


    with MyApp() as app:
        app.run()


**/usr/lib/myapp/templates/default.m**

.. code-block:: text

    This is the output of the MyBaseController.default() command.

    The value of the 'foo' variable is => '{{foo}}'


And this looks like:

.. code-block:: text

    $ python myapp.py

    This is the output of the MyBaseController.default() command.

    The value of the 'foo' variable is => 'bar'


Optionally, we can use the ``JsonOutputHandler`` via ``-o json`` to trigger
just Json output (supressing all other output) using our return dictionary:

.. code-block:: text

    $ python myapp.py -o json
    {"foo": "bar"}

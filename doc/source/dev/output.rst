Output Handling
===============

Cement defines an output interface called :ref:`IOutput <cement2.core.output>`, 
as well as the default :ref:`NullOutputHandler <cement2.ext.ext_nulloutput>` 
that implements the interface.  This handler is part of Cement, and actually 
does nothing to produce output.  Therefore it can be said that by default
a Cement application does not handle rendering output to the console, but 
can should another output handler be used.

Please note that there may be other handler's that implement the IOutput
interface.  The documentation below only references usage based on the 
interface and not the full capabilities of the implementation.

The following output handlers are included and maintained with Cement2:

    * :ref:`NullOutputHandler <cement2.ext.ext_nulloutput>`
    * :ref:`JsonOutputHandler <cement2.ext.ext_json>`
    * :ref:`YamlOutputHandler <cement2.ext.ext_yaml>`

Please reference the :ref:`IOutput <cement2.core.output>` interface 
documentation for writing your own output handler.

Rending Output
--------------

Cement application do not need to use an output handler by any means.  Most
small applications can get away with print() statements.  However, anyone
who has ever built a bigger application that produces a lot of output will 
know that this can get ugly very quickly in your code.   

Using an output handler allows the developer to keep their logic clean, and 
offload the display of relevant data to an output handler, possibly by 
templates or other means (GUI?).

An output handler has a 'render()' function that takes a data dictionary that
it uses to produce output.  Some output handler may also accept a 'template' 
or other parameters that define how output is rendered.  This is easily 
accessible by the application object.

.. code-block:: python

    from cement2.core import foundation, output

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

    from cement2.core import foundation, handler, output

    # Create a custom output handler
    class MyOutput(object):
        class Meta:
            interface = output.IOutput
            label = 'myoutput'

        def __init__(self):
            self.config = None

        def setup(self, config_obj):
            self.config = config_obj

        def render(self, data, template=None):
            for key in data:
                print "%s => %s" % (key, data[key])

    app = foundation.CementApp('myapp', output_handler=MyOutputHandler)

Which looks like:

.. code-block:: text

    $ python test.py
    foo => bar

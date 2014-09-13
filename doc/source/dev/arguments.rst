Argument and Option Handling
============================

Cement defines an argument interface called
:ref:`IArgument <cement.core.arg>`, as well as the default
:ref:`ArgParseArgumentHandler <cement.ext.ext_argparse>` that implements the
interface.  This handler is built on top of the
`ArgParse <http://docs.python.org/library/argparse.html>`_ module which is
included in the Python standard library.

Please note that there may be other handler's that implement the ``IArgument``
interface.  The documentation below only references usage based on the
interface and not the full capabilities of the implementation.

The following argument handlers are included and maintained with Cement:

    * :ref:`ArgParseArgumentHandler <cement.ext.ext_argparse>`


Please reference the :ref:`IArgument <cement.core.arg>` interface
documentation for writing your own argument handler.

Adding Arguments
----------------

The ``IArgument`` interface is loosely based on ``ArgParse`` directly.  That
said, it only defines a minimal set of params that must be honored by the
handler implementation, even though the handler itself may except more than
that.  The following shows some basic examples of adding
arguments based on the interface (meaning, these examples should work
regardless of what the handler is):

.. code-block:: python

    from cement.core import foundation

    # create the application
    app = foundation.CementApp('myapp')

    # then setup the application... which will use our 'mylog' handler
    app.setup()

    # add any arguments after setup(), and before run()
    app.args.add_argument('-f', '--foo', action='store', dest='foo',
                          help='the notorious foo option')
    app.args.add_argument('-V', action='store_true', dest='vendetta',
                          help='v for vendetta')
    app.args.add_argument('-A', action='store_const', const=12345,
                          help='the big a option')

    # then run the application
    app.run()

    # access the parsed args from the app.pargs shortcut
    if app.pargs.foo:
        print "Received foo option with value %s" % app.pargs.foo
    if app.pargs.vendetta:
        print "Received V for Vendetta!"
    if app.pargs.A:
        print "Received the A option with value %s" % app.pargs.A

    # close the application
    app.close()


Here we have setup a basic application, and then add a few arguments to the
parser.

.. code-block:: text

    $ python test.py --help
    usage: test.py [-h] [--debug] [--quiet] [-f FOO] [-V] [-A]

    optional arguments:
      -h, --help         show this help message and exit
      --debug            toggle debug output
      --quiet            suppress all output
      -f FOO, --foo FOO  the notorious foo option
      -V                 v for vendetta
      -A                 the big a option

    $ python test.py --foo=bar
    Received foo option with value bar

    $ python test.py -V
    Received V for Vendetta!


Accessing Parsed Arguments
--------------------------

The ``IArgument`` interface defines that the ``parse()`` function return any
type of object that stores the name of the argument as a class member.
Meaning, when adding the ``foo`` option with ``action='store'`` and the value
is stored as the ``foo`` destination... that would be accessible as
``app.pargs.foo``.  In the case of the ``ArgParseArgumentHandler`` the return
object is exactly what you would expect by calling ``parser.parse_args()``,
but may be different with other argument handler implementations.

The parsed arguments are actually stored as ``app._parsed_args``, but are
exposed as ``app.pargs``.  Accessing ``app.pargs`` can be seen in the examples
above.



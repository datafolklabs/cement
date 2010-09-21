Command Line Options and Arguments
==================================

Cement fully configures command line option and argument parsing via the
`OptionParser <http://docs.python.org/library/optparse.html>`_ library.  The following outlines how to create options, and 
access the options and arguments passed to your application.

Adding Options To a Namespace
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Typically, options are added directly to a namespace when that namespace is 
registered.  The following comes from the example plugin:

**helloworld/bootstrap/example.py**

.. code-block:: python

    from cement.core.namespace import CementNamespace, register_namespace

    example = CementNamespace(
        label='example', 
        controller='ExampleController',
        description='Example Plugin for helloworld',
        required_api='0.7-0.8:20100210',
        provider='helloworld'
        )

    example.config['foo'] = 'bar'

    example.options.add_option('-F', '--foo', action='store',
        dest='foo', default=None, help='Example Foo Option'
        )

    register_namespace(example)


The option added above shows up under the example namespace like so:

.. code-block:: text

    $ helloworld example --help
    Usage:   helloworld example <SUBCOMMAND> [ARGS] --(OPTIONS)

    Sub-Commands:  
        ex2, ex1

    Help?  try '[SUBCOMMAND]-help'

    Options:
        --version          show program's version number and exit
        -h, --help         show this help message and exit
        -F FOO, --foo=FOO  Example Foo Option
        -R, --root-option  Example root option
        --json             render output as json (CLI-API)
        --debug            toggle debug output
        --quiet            disable console logging
        --yaml             render output as yaml
    

The '-F/--foo' option does *not* show up under the root namespace 
(helloworld --help).  In most cases, an option also aligns with a config 
option as you can see in the example above.  When the '--foo' option is passed, 
if the config['foo'] option exists, it will override the value with that of 
the value passed at the command line.

You will also notice in the above that all of our root options also show up
under our 'example' namespace.  This is configurable by the 
'merge_root_options' plugin configuration option.  Take the following example:

.. code-block:: python

    from cement.core.namespace import CementNamespace, register_namespace

    example = CementNamespace(
                label='example', 
                controller='ExampleController',
                description='Example Plugin for helloworld',
                required_api='0.7-0.8:20100210',
                provider='helloworld'
                )

    example.config['foo'] = 'bar'
    example.config['merge_root_options'] = False

    example.options.add_option('-F', '--foo', action='store',
        dest='foo', default=None, help='Example Foo Option'
        )

    register_namespace(example)


And the output:

.. code-block:: text

    $ helloworld example --help
    Usage:   helloworld example <SUBCOMMAND> [ARGS] --(OPTIONS)

    Sub-Commands:  
        ex2, ex1

    Help?  try '[SUBCOMMAND]-help'

    Options:
        --version          show program's version number and exit
        -h, --help         show this help message and exit
        -F FOO, --foo=FOO  Example Foo Option
    
If 'merge_root_options' is set to False, only the options added to this 
namespace directly will be configured.


Adding Options To Another Namespace
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Options can be added *to* any namespace *from* any namespace bootstrap by way
of the built in 'options_hook'.  For example, you will see something like the 
following in your applications root bootstrap:

**helloworld/bootstrap/root.py**

.. code-block:: python

    from cement.core.opt import init_parser
    from cement.core.hook import register_hook

    # Register root options
    @register_hook()
    def options_hook(*args, **kwargs):
        # This hook allows us to append options to the root namespace
        root_options = init_parser()
        root_options.add_option('-R', '--root-option', action ='store_true', 
            dest='root_option', default=None, help='Example root option') 
        root_options.add_option('--json', action='store_true',
            dest='enable_json', default=None, 
            help='render output as json (CLI-API)')
        root_options.add_option('--debug', action='store_true',
            dest='debug', default=None, help='toggle debug output')
        root_options.add_option('--quiet', action='store_true',
            dest='quiet', default=None, help='disable console logging')
        return ('root', root_options)
    
    
The 'options_hook' expects a tuple in return when it runs that hook, and the
tuple is made up of (namespace_name, optparse_object).  Code similar to the
above can also be used to inject options into any other namespace allowing 
plugins to build off of, and add functionality to other plugins or other
built in namespaces in your application.


Accessing Options and Arguments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All options and arguments passed at command line are accessible via the 
attributes 'self.cli_opts' and 'self.cli_args' from within every 
CementController.  For example:

**helloworld/controllers/example.py**

.. code-block:: python

    class ExampleController(CementController):
        @expose(namespace='root')
        def cmd2(self):
            print "args[1] => ", self.cli_args[1]
            print "root_option => ", self.cli_opts.root_option
            return dict()
        
The output is:
        
.. code-block:: text

    $ helloworld cmd2 --root-option arg1 arg2
    args[1] =>  bar
    root_option =>  True


Alternate Option Examples
^^^^^^^^^^^^^^^^^^^^^^^^^

All options are standard OptParse options, however the following are some 
examples.

.. code-block:: python

    example.options.add_option('--prompt', action='store_true', dest='prompt',
        help='toggle prompting')

The above sets namespaces['example'].config['prompt'] to True, as well as 
self.cli_opts.prompt.  The action is can be either 'store' or 'store_true' 
which means store the value passed with the option, or just store the option
as True.  dest is the variable name that the option value is stored as.  help
is what is displayed in --help.


.. code-block:: python

    example.options.add_option('-F', '--foo', action='store', dest='foo',
        help='pass value to foo', metavar='STR')
        
The above sets namespaces['example'].config['foot'] to the value passed at
command line (helloworld --foo=bar), and also sets self.cli_opts.foo the same.
metavar is an extra option that alters the display in --help (-F STR, --foo=STR).



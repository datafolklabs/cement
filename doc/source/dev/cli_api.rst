Cement CLI-API (Rendered JSON Output)
=====================================

Every Cement Application has a built in CLI-API that allows other programs,
regardless of their language, to access your command line interface and get
back Json output.  This is extremely powerful in mixed environments where you
might not have control over legacy applications, or other departments code.
If the language can speak Json, they can make a system call to your program
and not have to parse through unreliable STDOUT to get the information they
need.

The the following for example:

**./helloworld/controllers/example.py**:

.. code-block:: python

    @expose('helloworld.templates.example.ex2', namespace='root')    
    @register_hook()
    def ex2(self, cli_opts, cli_args): 
        example = ExampleModel()
        example.label = 'This is my Example Model'

        if cli_opts.my_option:
            print '%s passed by --my-option' % cli_opts.my_option

        return dict(foo=True, example=example, items=['one', 'two', 'three'])
    
    
The following would be run by:

.. code-block:: text

    $ helloworld ex2 --my-option        
    loading example plugin
    loading clibasic plugin
    True passed by --my-option
    
    There are a number of things you can do such as conditional statements:

    Label: This is my Example Model

    Or a for loop:

      * one
      * two
      * three

    And functions:

      Hello, World!
      Hello, Edward!

You can see that, we passed the '--my-option' that triggerd a print statement.
Then our return dictionary was rendered via Genshi.  Now lets see what that
looks like with our Json engine:

.. code-block:: text

    $ helloworld ex2 --my-option --json
    {"items": ["one", "two", "three"], "foo": true, "example": {"label": "This is my Example Model"}, "stderr": "", "stdout": "True passed by --my-option\n"}
    
The return data is rendered as Json, as well as STDOUT and STDERR.  All other
output is suppressed, meaning the application calling this will get back just
the Json, a standard format from which they can use the data more reliably and
much more easily.
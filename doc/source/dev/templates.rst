Genshi Templating Engine
========================

Cement applications use a Model, View, Controller design.  By separating the
view, or in this case what is printed to STDOUT, you can significantly clean
up your controller code.  Cement configures new applications to use the 
Genshi text templating language by default.  This is configured in your
applications 'core.config' module via the setting 'output_handler'.  Note
that for developers not interested in having output rendered from template
or any other kind of output rendering... this setting can be set to None.

A sample controller that exports its data to a Genshi template:

**./helloworld/controllers/example.py**:

.. code-block:: python

    from helloworld.model.example import ExampleModel
    
    @expose('helloworld.templates.example.ex2', namespace='root')    
    def ex2(self, cli_opts, cli_args): 
        example = ExampleModel()
        example.label = 'This is my Example Model'

        if cli_opts.my_option:
            print '%s passed by --my-option' % cli_opts.root_option

        return dict(foo=True, example=example, items=['one', 'two', 'three'])
        
It should be noted that the output_handler is implied in the above code, and
tells Cement to use the default that is configured in your apps core.config
module under 'output_handler'.  To specify an alternate handler, you can do
the following:

.. code-block:: python

    @expose('jinja2:helloworld.templates.example.ex2', namespace='root') 
    ...
    
Where 'jinja2' is the alternate output_handler to use for that command only,
assuming that a plugin is installed that provides an output_handler called
'jinja2'.

The template looks like:

**./helloworld/templates/example/ex2.txt**:

.. code-block:: text

    {# This is an example Genshi Text Template.  Documentation is available    #}\
    {# at:                                                                     #}\
    {#                                                                         #}\
    {#    http://genshi.edgewall.org/wiki/Documentation/text-templates.html    #}\
    {#                                                                         #}\
    \
    \
    {# --------------------- 78 character baseline --------------------------- #}\

    There are a number of things you can do such as conditional statements:

    {% if foo %}\
    Label: ${example.label}
    {% end %}\

    Or a for loop:

    {% for item in items %}\
      * ${item}
    {% end %}\


    And functions:

    {% def greeting(name) %}\
      Hello, ${name}!
    {% end %}\
    ${greeting('World')}\
    ${greeting('Edward')}
    

Admittedly, the syntax is a bit cumbersome.  But once you get the hang of it
there is a lot you can do with it, and your controller code looks so much 
better.  When rendered, this looks like:

.. code-block:: text

    $ helloworld ex2                     
    loading example plugin
    loading clibasic plugin

    There are a number of things you can do such as conditional statements:

    Label: This is my Example Model

    Or a for loop:

      * one
      * two
      * three

    And functions:

      Hello, World!
      Hello, Edward!


For simple methods that don't print much data or maybe don't print at all, you 
can simply skip the templating engine.  The same method without rendering would
be:

.. code-block:: python

    from helloworld.model.example import ExampleModel
    
    @expose(namespace='root')    
    def ex2(self, cli_opts, cli_args): 
        example = ExampleModel()
        example.label = 'This is my Example Model'

        if cli_opts.my_option:
            print '%s passed by --my-option' % cli_opts.root_option

        return dict(foo=True, example=example, items=['one', 'two', 'three'])

Now, nothing is rendered by Genshi and no output will be printed to the 
console unless you print it out yourself.  That said, because we are still
returning our dictionary, we can still use our '--json' and output Json via
the CLI-API.

Genshi Syntax Basics
--------------------

As noted in the example template, documentation on Genshi Text Templating can
be found at:

    http://genshi.edgewall.org/wiki/Documentation/text-templates.html
    
**Printing Variables**

.. code-block:: text

    Hello ${user_name}

Where 'user_name' is a variable returned from the controller.  Will display:

.. code-block:: text

    Hello Johnny
    

**if statements**

.. code-block:: text
    
    {% if foo %}\
    Label: ${example.label}
    {% end %}\

Will only output 'Label: <label>' if foo == True.


**for loops**

.. code-block:: text

    {% for item in items %}\
      - ${item}
    {% end %}\

Where 'items' is a list returned from the controller.  Will display:

.. code-block:: text

    - list item 1
    - list item 2
    - list item 3
    
**Functions**

.. code-block:: text

    {% def greeting(name) %}\
      Hello, ${name}!
    {% end %}\
    ${greeting('World')}\
    ${greeting('Edward')}


Will output:

.. code-block:: text

    Hello, World!
    Hello, Edward!
    
    
**Formatted Columns**

The following example comes from the 'list-plugins' controller command in the
clibasic plugin of The Rosendale Project:

.. code-block:: text

    {# --------------------- 78 character baseline --------------------------- #}\

    plugin              ver       description
    ==================  ========  ================================================
    {% for plugin in plugins %}\
    ${"%-18s" % plugin.label}  ${"%-8s" % plugin.version}  ${"%-48s" % plugin.description}
    {% end %}


Output looks like:

.. code-block:: text

    $ helloworld list-plugins
    loading example plugin
    loading clibasic plugin

    plugin              ver       description
    ==================  ========  ================================================
    example             0.1       Example plugin for helloworld                   
    clibasic            0.5r2     Basic CLI Commands for Cement Applications   



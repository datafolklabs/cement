Genshi Templating Language
==========================

The Genshi Framework Extension enables applications built on Cement to render
console output from text templates.

Configuration
-------------

By default, templates are search for in the '<app_label>.templates' python
module.  To override this, you can subclass and pass to CementApp().

.. code-block:: python
    
    from cement2.core import foundation, backend
    from cement2.lib.ext_genshi import GenshiOutputHandler
    
    class MyOutputHandler(GenshiOutputHandler):
        class Meta:
            label = 'my_output_handler'
            template_module = 'myapp.cli.templates'
            
    app = foundation.CementApp('myapp', output_handler=MyOutputHandler)
    

Example Usage
-------------

The following is an example application within a python package.

*myapp/appmain.py*

.. code-block:: python

    from cement2.core import foundation, controller, handler, backend

    # define application controllers
    class MyAppBaseController(controller.CementBaseController):
        class Meta:
            label = 'base'
            description = "My Application Does Amazing Things"
            arguments = []

        @controller.expose(help="base controller default command", hide=True)
        def default(self):
            data = dict(
                controller='base',
                command='default',
                )
            print self.render(data, 'default.txt')

    # define the application
    class MyApp(foundation.CementApp):
        class Meta:
            label = 'myapp'
            output_handler = 'genshi'
            extensions = ['genshi']
            base_controller = MyAppBaseController
            
    try:
        app = MyApp()
        app.setup()
        app.run()
    finally:
        app.close()
    

*myapp/templates/default.txt*

.. code-block:: text

    Inside the ${controller}.${command} function!
    

And the output:

>>> from myapp import appmain
Inside the base.default function!


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



API Reference
-------------

.. _cement2.ext.ext_genshi:

:mod:`cement2.ext.ext_genshi`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: cement2.ext.ext_genshi
    :members:
    
.. _cement2.lib.ext_genshi:

:mod:`cement2.lib.ext_genshi`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: cement2.lib.ext_genshi
    :members:
    



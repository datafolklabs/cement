Genshi Templating Language
==========================

The Genshi Framework Extension enables applications built on Cement to render
console output from text templates.

Configuration
-------------

The genshi extension is configurable with the following config settings under
the [genshi] section.

    template_module   
        The template module to look for template files in.  
        Default: <app_name>.templates
        

The configurations can be passed as defaults:

.. code-block:: python
    
    from cement2.core import foundation, backend
    
    defaults = backend.defaults('myapp')
    defaults['genshi'] = dict(
        template_module='myapp.cli.templates'
        )
    
    app = foundation.lay_cement('myapp', defaults=defaults)
    

Additionally, an application configuration file might have a section like the
following:

.. code-block:: text

    [genshi]
    template_module = myapp.templates

        
Example Usage
-------------

The following is an example application within a python package.

*myapp/appmain.py*

.. code-block:: python

    from cement2.core import foundation, controller, handler, backend

    # create the application
    defaults = backend.defaults('myapp')
    defaults['base']['extensions'].append('genshi')
    defaults['base']['output_handler'] = 'genshi'
    app = foundation.lay_cement('myapp', defaults=defaults)

    # define application controllers
    class MyAppBaseController(controller.CementBaseController):
        class Meta:
            label = 'base'
            interface = controller.IController
            description = "My Application Does Amazing Things"
            defaults = dict()
            arguments = []

        @controller.expose(help="base controller default command", hide=True)
        def default(self):
            data = dict(
                controller='base',
                command='default'
                )
        
            print self.render(data, 'default.txt')
      
    # register the controllers
    handler.register(MyAppBaseController)        

    # setup the application
    app.setup()

    try:
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
    



Handlers
========

Cement sets up and provides a handlers object that is used to make pieces
of the framework (and your application) both pluggable, and customizable.
Currently this is a new feature, and only 'output' handling has been ported
to the handler system.  That said, it is a perfect example of how it is used.
At application bootstrap, Cement defines the 'output' handler type, and then
registers the default output handlers to that type (genshi, and json).  As you
can see, this is useful in that functions will return data to a genshi
template, but if the '--json' option is passed it is rendered as Json.  
Additionally, developers can add additional handlers via plugins such as the 
Rosendale YAML Plugin which adds an output handler called 'yaml', and is called 
when the user passes '--yaml'.  

Generally, a handler is a Class or Function of some kind, and provides some
functionality in more or less a 'standardized' way.  Meaning, all handlers
of type 'output' should function the same way.  It is a very loose, but 
versatile method of configuring and using handlers.  How a handler functions 
is up to the developer, and should be documented well.  It is recommended that
a base 'Handler' class be constructed, and documented so that other developers
know what is expected of that Handler (and so they can sub-class from it).


Defining a Handler
------------------

By default, as of 0.8.9, the only default handler type is called 'output'
and can be accessed as the following (from within a loaded cement app):

.. code-block:: python

    from cement import handlers
    handlers['output']
    

Handlers should be defined within you bootstrap process, generally in the 
root bootstrap.  To define a handler type, add something similar to the 
following:

**helloworld/bootstrap/root.py**

.. code-block:: python

    from cement.core.handler import define_handler
    define_handler('my_handler')


Registering a Handler
---------------------

Handlers should also be registered during the bootstrap process.  The 
following is an example from rosendale.yaml and shows how to register
an output handler (keep in mind this is only a snippit of the code in that
file):

**rosendale.bootstrap.yaml_output**

.. code-block:: python
    
    from rosendale.lib.yaml_output import render_yaml_output
    register_handler('output', 'yaml', render_yaml_output)
    
In this example, the first argument (output) is the handler type, the second 
(yaml) is the label/name of the output handler you are registering, and finally
the last argument is the function or class object to store as the handler.  
**Note**: Do not pass an instantiated function or object, meaning pass 'AClass'
and not 'AClass()'.


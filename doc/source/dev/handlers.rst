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
Developers can add additional handlers via plugins such as the 
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
    

Handlers should be defined within your bootstrap process, generally in the 
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

**Note**: The handler can be store as an instantiated function/class or not. 
This all depends on how the handler is to be used.  For example, you might want
to use handlers to create a stateful object (instantated once) or not 
(instantiated every time it is called).  The 'output' handler is an example
of a handler that is not instantiated, because it is only a function that 
relies on different arguments everytime it is called.  However, a database
handler might only be instantiated once (same database, same info, same args)

Example Usage
-------------

How a handler is accessed depends on how the handler is defined.  Does it 
expect arguments?  Does it return data?  This is all for the developer of the
application to determine, and document.  As an example, lets say we have a
database handler.  We want to use handlers to setup and provide access to
two different databases.  One for read operations, and one for write
operations.  Please note, this is a psuedo example and will not have any real
database interaction.  

helloworld/core/database.py

.. code-block:: python

    class Database(object):
        def __init__(self, uri):
            self.uri = uri
        
        def connect(self):
            # do something and establish a connection
            raise NotImplementedError, "Database.connect() must be subclassed."
        
        def query(self, query_string):
            # do something and return query_results
            raise NotImplementedError, "Database.query() must be subclassed."            
        

helloworld/lib/database/mysql.py

.. code-block:: python

    from helloworld.core.database import Database
    
    class MySQLDatabase(Database)
        def connect(self):
            # do something to connect to self.uri
            pass
        
        def query(self, query_string):
            # do something with query_string
            return query_results
            

helloworld/bootstrap/root.py

.. code-block:: python

    from cement.core.handler import define_handler
    from helloworld.lib.database.mysql import MySQLDatabase
    
    define_handler('database')
    
    # setup a persistant database object, one for read one for write
    read_db = MySQLDatabase('some_db_uri')
    write_db = MySQLDatabase('some_other_db_uri')
    register_handler('database', 'read_db', read_db)
    register_handler('database', 'write_db', write_db)
    
    
helloworld/controller/root.py

.. code-block:: python

    from cement.core.handler import get_handler
    
    class RootController(CementController):
        def query_database(self)
            # read from the readonly database server
            db = get_handler('database', 'read_db')
            res = db.query('some SQL query')
            # do something with res
        
        def update_something(self):
            # do some operation on the write database server
            db = get_handler('database', 'write_db')
            db.query('some query to update something')

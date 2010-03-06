Understanding Your Application
==============================

Your application is broken up into specific directories, each with their own
purpose.  Using our helloworld example we have the following modules and
directories:

    * helloworld.core
    * helloworld.bootstrap
    * helloworld.controllers
    * helloworld.model
    * helloworld.templates
    * helloworld.helpers
    
We are going to briefly explain each, and go into more detail later in the 
documentation.


helloworld.core
---------------

This module is the 'core' of your application and is the first phase of the
application runtime where the Cement Framework is initialized.  By default this 
includes the appmain.py and config.py files.  Both of which can be modified, 
but you don't need to.  The core module should be used for any code that sets 
up the base of your application, or provides libraries and functions that are 
not tied to any commands (commands are created in the controllers module).  An 
example of a library that might go into the core module would be code that sets 
up an xmlrpclib proxy object to talk to a remote server.  Most likely you want 
all controllers to access the same proxy object once it is setup.  

It should be noted that plugins should not create files/libraries in this
namespace.


helloworld.bootstrap
--------------------

The bootstrap modules is the second phase of the application runtime and is 
used to initialize parts of the application that are required before and 
controllers or code is loaded.  Typical uses of the bootstrap module are for:

    * Creating namespaces
    * Defining and registering hooks

The helloworld/bootstrap/root.py is the only bootstrap called by the Cement
Framework, however the 'root' namespace is already setup by Cement and does
not get created in this bootstrap.  That said, and additional bootstrap files
need to be imported into the root bootstrap.  For example, if you are creating
a namespace for 'systems' you would create a file at 
helloworld/bootstrap/systems.py where you would define and configure that
namespace.  Then, if helloworld/bootstrap/root.py you would import it like:

.. code-block:: python

    from helloworld.bootstrap import system
    

This triggers the system bootstrap which is responsible for setting up the 
system namespace.


helloworld.controllers
----------------------

The controllers module is used primarily for creating commands.  A controller
is attached to a namespace when that namespace is bootstrapped, therefore
you should not import a controller directly anywhere in your application.

Controllers are used to expose commands to your application, and then perform
operations when that command is called.  Ideally it should not present 
output to the user at all, as this is handled by your templates.  Each command
should perform an action and then return a dictionary of data.  This dictionary
is then used to be rendered into either Json, or by Genshi Text Templating.
That said, some people will not care to use templating and would rather just
print output to the console.  This is perfectly fine, but may clutter up your
controller code with excessive print statements and janky formatting.


helloworld.model
----------------

The model module is used to define objects related to data.  This might be
an SQLAlchemy DeclarativeBase object, or similar data abstractions.  It can
be anything you want, but should be strictly for interfacing with data and 
not interfacing with the user.  

Generally, the controller will use a model object to store data that it is
operating on.  This allows you to separate the code that defines the model
from the other parts of the application that use that model.


helloworld.templates
--------------------

The templates module is a data directory containing nothing but txt template
files.  Note that the first level must be directories related to a namespace.
For example 'helloworld/templates/root' would be the directory with txt
files used for templating commands that are exposed from the root controller.

Cement use the Genshi Text Template Engine to render the dictionary of data
that your controller function returns.  Documentaton can be found at:

    * http://genshi.edgewall.org/wiki/Documentation/text-templates.html 
    
    
helloworld.helpers
------------------

Finally, the helpers module is used for miscellaneous code that is used 
throughout your application.  This code should not be namespace or plugin
specific but should be able to be called from anywhere in your application.
Helpers are often used for quick functions that just don't fit anywhere else.


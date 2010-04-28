Model, View, Controller Overview
================================

The Cement Framework creates applications that encourage the Model, View, 
Controller design.  Each piece of your application should be separated this
way.  For example, if you add a plugin called 'myplugin' you should work out 
of the following files:

 * helloworld/bootstrap/myplugin.py
 * helloworld/model/myplugin.py
 * helloworld/controllers/myplugin.py
 * helloworld/templates/myplugin/
 

As always, review the 'example' plugin included with your application to see
how this all works.  Additionally, a great explanation of a typical MVC design
can be found on `Wikipedia <http://en.wikipedia.org/wiki/Model–view–controller>`_.

 
The Model 
^^^^^^^^^

The Model represents the data that you are working with.  This might be a
User class, or a Product, etc.  The class might be an SQLAlchemy class tied
to a database, or can just simply be an object allowing you to organize data.

**helloworld/model/user.py**

.. code-block:: python

    class User(object):
        def __init__(self, first, last, **kwargs):
            self.first_name = first
            self.last_name = last
            self.address = kwargs.get('address', None)
        
        @property
        def display_name(self):
            return "%s %s" % (self.first_name, self.last_name)

            
The model should always be associated with 'data' and should rarely perform
operations or tasks outside of creating/editing/saving/deleting/etc the 
data associated with that model.

A recommended way of accessing your model throughout your application is to
import all model classes into the 'root' model file like so:

**helloworld/model/root.py**

.. code-block:: python

    from helloworld.model.example import Example
    from helloworld.model.user import User
    from helloworld.model.product import Product
    

Then, throughout your application you can access all of you module objects
like this:

.. code-block:: python

    from helloworld.model import root as model
    
    user = model.User()
    product = model.Product()
    
    
The Controller
^^^^^^^^^^^^^^

The controller is primarily used to expose commands to your application. Note 
that you can expose a command function to any namespace that has been defined.  
By default all commands are exposed to the 'root' namespace and will display 
when you execute:

.. code-block:: text

    $ helloworld --help
    
When you expose to another namespace, like say 'greeting' then your command
will show up under:

.. code-block:: text

    $ helloworld greeting --help
    

A typical example of this would be

**helloworld/controllers/greeting.py**

.. code-block:: python

    from cement.core.controller import CementController, expose
    from helloworld.model import root as model
    
    class GreetingController(CementController):
        @expose('helloworld.templates.greetings.sayhi', namespace='root')
        def sayhi(self, cli_opts, cli_args):
            user = model.User(first=cli_opts.first_name, 
                              last=cli_opts.last_name)
            return dict(user=user)


The method 'GreetingController.sayhi' is exposed to the 'root' namespace, and
will be called when the following command is run:

.. code-block:: text

    $ helloworld sayhi --firstname="John" --lastname="Doe"

    
The user object is then returned in a dictionary and rendered by Genshi with
the template 'helloworld.templates.greetings.sayhi' or what equates to 
'helloworld/templates/greetings/sayhi.txt' on the filesystem (as an example).
The return dictionary can contain strings, lists, tuples, dicts, class objects
and similar data.  It should never return functions or other non-serializable
objects.  

*Note: You can also tell Cement to write output to a file rather than STDOUT
by passing "output_file='/path/to/file'" in your return dict().*

Controllers are very flexible.  Some people won't want to use Genshi
templating, which is perfectly fine.  The following exposes a command without
template rendering:

**helloworld/controllers/greeting.py**

.. code-block:: python

    from cement.core.controller import CementController, expose
    from helloworld.model import root as model
    
    class GreetingController(CementController):
        @expose()
        def sayhi(self, cli_opts, cli_args):
            user = model.User(first=cli_opts.first_name, 
                              last=cli_opts.last_name)
            print 'Hello %s!' % user.display_name
            return dict(user=user)

Notice how we don't need to specify a template path, though the command is 
still exposed.  That said, you should always return any relevant data even
if not rendering a template.  This is because every command automatically
has a Json output engine.  By adding '--json' to the end of your command, all
output is suppressed and only the return data is rendered via Json.  In 
addition stdout, and stderr are also added to the Json output.


The View
^^^^^^^^
            
Note that the templates directory *must* have a directory for each namespace
that contains your template file (more on templating later).  Templating is not
necessary if you prefer to simply use the print statement, that said for
larger applications that provide a lot of console output learning the Genshi
Text Template syntax will significantly clean up your controllers and provide
more robust output to the user.

Our 'sayhi' template would look like:

**helloworld/templates/greetings/sayhi.txt**

.. code-block:: text

    {# This is an example Genshi Text Template.  Documentation is at:          #}\
    {#                                                                         #}\
    {#    http://genshi.edgewall.org/wiki/Documentation/text-templates.html    #}\
    {#                                                                         #}\
    \
    \
    {# --------------------- 78 character baseline --------------------------- #}\
    
    Hello ${user.display_name}
    
    
Using the '78 character baseline' comment in your templates is useful so that 
you ensure your output remains within that limit when possible.
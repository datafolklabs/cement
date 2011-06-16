Nose Testing Your Application
=============================

Because the majority of features in Cement rely on a loaded application to 
access them, testing is a bit more complex than simply running nose on your
source tree.  There are some features built into Cement and the devtools
templates that provide a semi-standard means of testing your application.

Obviously, there are other means of testing besides Nose but it is a very
common standard for testing.  For more information on Nose please see their
`website <http://somethingaboutorange.com/mrl/projects/nose/0.11.2/>`_.

The primary thing to note about nose testing is that your base application 
needs to be loaded in order to test it, however because nose runs all tests
in one stream it means that the application is only loaded once.. and not 
everytime for each test (and for each command you are testing).  For that
reason we have developed a scheme for testing that allows the application
to be loaded once, but then having the ability to simulate running commands
from command line.

As of 0.8.9, creating applications using the cement.devtools and paster 
templates generate a base ./tests directory with functional nose tests
that serve as an example and starting point for adding more tests.  You will
see two files:

 * tests/00_initialize_tests.py
 * tests/example_tests.py
 
 
The 00_initialize_tests.py file must be loaded first (which is why it starts
with 00), which runs the 'nose_main()' function from your application.  This
is an alternative to using 'main()' and does not catch any exceptions 
(allowing you to test for them).  There is also an alternative 
'get_nose_config()' function in yourapp.core.config that has a configuration
specifically for testing and assumes you are running from within the root
of your sources directory.  Finally, in your ./config directory there is a
configuration file called 'yourapp.conf-test' which is meant for testing
only.  

It is important to note that nosetests must be run from the root of your
applications sources (by default)... and that as the application grows you 
must add tests to ./tests to test new features.


Running Tests
-------------

To run the included tests, and future tests that get added you need to first
install the 'nose' package, and also (optionally) install the 'coverage'
package.

.. code-block:: text

    $ easy_install nose coverage
    

Then run the following:

.. code-block:: text

    $ python setup.py nosetests    


Creating a Nose Test
--------------------

All nose testing is standard, however how you call parts of your application
is Cement specific.  Take the following example:

.. code-block:: python

    from nose.tools import raises, with_setup, eq_, ok_
    from cement.core.testing import simulate
    
    def setup_func():
        # do something before every test
        pass
    
    def teardown_func():
        # do something after every test
        pass
    
    @with_setup(setup_func, teardown_func)
    def test_some_functionality():
        (res_dict, output_txt) = simulate([__file__, 'some-cmd', '--foo=bar'])
        # do something to test the results
        
As you can see, simulate is used to 'simulate' running a command at the 
command line.  It takes a list of args which it expects to be in the same
fashion as it would be as 'sys.argv'.  The first argument is '__file__' 
simply because from command line this would be the name of your cli app, 
however in testing it can be useful to know what __file__ the call is coming
from.  

The simulate function returns a tuple of (result_dictionary, output_txt) which
is the 'dict' as returned by the controller function, and the output text as
returned from the output handler.  It should be noted that this is not the 
output of say 'print()', but only output rendered by the output handler 
(genshi, json, etc).

There are many internals within cement that can be used directly such as the
global namespaces, hooks, handlers, etc but that is outside the scope of this
doc.  How to test your applications features is very dependent on what the
application and those features do... however using simulate is a solid 
starting point to getting basic testing of your application going.

Be sure to look in the ./tests directory of your application to see a working
example of this documentation (as of 0.8.9).  Additionally, you can review the
code of the `Cement Test <https://github.com/derks/cement/tree/master/src/cement.test>`_ 
application which provides 95% test coverage of the Cement framework.


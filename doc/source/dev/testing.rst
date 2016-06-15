Unit Testing Your Application
=============================

Testing is an incredibly important part of the application development 
process.  The Cement framework provides some simple helpers and shortcuts for 
executing basic tests of your application. Please note that 
:ref:`cement.utils.test <cement.utils.test>` *does* require the 'nose' package.  That said, 
using :ref:`cement.utils.test <cement.utils.test>` is not required to test a Cement based
application.  It is merely here for convenience, and is used by Cement when
performing its own Nose tests.

For more information on testing, please see the following:

 * `UnitTest <http://docs.python.org/library/unittest.html>`_
 * `Nose <https://nose.readthedocs.io/en/latest/>`_
 * `Coverage <http://nedbatchelder.com/code/coverage/>`_
 
API Reference:

    * :ref:`Cement Testing Utility <cement.utils.test>`
    
An Example Test Case
--------------------

The following outlines a basic test case using the cement.utils.test module.
    
.. code-block:: python

    from cement.utils import test
    from myapp.cli.main import MyApp
    
    class MyTestCase(test.CementTestCase):
        app_class = MyApp
        
        def setUp(self):
            super(MyTestCase, self).setUp()
            
            # Create a default application for the test functions to use.
            # Note that some tests may require you to perform this in the
            # test function in order to alter functionality.  That's perfectly
            # fine, this is only here for convenience.
            self.app = MyApp(argv=[], config_files=[])
            
        def test_myapp(self):
            with self.app as app:
            
                # Perform basic assertion checks.  You can do this anywhere 
                # in the test function, depending on what the assertion is 
                # checking.
                self.ok(app.config.has_key('myapp', 'debug'))
                self.eq(app.config.get('myapp', 'debug'), False)
                
                # Run the applicaion, if necessary
                app.run()
                
                # Test the last rendered output (if app.render was used)
                data, output = app.get_last_rendered()
                self.eq(data, {'foo':'bar'})
                self.eq(output, 'some rendered output text')
            
        @test.raises(Exception)
        def test_exception(self):
            try:
                # Perform tests that intentionally cause an exception.  The 
                # test passes only if the exception is raised.
                raise Exception('test')
            except Exception as e:
                # Do further checks to ensure the proper exception was raised
                self.eq(e.args[0], 'Some Exception Message')
                
                # Finally, call raise again which re-raises the exception that
                # we just caught.  This completes our test (to actually 
                # verify that the exception was raised)
                raise


Cement Testing Caveats
----------------------

In general, testing Cement applications should be no different than testing
anything else in Python.  That said, the following are some things to 
keep in mind.

**Command Line Arguments**

Never rely on ``sys.argv`` for command line arguments.  The ``CementApp()`` 
class accepts the ``argv`` keyword argument allowing you to pass the arguments 
that you would like to test for.  Using ``sys.argv`` will cause issues with 
the calling script (i.e. ``nosetests``, etc) and other issues. Always pass 
``argv`` to ``CementApp()`` in tests.

**Config Files**

It is recommended to always set your apps ``config_files`` setting to an empty 
list, or to something relative to your current working directory.  Using 
default config files settings while testing will introduce unexpected results.  
For example, if a ``~/myapp.conf`` user configuration exists it can alter the
runtime of your application in a way that might cause tests to fail.

**Making Things Easy**

The easiest way to accomplish the above is by sub-classing your ``CementApp`` 
into a special 'testing' version.  For example:

.. code-block:: python

    from cement.utils import test
    from myapp.cli.main import MyApp
    
    class MyTestApp(MyApp):
        class Meta:
            argv = []
            config_files = []
            
    class MyTestCase(test.CementTestCase):
        app_class = MyTestApp
        
        def test_myapp_default(self):
            with self.app as app:
                app.run()
            
        def test_myapp_foo(self):
            with MyTestApp(argv=['--foo', 'bar']) as app:
                app.run()
            
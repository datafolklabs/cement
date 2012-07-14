Unit Testing Your Application
=============================

Testing is an incredibly important part of the application development 
process.  The Cement framework provides some basic helpers for testing your
application. Please note that cement.utils.test *does* require the 'nose' 
package.

API Reference:

    * :ref:`Cement Testing Utility <cement.utils.test>`
    
Example:
    
.. code-block:: python

    from cement.utils import test
    from myapp.cli.main import MyApp
    
    class MyTestCase(test.CementTestCase):
        def setUp(self):
            super(MyTestCase, self).setUp()
            self.reset_backend()
            self.app = MyApp(argv=[], config_files=[])
            
        def test_myapp(self):
            self.app.setup()
            
            # assertion checks
            self.ok(self.config.has_key('myapp', 'debug))
            self.eq(self.config.get('myapp', 'debug'), False)
            
            self.app.run()
            self.app.close()
            
        @test.raises(Exception)
        def test_exception(self):
            raise Exception('test')
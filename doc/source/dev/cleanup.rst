Application Cleanup
===================

The concept of 'cleanup' after application run time is nothing new.  What
happens during 'cleanup' all depends on the application.  This might mean
cleaning up temporary files, removing session data, or removing a PID 
(Process ID) file.  

To allow for application cleanup not only within your program, but also 
external plugins and extensions, there is the app.close() function that must
be called after app.run() and after program execution.

For example:

.. code-block:: python

    from cement.core import foundation
    
    app = foundation.CementApp('helloworld')
    
    try:    
        app.setup()
        app.run()
    finally:
        app.close()
        
        
You will note that we put app.run() within a 'try' block, and app.close() in
a 'finally' block.  The important thing to note is that we put app.close()
within a 'finally' block so that regardless of whether an exception is 
encountered or not, we always run app.close().  The primary purpose of 
app.close() is that is where the 'pre_close' and 'post_close' hooks are run,
allowing extensions/plugins/etc to cleanup after the program runs.

Running Cleanup Code
--------------------

Any extension, or plugin, or even the application itself that has 'cleanup' 
code can do so within the 'pre_close' or 'post_close' hooks.  For example:

.. code-block:: python

    from cement.core import hook

    def my_cleanup(app):
        # do something when app.close() is called
        pass
    
    hook.register('pre_close', my_cleanup)

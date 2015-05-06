Sending Email Messages
======================

Cement defines a mail interface called
:ref:`IMail <cement.core.mail>`, as well as the default
:ref:`DummyMailHandler <cement.ext.ext_dummy>` that implements
the interface.

Please note that there are other handlers that implement the ``IMail``
interface.  The documentation below only references usage based on the
interface and not the full capabilities of the implementation.

The following mail handlers are included and maintained with Cement:

    * :ref:`DummyMailHandler <cement.ext.ext_dummy>` (default)
    * :ref:`SMTPMailHandler <cement.ext.ext_smtp>`


Please reference the :ref:`IMail <cement.core.mail>` interface
documentation for writing your own mail handler.


Example Usage
-------------

.. code-block:: python

    from cement.core.foundation import CementApp

    class MyApp(CementApp):
        class Meta:
            label = 'myapp'

    with MyApp() as app:
        app.run()

        # send an email message
        app.mail.send('This is my message',
            subject='This is my subject',
            to=['you@example.com'],
            from_addr='me@example.com',
            cc=['him@example.com', 'her@example.com'],
            bcc=['boss@example.com']
            )


Note that the default mail handler simply prints messages to the screen, and
does not actually send anything.  You can override this pretty easily without
changing any code by using the built-in
:ref:`SMTPMailHandler <cement.ext.ext_smtp>`.  Simply modify the application
configuration to something like:

**myapp.conf**

.. code-block:: text

    [myapp]
    mail_handler = smtp

    [mail.smtp]
    ssl = 1
    tls = 1
    auth = 1
    username = john.doe
    password = oober_secure_password


.. _faq:

Frequenty Asked Questions
=========================

How do I Manually Print the Help Text for My Application
--------------------------------------------------------

The common question is how to print the help text that you see when you pass
``--help`` to your application, but manually from within your code.  This is
a feature of ArgParse and is as simple as calling:

.. code-block:: python

    app.args.print_help()


Note that, this obviously will not work if using a different argument handler
that implements the ``IArgument`` interface rather than the default
``ArgparseArgumentHandler``.

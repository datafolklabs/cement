Extending CementApp
===================

CementApp provides a convenient ``extend`` mechanism that allows plugins, 
extensions, or the app itself to add objects/functions to the global
application object.  For example, a plugin might extend the CementApp with an 
``api`` member allowing developers to call ``app.api.get(...)``.  The 
application itself does not provide ``app.api`` however the plugin does.  As 
plugins are often third party, it is not possible for the plugin developer to
simply sub-class the CementApp and add the functionality because the CementApp
is already instantiated by the time plugins are loaded.

Take the following for example:

**myapp.py**

.. code-block:: python

    from cement.core.foundation import CementApp

    with CementApp('myapp') as app:
        app.run()


The above is a very simple Cement application, which obviously doesn't do 
much.  That said, we can add a plugin that extends the application to add an
API client object, for example, pretty easily.  Note the following is an 
arbitrary and non-functional example using dRest:

**/etc/myapp/plugins.d/api.conf**

.. code-block:: console

    [api]
    enable_plugin = true
    endpoint = https://example.com/api/v1
    user = john.doe
    password = XXXXXXXXXXXX


**/var/lib/myapp/plugins/api.py**

.. code-block:: python

    import drest
    from cement.core import hook

    def extend_api_object(app):
        # get api info from this plugins configuration
        endpoint = app.config.get('api', 'endpoint')
        user = app.config.get('api', 'user')
        password = app.config.get('api', 'password')

        # create an api object and authenticate
        my_api_client = drest.API(endpoint)
        my_api_client.auth(username, password)

        # extend the global app object with an ``api`` member
        app.extend('api', my_api_client)

    def load(app):
        hook.register('pre_run', extend_api_object)

In the above plugin, we simply created a dRest API client within a 
``pre_run`` hook and then extended the global ``app`` with it.  The developer
can now reference ``app.api`` anywhere that the global ``app`` object is 
accessible.  

Our application code could now look like:

**myapp.py**

.. code-block:: python

    from cement.core.foundation import CementApp

    with CementApp('myapp') as app:
        app.run()

        # use the api object that the plugin provides
        app.api.get(...)


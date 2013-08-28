"""Mustache Framework Extension."""

import sys
import pkgutil
import pystache
from ..core import output, exc, handler
from ..utils.misc import minimal_logger

LOG = minimal_logger(__name__)


class MustacheOutputHandler(output.CementOutputHandler):
    """
    This class implements the :ref:`IOutput <cement.core.output>`
    interface.  It provides text output from template and uses the
    `Mustache Templating Language <http://mustache.github.com>`_.

    **Note** This extension has an external dependency on `pystache`.  You
    must include `pystache` in your applications dependencies as Cement 
    explicitly does *not* include external dependencies for optional 
    extensions.

    Optional / Meta Arguments:

        template_module
            The python (base) module where templates are loaded from.  This
            defaults to 'label.templates'.

    
    Usage:
    
    .. code-block:: python
    
        from cement.core import foundation
        
        class MyApp(foundation.CementApp):
            class Meta:
                label = 'myapp'
                extensions = ['mustache']
                output_handler = 'mustache'
            
        # ...
        
    From here, you would then put a Mustache template file in 
    `myapp.templates.my_template.mustache` and then render a data dictionary
    with it:
        
    .. code-block:: python
    
        # via the app object
        myapp.render(some_data_dict, 'my_template.mustache')
    
        # or from within a controller or handler
        self.app.render(some_data_dict, 'my_template.mustache')

    

    Configuration:

    By default, templates are searched for in the '[app_label].templates' 
    python module.  You can override this by doing something like the 
    following:

    .. code-block:: python
    
        from cement.core import foundation, backend
        from cement.ext.ext_mustache import MustacheOutputHandler

        OUTPUT = MustacheOutputHandler(template_module='myapp.cli.templates')
        
        app = foundation.CementApp('myapp', output_handler=OUTPUT)


    The Mustache extension does honor any configuration file settings.

    """

    class Meta:
        interface = output.IOutput
        label = 'mustache'
        template_module = None

    def __init__(self, *args, **kw):
        super(MustacheOutputHandler, self).__init__(*args, **kw)
        self.config = None

    def _setup(self, app_obj):
        self.app = app_obj
        if self._meta.template_module is None:
            self._meta.template_module = '%s.templates' % self.app._meta.label

    def render(self, data_dict, template):
        """
        Take a data dictionary and render it using the given template file.

        Required Arguments:

        :param data_dict: The data dictionary to render.
        :param template: The file system path to the template file, within the
            template_module.  For example, if the template module were
            'myapp.templates' and the full template file path were 
            'myapp/templates/users/display.mustache' then you would only pass 
            'users/display.mustache'.
        :returns: str (the rendered template text)
        
        """
        
        tmpl_module = self._meta.template_module
        LOG.debug("mustache template module is '%s'" % tmpl_module)

        if template is None:
            raise exc.FrameworkError("Invalid template 'None'.")

        template = template.lstrip('/')

        # get the template content
        tmpl_content = pkgutil.get_data(tmpl_module, template)

        if tmpl_content is None:
            raise exc.FrameworkError(
                "Template file '%s' does not exist in module '%s'." %
                (template, tmpl_module))
        else:
            LOG.debug("rendering output using '%s' as a template." % template)
            return pystache.render(tmpl_content, data_dict)


def load():
    handler.register(MustacheOutputHandler)

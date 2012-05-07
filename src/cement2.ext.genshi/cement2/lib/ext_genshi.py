"""Genshi Framework Extension Library."""

import sys
import pkgutil
from genshi.template import NewTextTemplate
from ..core import output, backend, exc

Log = backend.minimal_logger(__name__)
    
class GenshiOutputHandler(output.CementOutputHandler):
    """
    This class implements the :ref:`IOutput <cement2.core.output>` 
    interface.  It provides text output from template and uses the 
    `Genshi Text Templating Language <http://genshi.edgewall.org/wiki/Documentation/text-templates.html>`_.  
    
    Optional / Meta Arguments:
    
        template_module
            The python (base) module where templates are loaded from.  This 
            defaults to 'label.templates'.
            
    """
    class Meta:
        interface = output.IOutput
        label = 'genshi'
        template_module = None
        
    def __init__(self, *args, **kw):
        super(GenshiOutputHandler, self).__init__(*args, **kw)
        self.config = None
        
    def _setup(self, app_obj):
        self.app = app_obj
        if self._meta.template_module is None:
            self._meta.template_module = '%s.templates' % self.app._meta.label
            
    def render(self, data_dict, template):
        """
        Take a data dictionary and render it using the given template file.
        
        Required Arguments:
        
            data_dict
                The data dictionary to render.

            template
                The file system path to the template file, *after* within the
                template_module.  For example, if the template module were
                'myapp.templates' (a.k.a. 'myapp/templates/__init__.py') then
                and the full template file path were 
                'myapp/templates/users/display.txt' then you would only pass
                'users/display.txt'.
                
        Returns: string
        
        """
        tmpl_module = self._meta.template_module
        Log.debug("genshi template module is '%s'" % tmpl_module)
        
        if template is None:
            raise exc.CementRuntimeError("Invalid template 'None'.")
        
        template = template.lstrip('/')
        
        # get the template content
        tmpl_content = pkgutil.get_data(tmpl_module, template)

        if tmpl_content is None:  
            raise exc.CementRuntimeError(
                "Template file '%s' does not exist in module '%s'." % \
                (template, tmpl_module))
        else:
            Log.debug("rendering output using '%s' as a template." % template)
            tmpl = NewTextTemplate(tmpl_content)
            res = tmpl.generate(**data_dict).render()
            return res
            

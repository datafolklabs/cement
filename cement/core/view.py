"""Methods and classes that enable Cement templating support."""

from cement import namespaces, SAVED_STDOUT
from cement.core.handler import get_handler
from cement.core.exc import CementRuntimeError
from cement.core.log import get_logger

log = get_logger(__name__)
        
class CementOutputHandler(object):
    """
    This is the standard class for output handling.  All output handlers
    should subclass from here.

    Required Arguments:
    
        data
                The dictionary returned from a controller function.
            
        template
            The template file in module form, such as:
            (myapp.templates.namespace.file) where the path to the file
            is actually myapp/templates/namespace/file.txt or similar.
            
    """
    def __init__(self, data, template=None):
        self.data = data
        self.template = template
        self._verify_template()
        self.tmpl_content = self._parse_template()
        
    def _verify_template(self):
        """
        Perform any operations to verify that the handler can use the given
        template.  Should return True if verification is successful or 
        raise CementRuntimeError if not.
        """
        pass
    
    def _parse_template(self):
        """
        Parse a template file and return the contents of the file.
        """
        pass
        
    def render(self):
        """
        Using the contents of the template file, or from the data dictionary
        directly, render output.  Will raise NotImplementedError if not 
        subclassed.
        """
        raise NotImplementedError, "CementOutputHandler.render() must be subclassed."
        
class GenshiOutputHandler(CementOutputHandler):
    def __init__(self, data, template=None):
        """
        Render output from Genshi template text.  In general, this function 
        should not be called directly, as it is called from render().
    
        Required Arguments:
    
            data
                The dictionary returned from a controller function.
            
            template
                The template file in module form, such as:
                (myapp.templates.namespace.file) where the path to the file
                is actually myapp/templates/namespace/file.txt or similar.

        """
        self.tmpl_file = None
        self.tmpl_module = None
        CementOutputHandler.__init__(self, data, template)
        
    def _parse_template(self):
        if self.template:
            try:
                from pkgutil import get_data
            except ImportError:
                # backported for < 2.6 compat
                from cement.backports.pkgutil import get_data
            # Mock up the template path
            parts = self.template.split('.')
            self.tmpl_file = "%s.txt" % parts.pop() # the last item is the file            
            self.tmpl_module = '.'.join(parts) # left over in between
            self.tmpl_content = get_data(self.tmpl_module, self.tmpl_file)
            return self.tmpl_content
            
    def render(self):
        log.debug("rendering genshi output")
        from genshi.template import NewTextTemplate
        if self.tmpl_content:  
            tmpl = NewTextTemplate(self.tmpl_content)
            res = tmpl.generate(**self.data).render()
            return res
        else:
            log.debug('template content is empty.')
            return ''
        
class JsonOutputHandler(CementOutputHandler):
    """
    Render output into JSON from the controller data dictionary.  The
    template param is ignored.

    Required Arguments:

        data
            The dictionary returned from a controller function.
        
        template
            Ignored by this handler

    Usage:

    .. code-block:: python

        from cement.core.handler import get_handler
    
        fake_dict = dict(foo='String', bar=100, list=[1,2,3,4,5])
        handler = get_handler('output', 'json')(fake_dict)
        output = handler.render()
    
    """

    def render(self):
        log.debug("rendering json output")
        import jsonpickle
        from cement import buf_stdout, buf_stderr
        
        self.data['stdout'] = buf_stdout.buffer
        self.data['stderr'] = buf_stderr.buffer
        return jsonpickle.encode(self.data, unpicklable=False)
    
class render(object):
    """
    Class decorator to render data with the specified output handler.
    Called when the function is decorated, sets up the engine and template for 
    later use.
    
    *Note: This is called from the cement.core.controller.expose() decorator 
    and likely shouldn't ever be needed to call directly.*
    
    *Note: If 'output_file' is passed in the return dictionary from func, then
    the output is written to the specified file rather than STDOUT.*
    
    Keywork arguments:
    
        output_handler
            The name of the output handler to use for rendering
            
        template
            The module path to the template (default: None)
            
    
    When called, a tuple is returned consisting of (dict, output), meaning
    the first item is the result dictionary as returned by the original
    function, and the second is the output as rendered by the output handler.
    
    """
    def __init__(self, output_handler, template=None):
        self.func = None
        self.template = template
        self.tmpl_module = None
        self.tmpl_file = None
        self.config = namespaces['root'].config
        self.handler = output_handler

    def __call__(self, func):
        """
        Called when the command function is actually run.  Expects a 
        dictionary in return from the function decorated in __init__.
        
        """
        self.func = func
        
        def wrapper(*args, **kw):  
            # honor output_handler_override
            if self.config['output_handler_override']:
                self.handler = self.config['output_handler_override']

            log.debug("decorating '%s' with '%s:%s'" % \
                (func.__name__, self.handler, self.template))  
            
            res = self.func(*args, **kw)
            
            out = SAVED_STDOUT
            tmpl_content = None
            
            if not res:
                res = dict()
            if type(res) != dict:
                raise CementRuntimeError, \
                    "Controller functions must return type dict()."
            
            if self.handler:
                h = get_handler('output', self.handler)(res, self.template)
                namespaces['root'].config['output_handler'] = self.handler
                out_txt = h.render()
            
                if not out_txt:
                    out_txt = ''
                
                if res.has_key('output_file') and res['output_file']:
                    f = open(res['output_file'], 'w+')
                    f.write(out_txt)
                    f.close()
                elif out and self.config['log_to_console']:
                    out.write(out_txt)
                
                # return res and out_txt, because we want it to be 
                # readable when called directly from 
                # run_controller_command()
                return (res, out_txt)
                    
        return wrapper

"""Cement core output module."""

import os
import sys
import pkgutil
import re
from abc import abstractmethod
from ..core import exc
from ..core.handler import Handler
from ..utils.misc import minimal_logger
from ..utils import fs

LOG = minimal_logger(__name__)


class OutputHandlerBase(Handler):

    """
    This class defines the Output Handler Interface.  Classes that
    implement this interface must provide the methods and attributes defined
    below.

    Usage:

        .. code-block:: python

            from cement.core.output import OutputHandlerBase

            class MyOutputHandler(OutputHandlerBase):
                class Meta:
                    label = 'my_output_handler'
                ...

    """

    class Meta:

        """Handler meta-data."""

        #: The string identifier of the interface
        interface = 'output'

    @abstractmethod
    def render(self, data, *args, **kwargs):
        """
        Render the ``data`` dict into output in some fashion.  This function
        must accept both ``*args`` and ``**kwargs`` to allow an application to
        mix output handlers that support different features.

        Args:
            data (dict): The dictionary whose data we need to render into
                output.

        Returns:
            str, None: The rendered output string, or ``None`` if no output is
            rendered

        """
        pass


class OutputHandler(OutputHandlerBase):

    """Output handler implementation."""

    pass

class TemplateOutputHandler(OutputHandler):

    """Base class for template base output handlers."""

    def _load_template_from_file(self, template_path):
        for template_dir in self.app._meta.template_dirs:
            template_prefix = template_dir.rstrip('/')
            template_path = template_path.lstrip('/')
            full_path = fs.abspath(os.path.join(template_prefix,
                                                template_path))
            LOG.debug("attemping to load output template from file %s" %
                      full_path)
            if os.path.exists(full_path):
                content = open(full_path, 'r').read()
                LOG.debug("loaded output template from file %s" %
                          full_path)
                return (content, full_path)
            else:
                LOG.debug("output template file %s does not exist" %
                          full_path)
                continue

        return (None, None)

    def _load_template_from_module(self, template_path):
        template_module = self.app._meta.template_module
        template_path = template_path.lstrip('/')
        full_module_path = "%s.%s" % (template_module,
                                      re.sub('/', '.', template_path))

        LOG.debug("attemping to load output template '%s' from module %s" %
                  (template_path, template_module))

        # see if the module exists first
        if template_module not in sys.modules:
            try:
                __import__(template_module, globals(), locals(), [], 0)
            except ImportError as e:
                LOG.debug("unable to import template module '%s'."
                          % template_module)
                return (None, None)

        # get the template content
        try:
            content = pkgutil.get_data(template_module, template_path)
            LOG.debug("loaded output template '%s' from module %s" %
                      (template_path, template_module))
            return (content, full_module_path)
        except IOError as e:
            LOG.debug("output template '%s' does not exist in module %s" %
                      (template_path, template_module))
            return (None, None)

    def load_template(self, template_path):
        """
        Loads a template file first from ``self.app._meta.template_dirs`` and
        secondly from ``self.app._meta.template_module``.  The
        ``template_dirs`` have presedence.

        Args:
            template_path (str): The secondary path of the template **after**
                either ``template_module`` or ``template_dirs`` prefix (set via
                ``App.Meta``)

        Returns:
            str: The content of the template

        Raises:
            cement.core.exc.FrameworkError: If the template does not exist in
                either the ``template_module`` or ``template_dirs``

        """
        res = self.load_template_with_location(template_path)
        content, template_type, path = res

        # only return content for backward compatibility
        return content

    # FIX ME: Should eventually replace ``load_template()`` (but that breaks
    # compatibility)
    def load_template_with_location(self, template_path):
        """
        Loads a template file first from ``self.app._meta.template_dirs`` and
        secondly from ``self.app._meta.template_module``.  The
        ``template_dirs`` have presedence.

        Args:
            template_path (str): The secondary path of the template **after**
                either ``template_module`` or ``template_dirs`` prefix (set via
                ``App.Meta``)

        Returns:
            tuple: The content of the template (``str``), the type of template
            (``str``: ``directory``, or ``module``), and the path (``str``) of
            the directory or module)

        Raises:
            cement.core.exc.FrameworkError: If the template does not exist in
                either the ``template_module`` or ``template_dirs``.
        """
        if not template_path:
            raise exc.FrameworkError("Invalid template path '%s'." %
                                     template_path)

        # first attempt to load from file
        content, path = self._load_template_from_file(template_path)
        if content is None:
            # second attempt to load from module
            content, path = self._load_template_from_module(template_path)
            template_type = 'module'
        else:
            template_type = 'directory'

        # if content is None, that means we didn't find a template file in
        # either and that is an exception
        if content is None:
            raise exc.FrameworkError("Could not locate template: %s" %
                                     template_path)

        return (content, template_type, path)

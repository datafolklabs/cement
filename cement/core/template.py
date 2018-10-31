"""Cement core template module."""

import os
import sys
import pkgutil
import re
import shutil
from abc import abstractmethod
from ..core import exc
from ..core.interface import Interface
from ..core.handler import Handler
from ..utils.misc import minimal_logger
from ..utils import fs

LOG = minimal_logger(__name__)


class TemplateInterface(Interface):

    """
    This class defines the Template Interface.  Handlers that implement this
    interface must provide the methods and attributes defined below. In
    general, most implementations should sub-class from the provided
    :class:`TemplateHandler` base class as a starting point.
    """

    class Meta:

        """Handler meta-data."""

        #: The string identifier of the interface
        interface = 'template'

    @abstractmethod
    def render(self, content, data):
        """
        Render ``content`` as a template using the ``data`` dict.

        Args:
            content (str): The content to be rendered as a template.
            data (dict): The data dictionary to render with template.

        Returns:
            str: The rendered template string.

        """
        pass  # pragma: nocover

    @abstractmethod
    def copy(self, src, dest, data):
        """
        Render the ``src`` directory path, and copy to ``dest``.  This method
        must render directory and file **names** as template content, as well
        as the contents of files.

        Args:
            src (str): The source template directory path.
            dest (str): The destination directory path.
            data (dict): The data dictionary to render with template.
        Returns: None
        """
        pass  # pragma: nocover

    @abstractmethod
    def load(self, path):
        """
        Loads a template file first from ``self.app._meta.template_dirs`` and
        secondly from ``self.app._meta.template_module``.  The
        ``template_dirs`` have presedence.

        Args:
            path (str): The secondary path of the template **after**
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
        pass  # pragma: nocover


class TemplateHandler(TemplateInterface, Handler):
    """
    Base class that all template implementations should sub-class from.
    Keyword arguments passed to this class will override meta-data options.
    """

    class Meta:
        #: Unique identifier (str), used internally.
        label = None

        #: The interface that this handler implements.
        interface = 'template'

        #: List of file patterns to exclude (copy but not render as template)
        exclude = None

        #: List of file patterns to ignore completely (not copy at all)
        ignore = None

    def __init__(self, *args, **kwargs):
        super(TemplateHandler, self).__init__(*args, **kwargs)
        if self._meta.ignore is None:
            self._meta.ignore = []
        if self._meta.exclude is None:
            self._meta.exclude = []

    def render(self, content, data):
        """
        Render ``content`` as template using using the ``data`` dictionary.

        Args:
            content (str): The content to render.
            data (dict): The data dictionary to interpolate in the template.

        Returns:
            str: The rendered content.
        """

        # must be provided by a subclass
        raise NotImplementedError  # pragma: nocover

    def _match_patterns(self, item, patterns):
        for pattern in patterns:
            if re.match(pattern, item):
                return True
        return False

    def copy(self, src, dest, data, force=False, exclude=None, ignore=None):
        """
        Render ``src`` directory as template, including directory and file
        names, and copy to ``dest`` directory.

        Args:
            src (str): The source directory path.
            dest (str): The destination directory path.
            data (dict): The data dictionary to interpolate in the template.
            force (bool): Whether to overwrite existing files.
            exclude (list): List of regular expressions to match files that
                should only be copied, and not rendered as template.
            ignore (list): List of regular expressions to match files that
                should be completely ignored and not copied at all.

        Returns:
            bool: Returns ``True`` if the copy completed successfully.

        Raises:
            AssertionError: If the ``src`` template directory path does not
                exists, and when a ``dest`` file already exists and
                ``force is not True``.
        """

        dest = fs.abspath(dest)
        src = fs.abspath(src)
        escaped_src = src.encode('unicode-escape').decode('utf-8')

        # double escape for regex matching
        escaped_src_pattern = escaped_src.encode('unicode-escape')
        escaped_src_pattern = escaped_src_pattern.decode('utf-8')

        if exclude is None:
            exclude = []
        if ignore is None:
            ignore = []
        ignore_patterns = self._meta.ignore + ignore
        exclude_patterns = self._meta.exclude + exclude

        assert os.path.exists(src), "Source path %s does not exist!" % src

        if not os.path.exists(dest):
            os.makedirs(dest)

        LOG.debug('copying source template %s -> %s' % (src, dest))

        # here's the fun
        for cur_dir, sub_dirs, files in os.walk(src):
            escaped_cur_dir = cur_dir.encode('unicode-escape').decode('utf-8')

            if cur_dir == '.':
                continue    # pragma: nocover
            elif cur_dir == src:
                # don't render the source base dir (because we are telling it
                # where to go as `dest`)
                cur_dir_dest = dest
            elif self._match_patterns(cur_dir, ignore_patterns):
                LOG.debug(
                    'not copying ignored directory: %s' % cur_dir)
                continue
            elif self._match_patterns(cur_dir, exclude_patterns):
                LOG.debug(
                    'not rendering excluded directory as template: ' +
                    '%s' % cur_dir)

                cur_dir_stub = re.sub(escaped_src_pattern,
                                      '',
                                      escaped_cur_dir)
                cur_dir_stub = cur_dir_stub.lstrip('/')
                cur_dir_stub = cur_dir_stub.lstrip('\\\\')
                cur_dir_stub = cur_dir_stub.lstrip('\\')
                cur_dir_dest = os.path.join(dest, cur_dir_stub)
            else:
                # render the cur dir
                LOG.debug(
                    'rendering directory as template: %s' % cur_dir)

                cur_dir_stub = re.sub(escaped_src_pattern,
                                      '',
                                      escaped_cur_dir)
                cur_dir_stub = self.render(cur_dir_stub, data)
                cur_dir_stub = cur_dir_stub.lstrip('/')
                cur_dir_stub = cur_dir_stub.lstrip('\\\\')
                cur_dir_stub = cur_dir_stub.lstrip('\\')
                cur_dir_dest = os.path.join(dest, cur_dir_stub)

            # render sub-dirs
            for sub_dir in sub_dirs:
                escaped_sub_dir = sub_dir.encode('unicode-escape')
                escaped_sub_dir = escaped_sub_dir.decode('utf-8')

                full_path = os.path.join(cur_dir, sub_dir)

                if self._match_patterns(full_path, ignore_patterns):
                    LOG.debug(
                        'not copying ignored sub-directory: ' +
                        '%s' % full_path)
                    continue
                elif self._match_patterns(full_path, exclude_patterns):
                    LOG.debug(
                        'not rendering excluded sub-directory as template: ' +
                        '%s' % full_path)
                    sub_dir_dest = os.path.join(cur_dir_dest, sub_dir)
                else:
                    LOG.debug(
                        'rendering sub-directory as template: %s' % full_path)

                    new_sub_dir = re.sub(escaped_src_pattern,
                                         '',
                                         self.render(escaped_sub_dir, data))
                    sub_dir_dest = os.path.join(cur_dir_dest, new_sub_dir)

                if not os.path.exists(sub_dir_dest):
                    LOG.debug('creating sub-directory %s' % sub_dir_dest)
                    os.makedirs(sub_dir_dest)

            for _file in files:
                _rendered = self.render(_file, data)
                new_file = re.sub(escaped_src_pattern, '', _rendered)

                _file = fs.abspath(os.path.join(cur_dir, _file))
                _file_dest = fs.abspath(os.path.join(cur_dir_dest, new_file))

                # handle if destination path already exists

                if os.path.exists(_file_dest):
                    if force is True:
                        LOG.debug(
                            'overwriting existing file: %s ' % _file_dest)
                    else:
                        assert False, \
                            'Destination file already exists: %s ' % _file_dest

                if self._match_patterns(_file, ignore_patterns):
                    LOG.debug(
                        'not copying ignored file: ' +
                        '%s' % _file)
                    continue

                elif self._match_patterns(_file, exclude_patterns):
                    LOG.debug(
                        'not rendering excluded file: ' +
                        '%s' % _file)
                    shutil.copy(_file, _file_dest)

                else:
                    LOG.debug('rendering file as template: %s' % _file)
                    f = open(_file, 'r')
                    content = f.read()
                    f.close()

                    _file_content = self.render(content, data)
                    f = open(_file_dest, 'w')
                    f.write(_file_content)
                    f.close()

        return True

    def _load_template_from_file(self, template_path):
        for template_dir in self.app._meta.template_dirs:
            template_prefix = template_dir.rstrip('/')
            template_path = template_path.lstrip('/')
            full_path = fs.abspath(os.path.join(template_prefix,
                                                template_path))
            LOG.debug(
                "attemping to load output template from file %s" % full_path)
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
            except ImportError:
                LOG.debug("unable to import template module '%s'."
                          % template_module)
                return (None, None)

        # get the template content
        try:
            content = pkgutil.get_data(template_module, template_path)
            LOG.debug("loaded output template '%s' from module %s" %
                      (template_path, template_module))
            return (content, full_module_path)
        except IOError:
            LOG.debug("output template '%s' does not exist in module %s" %
                      (template_path, template_module))
            return (None, None)

    def load(self, template_path):
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

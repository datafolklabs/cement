"""Common File System Utilities."""

import os
import tempfile
import shutil


class Tmp(object):

    """
    Provides creation and cleanup of a separate temporary directory, and file.

    Keyword Arguments:
        cleanup (bool): Whether or not to delete the temporary directory and
            file on exit (when used with the ``with`` operator).
        suffix (str): The suffix that the directory and file will end with.
            Default: *no suffix*
        prefix (str): The prefix that the directory and file will start
            with. Default: *no prefix*
        dir (str): The parent directory path that the temp directory and file
            will be created in.  Default: *system default temporary path*

    Example:

        .. code-block:: python

            from cement.utils import fs

            with fs.Tmp() as tmp:
                # do something with a temporary directory
                os.path.listdir(tmp.dir)

                # do something with a temporary file
                with open(tmp.file, 'w') as f:
                    f.write('some data')

    """

    def __init__(self, **kwargs):
        self.cleanup = kwargs.get('cleanup', True)
        suffix = kwargs.get('suffix', '')
        prefix = kwargs.get('prefix', 'tmp')
        dir = kwargs.get('dir', None)

        self.dir = tempfile.mkdtemp(suffix=suffix,
                                    prefix=prefix,
                                    dir=dir)
        _, self.file = tempfile.mkstemp(suffix=suffix,
                                        prefix=prefix,
                                        dir=dir)

    def remove(self):
        """
        Remove the temporary directory (and file) if it exists, and
        ``self.cleanup`` is ``True``.
        """
        if self.cleanup is True:
            if os.path.exists(self.dir):
                shutil.rmtree(self.dir)
            if os.path.exists(self.file):
                os.remove(self.file)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.remove()


def abspath(path):
    """
    Return an absolute path, while also expanding the ``~`` user directory
    shortcut.

    Args:
        path (str): The original path to expand.

    Returns:
        str: The fully expanded, absolute path to the given ``path``

    Example:

        .. code-block:: python

            from cement.utils import fs

            fs.abspath('~/some/path')
            fs.abspath('./some.file')

    """
    return os.path.abspath(os.path.expanduser(path))


def join(*args, **kwargs):
    """
    Return a complete, joined path, by first calling ``abspath()`` on the first
    item to ensure the final path is complete.

    Args:
        paths (list): A list of paths to join together.

    Returns:
        list: The complete and absolute joined path.

    Example:

        .. code-block:: python

            from cement.utils import fs

            fs.join('~/some/path', 'some/other/relevant/paht')

    """
    paths = list(args)
    first_path = abspath(paths.pop(0))
    return os.path.join(first_path, *paths, **kwargs)


def join_exists(*paths):
    """
    Wrapper around ``os.path.join()``, ``os.path.abspath()``, and
    ``os.path.exists()``.

    Arguments:
        paths (list): List of paths to join, and then return ``True`` if that
                      path exists, or ``False`` if it does not.

    Returns:
        tuple: First item is the fully joined absolute path, and the second
               is ``bool`` (whether that path exists or not).
    """
    path = join(*paths)
    return (path, os.path.exists(path))


def ensure_dir_exists(path):
    """
    Ensure the directory ``path`` exists, and if not create it.

    Arguments:
        path (str): The filesystem path of a directory.

    Raises:
        AssertionError: If the directory ``path`` exists, but is not a
        directory.

    Returns: None
    """

    path = abspath(path)

    if os.path.exists(path) and not os.path.isdir(path):
        raise AssertionError('Path `%s` exists but is not a directory!' % path)
    elif not os.path.exists(path):
        os.makedirs(path)


def ensure_parent_dir_exists(path):
    """
    Ensure the parent directory of ``path`` (file, or directory) exists, and if
    not create it.

    Arguments:
        path (str): The filesystem path of a file or directory.

    Returns: None
    """

    parent_dir = os.path.dirname(abspath(path))
    return ensure_dir_exists(parent_dir)


def backup(path, suffix='.bak'):
    """
    Rename a file or directory safely without overwriting an existing
    backup of the same name.

    Args:
        path (str): The path to the file or directory to make a backup of.
        suffix (str): The suffix to rename files with.

    Returns:
        str: The new path of backed up file/directory

    Example:

        .. code-block:: python

            from cement.utils import fs

            fs.backup('/path/to/original/file')

    """
    count = -1
    new_path = None
    while True:
        if os.path.exists(path):
            if count == -1:
                new_path = "%s%s" % (path, suffix)
            else:
                new_path = "%s%s.%s" % (path, suffix, count)
            if os.path.exists(new_path):
                count += 1
                continue
            else:
                if os.path.isfile(path):
                    shutil.copy(path, new_path)
                elif os.path.isdir(path):
                    shutil.copytree(path, new_path)
                break
        else:
            break
    return new_path


# Kinda dirty, but should resolve issues on Windows per #183
if 'HOME' in os.environ:
    HOME_DIR = abspath(os.environ['HOME'])
else:
    HOME_DIR = abspath('~')  # pragma: nocover

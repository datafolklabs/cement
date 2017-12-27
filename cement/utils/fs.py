"""Common File System Utilities."""

import os
import shutil


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

            from cement.core.utils import fs

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

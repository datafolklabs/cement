"""Common File System Utilities."""

import os
import shutil
import tempfile
from datetime import datetime
from pathlib import Path as _Path
from types import TracebackType
from typing import Any


class Tmp:

    """
    Provides creation and cleanup of a separate temporary directory, and file.

    Keyword Args:
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
                os.listdir(tmp.dir)

                # do something with a temporary file
                with open(tmp.file, 'w') as f:
                    f.write('some data')

    """

    dir: str
    file: str

    def __init__(self, **kwargs: str) -> None:
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

    def remove(self) -> None:
        """
        Remove the temporary directory (and file) if it exists, and
        ``self.cleanup`` is ``True``.
        """
        if self.cleanup is True:
            if _Path(self.dir).exists():
                shutil.rmtree(self.dir)
            if _Path(self.file).exists():
                os.remove(self.file)

    def __enter__(self):  # type: ignore
        return self

    def __exit__(self,
                 __exc_type: type[BaseException] | None,
                 __exc_value: BaseException | None,
                 __exc_traceback: TracebackType | None) -> None:
        self.remove()


def abspath(path: str, strip_trailing_slash: bool = True) -> str:
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

    return str(_Path(path).expanduser().resolve(strict=False))


def join(*args: str, **kwargs: Any) -> str:
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
    # NOTE: ``**kwargs`` is retained on the public signature for backward
    # compatibility but is unused by the body. The original implementation
    # forwarded kwargs to the stdlib path-join (which only accepts
    # positional args), so any non-empty kwargs would have raised
    # TypeError. No in-tree caller passes kwargs; downstream callers
    # passing kwargs were already broken pre-migration.
    paths = list(args)
    first_path = abspath(paths.pop(0))
    p = _Path(first_path)
    for part in paths:
        p = p / part
    return str(p)


def join_exists(*paths: str) -> tuple[str, bool]:
    """
    Wrapper around :func:`join` plus an existence check via
    :class:`pathlib.Path`.

    Args:
        paths (list): List of paths to join, and then return ``True`` if that
                      path exists, or ``False`` if it does not.

    Returns:
        tuple: First item is the fully joined absolute path, and the second
               is ``bool`` (whether that path exists or not).
    """
    path = join(*paths)
    return (path, _Path(path).exists())


def ensure_dir_exists(path: str) -> None:
    """
    Ensure the directory ``path`` exists, and if not create it.

    Args:
        path (str): The filesystem path of a directory.

    Raises:
        AssertionError: If the directory ``path`` exists, but is not a
        directory.

    Returns: None
    """

    path = abspath(path)
    p = _Path(path)

    if p.exists() and not p.is_dir():
        raise AssertionError(f'Path `{path}` exists but is not a directory!')
    elif not p.exists():
        p.mkdir(parents=True)


def ensure_parent_dir_exists(path: str) -> None:
    """
    Ensure the parent directory of ``path`` (file, or directory) exists, and if
    not create it.

    Args:
        path (str): The filesystem path of a file or directory.

    Returns: None
    """

    parent_dir = str(_Path(abspath(path)).parent)
    return ensure_dir_exists(parent_dir)


def backup(path: str, suffix: str = '.bak', **kwargs: Any) -> str | None:
    """
    Rename a file or directory safely without overwriting an existing
    backup of the same name.

    Args:
        path (str): The path to the file or directory to make a backup of.
        suffix (str): The suffix to rename files with.

    Keyword Args:
        timestamp(bool): whether to add a timestamp to the backup suffix
        timestamp_format(str): Date-Time format in python datetime.datetime
            notation. default '%Y-%m-%d-%H:%M:%S'

    Returns:
        str: The new path of backed up file/directory

    Example:

        .. code-block:: python

            from cement.utils import fs

            fs.backup('/path/to/original/file')

    """
    count = -1
    new_path = None
    path = abspath(path)

    if kwargs.get('timestamp', False) is True:
        timestamp_format = kwargs.get('timestamp_format', '%Y-%m-%d-%H:%M:%S')
        timestamp = datetime.now().strftime(timestamp_format)
        suffix = '-'.join((suffix, timestamp))

    p = _Path(path)
    while True:
        if p.exists():
            if count == -1:
                new_path = f"{path}{suffix}"
            else:
                new_path = f"{path}{suffix}.{count}"
            if _Path(new_path).exists():
                count += 1
                continue
            else:
                if p.is_file():
                    shutil.copy(path, new_path)
                elif p.is_dir():
                    shutil.copytree(path, new_path)
                break
        else:
            break  # pragma: nocover  # defensive: unreachable
    return new_path


# Kinda dirty, but should resolve issues on Windows per #183
if 'HOME' in os.environ:
    HOME_DIR = abspath(os.environ['HOME'])
else:
    HOME_DIR = abspath('~')  # pragma: nocover  # platform-specific

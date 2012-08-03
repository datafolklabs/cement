"""Common File System Utilities."""

import os
import shutil

def abspath(path):
    """
    Return an absolute path, while also expanding the '~' user directory
    shortcut.
    
    :param path: The original path to expand.
    :rtype: str
            
    """
    return os.path.abspath(os.path.expanduser(path))

def backup(path):
    """
    Rename a file or directory safely without overwriting an existing
    backup of the same name.
    
    :param path: The path to the file or directory to make a backup of.
    :returns: The new path of backed up file/directory
    :rtype: str
    
    """
    count = -1
    new_path = None
    while True:
        if os.path.exists(path):
            if count == -1:
                new_path = "%s.bak" % (path)
            else:
                new_path = "%s.bak.%s" % (path, count)
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
"""Common File System Utilities."""

import os

def abspath(path):
    """
    Return an absolute path, while also expanding the '~' user directory
    shortcut.
    
    Required Arguments:
    
        path
            The original path to expand.
            
    """
    return os.path.abspath(os.path.expanduser(path))
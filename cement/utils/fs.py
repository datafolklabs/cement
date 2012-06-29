"""Common File System Utilities."""

import os

def abspath(path):
    return os.path.abspath(os.path.expanduser(path))
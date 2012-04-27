"""Cement util module."""                        

import os

def is_true(item):
    """
    Given a value, determine if it is one of [True, 'True', 'true', 1, '1'].
    
    """
    if item in [True, 'True', 'true', 1, '1']:
        return True
    else:
        return False

def abspath(path):
    """
    Wrapper to return the absolute path of a given path.
    
    """
    return os.path.abspath(os.path.expanduser(path))
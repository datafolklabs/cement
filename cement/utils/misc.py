"""Misc utilities."""

def is_true(item):
    """
    Given a value, determine if it is one of [True, 'True', 'true', 1, '1'].
    
    """
    if item in [True, 'True', 'true', 1, '1']:
        return True
    else:
        return False

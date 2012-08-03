"""Misc utilities."""

def is_true(item):
    """
    Given a value, determine if it is one of [True, 'True', 'true', 1, '1'].

    :param item: The item to convert to a boolean.
    :returns: True if `item` is in ``[True, 'True', 'true', 1, '1']``, False
        otherwise.
    :rtype: boolean
    
    """
    if item in [True, 'True', 'true', 1, '1']:
        return True
    else:
        return False

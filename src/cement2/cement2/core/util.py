                        
def is_true(item):
    if item in [True, 'True', 'true', 1, '1']:
        return True
    else:
        return False
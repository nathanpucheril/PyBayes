# Utilities for Bayes Net
# ________________________
# @author Nathan Pucheril
# @author Keith Hardaway

def islist_like(iterable):
    return hasattr(iterable, '__iter__') and not isinstance(iterable, str) and not isinstance(iterable, dict)

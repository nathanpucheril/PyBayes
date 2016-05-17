# Utilities for Bayes Net
# ________________________
# @author Nathan Pucheril
# @author Keith Hardaway

class OrderedMultiDict(dict):
    """docstring for """
    # def __init__(self, *args, **kwargs):
    #     self.update(*args, **kwargs)

    def __getitem__(self, **key):
        modified_key = tuple(sorted(key.items()))
        return dict.__getitem__(self, modified_key)

    def __setitem__(self, value, **key):
        modified_key = tuple(sorted(key.items()))
        dict.__setitem__(self, modified_key, value)

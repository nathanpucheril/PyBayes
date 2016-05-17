# Utilities for Bayes Net
# ________________________
# @author Nathan Pucheril
# @author Keith Hardaway

class UnorderedMultiDict(dict):
    """docstring for """
    # def __init__(self, *args, **kwargs):
    #     self.update(*args, **kwargs)

    def __getitem__(self, key, **args):
        modified_key = tuple(sorted(key.items()))
        return dict.__getitem__(self, modified_key)

    def __setitem__(self, key, value):
        modified_key = tuple(sorted(key))
        dict.__setitem__(self, modified_key, value)


d = UnorderedMultiDict()
d[{k = 4}]

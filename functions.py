# Common functions, such as noops


def constant_func(const, docstring=''):
    '''
    Constructs a function that always returns the value const.
    Mostly here for implementing noop, true, false.
    '''
    func = lambda *a, **kw: const
    func.__doc__ = docstring
    return func

noop = constant_func(None, '''Useful default for a callback''')
true = constant_func(True, '''Always returns True''')
false = constant_func(False, '''Always returns False''')

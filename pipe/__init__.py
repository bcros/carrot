## carrot.pipe.__init__


class pipe(object):
    """
    Decorator that allows us to use the pipe notation

    @pipe
    def where(iterable, criteria_func):
        return [x for x in iterable if criteria_func(x)]
    >>> evens = range(16) | where(lambda x: x%2 == 0)
    >>> evens
    [0, 2, 4, 6, 8, 10, 12, 14]
    Use with generators for memory-happy chaining fun!
    Easily wrap most current functional methods (sometimes you'll need to curry)
    >>> psum = pipe(sum)
    >>> print range(1,5) | psum
    10
    """
    def __init__(self, func):
        self.func = func
        self.__doc__ = func.__doc__

    def __ror__(self, lhs):
        return self.func(lhs)

    def __call__(self, *args, **kwargs):
        return pipe(lambda lhs: self.func(lhs, *args, **kwargs))

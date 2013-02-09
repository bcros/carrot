from . import pipe
from .. import functions
import itertools

_real_all = all
_real_any = any


@pipe
def all(iterable, predicate):
    """builtin all for iterable"""
    return _real_all(predicate(x) for x in iterable)


@pipe
def any(iterable, predicate):
    """builtin any for iterable"""
    return _real_any(predicate(x) for x in iterable)


@pipe
def cast_each(iterable, dtype):
    """casts each item in iterable as dtype"""
    return (dtype(item) for item in iterable)


@pipe
def cast_as(iterable, dtype):
    """casts the iterable as dtype"""
    return dtype(iterable)


@pipe
def islice(iterable, start, stop, step):
    """itertools.islice"""
    return itertools.islice(iterable, start, stop, step)


@pipe
def reverse(iterable):
    """builtin reverse generator of iterable"""
    return reversed(iterable)


@pipe
def take(iterable, nitems):
    """Returns a generator of first nitems of iterable"""
    return itertools.islice(iterable, 0, nitems)


def take_every(iterable, step):
    """Returns a generator of iterable[::step]"""
    return itertools.islice(iterable, None, None, step)


@pipe
def take_until(iterable, predicate=functions.false):
    """Returns items until predicate(item) is true for an item in iterable"""
    for item in iterable:
        if not predicate(item):
            yield item
        else:
            return


@pipe
def take_while(iterable, predicate=functions.true):
    """Returns items while predicate(item) is true for item in iterable"""
    return itertools.takewhile(predicate, iterable)


@pipe
def where(iterable, predicate=functions.true):
    """Returns a generator on iterable of items where predicate(item)"""
    return (x for x in iterable if predicate(x))


@pipe
def where_not(iterable, predicate=functions.false):
    """Returns a generator on iterable of items where not predicate(item)"""
    return (x for x in iterable if not predicate(x))

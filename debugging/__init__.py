## carrot.debugging.__init__
import time
import cProfile
import pstats
from ..io import rm


def class_name(obj):
    """
    Returns the class name of an object.
    Includes namespaces; for example-
    in module a.py:
    class b(object):
        def __init__(self):
            class c(object): pass
        self.c = c()
    d = b().c
    print class_name(d) # prints "a.b.c"
    """
    return ".".join(str(obj.__class__).split("'")[1].split(".")[1:])


def profile(funcstr):
    filename = "profile_tmpfile"
    cProfile.run(funcstr, filename)
    stats = pstats.Stats(filename)
    rm(filename)
    return stats


def timer():
    '''
    Super basic function that you call when you want to start timing,
    and call again to get the delta since it started.
    '''
    clock = time.clock  # Localize function for tighter timing
    start = clock()
    return lambda: clock() - start

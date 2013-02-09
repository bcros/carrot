# Common iteration tools
import itertools


def ezip(*iters):
    '''
    Enumerated zip, almost the same as enumerate(zip(*iters))
    (different because you don't need to unpack twice)

    Example:
    first_names = ['Sarah', 'Bob', 'Steve']
    last_names = ['Jane', 'Log', 'Smith']
    for i, first, last in ezip(first_names, last_names):
        print i, "{}, {}".format(last, first)

    # prints:
    # 0 Jane, Sarah
    # 1 Log, Bob
    # 2 Smith, Steve

    The alternative is to use enum around zip:
    for i, (first, last) in enumerate(zip(first_names, last_names)):
        print i, "{}, {}".format(last, first)
    '''
    return itertools.izip(itertools.count(), *iters)

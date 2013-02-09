import itertools


def merge_dicts(*dicts):
    '''Merges any number of dictionaries into a new dictionary'''
    return dict(itertools.chain(*[d.iteritems() for d in dicts]))

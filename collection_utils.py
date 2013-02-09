import itertools
import collections
from contextlib import contextmanager


def merge_dicts(*dicts):
    '''Merges any number of dictionaries into a new dictionary'''
    return dict(itertools.chain(*[d.iteritems() for d in dicts]))


@contextmanager
def set_transaction(mutable_set, internal_set=set):
    '''
    Allows you to mutate a set during iteration.
    Changes are not reflected in the scope of the modifying iteration,
        but are available immediately after.
    Leaving the scope of the context manager commits pending changes.
    internal_set should support the usual mutable set functions,
        including update and difference_update.
        (see the built-in collections.MutableSet)
    '''
    transaction_set = TransactionSet(mutable_set, internal_set=internal_set)

    yield transaction_set
    transaction_set.flush_transaction()

    mutable_set.clear()
    mutable_set.update(transaction_set)


def apply_set_diffs(set, add, discard):
    '''
    Adds all elements of add to the set
    Discards all elements of discard from the set
    '''
    set.update(add)
    set.difference_update(discard)


class TransactionSet(collections.MutableSet):
    '''
    Supports **sort of** mutation during iteration.
    Changes made against one iterator can't be seen in that iterator
    '''
    def __init__(self, iterable=None, internal_set=set):
        self._setcls = internal_set
        self._set = self._setcls()
        self._tradd = self._setcls()
        self._trdis = self._setcls()
        if iterable is not None:
            self._set.update(iterable)

    def flush_transaction(self):
        '''
        Commit any pending changes to the underlying set.
        Clear transaction sets
        '''
        apply_set_diffs(self._set, self._tradd, self._trdis)
        self._tradd, self._trdis = self._setcls(), self._setcls()

    def add(self, value):
        self._tradd.add(value)
        self._trdis.discard(value)

    def discard(self, value):
        self._trdis.add(value)
        self._tradd.discard(value)

    def __contains__(self, value):
        return (value in self._tradd
                or value in self._set and not value in self._trdis)

    def __len__(self):
        return len(self._set) + len(self._tradd) - len(self._trdis)

    def __iter__(self):
        if not self._tradd and not self._trdis:
            return iter(self._set)
        snapshot = self._setcls(self._set)
        apply_set_diffs(snapshot, self._tradd, self._trdis)
        return iter(snapshot)

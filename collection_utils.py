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
    Changes are not reflected in the scope of the modifying iteration, but are available immediately after.
    Leaving the scope of the context manager commits pending changes.
    internal_set should support the usual mutable set functions, as well as update.
        (see set.update)
    '''
    transaction_set = TransactionSet(mutable_set, internal_set=internal_set)

    yield transaction_set
    transaction_set.flush_transaction()

    mutable_set.clear()
    mutable_set.update(transaction_set)


def apply_transaction(set, trans):
    for value, op in trans.iteritems():
        if op:
            set.add(value)
        else:
            set.discard(value)


class TransactionSet(collections.MutableSet):
    '''
    Supports **sort of** mutation during iteration.
    Changes made against one iterator can't be seen in that iterator
    '''
    def __init__(self, iterable=None, internal_set=set):
        self._setcls = internal_set
        self._set = self._setcls()
        self._tran = {}
        if iterable is not None:
            self._set.update(iterable)

    def flush_transaction(self):
        '''
        Commit any pending changes to the underlying set.
        Clear transaction sets
        '''
        apply_transaction(self._set, self._tran)
        self._tran = {}

    def add(self, value):
        self._tran[value] = 1

    def discard(self, value):
        self._tran[value] = 0

    def update(self, iterable):
        for it in iterable:
            self.add(it)

    def __contains__(self, value):
        if value in self._tran:
            return self._tran[value]
        return value in self._set

    def __len__(self):
        tran_vals = self._tran.values()
        return len(self._set) + tran_vals.count(1) - tran_vals.count(0)

    def __iter__(self):
        if not self._tran:
            return iter(self._set)
        snapshot = self._setcls(self._set)
        apply_transaction(snapshot, self._tran)
        return iter(snapshot)

    def __repr__(self):
        items = map(str, self)
        return "TransactionSet([{}])".format(', '.join(items))

    def __str__(self):
        return repr(self)

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
    internal_set should support the usual mutable set functions
        (see the built-in collections.MutableSet)
    '''
    transaction_set = TransactionSet(mutable_set, internal_set=internal_set)

    transaction_set.begin_transaction()
    yield transaction_set
    transaction_set.commit_transaction()

    mutable_set.clear()
    if hasattr(mutable_set, 'update'):
        mutable_set.update(transaction_set)
    else:
        for value in transaction_set:
            mutable_set.add(value)


def apply_set_diffs(set, add, discard):
    '''
    Adds all elements of add to the set
    Discards all elements of discard from the set
    '''
    if hasattr(set, 'update'):
        set.update(add)
    else:
        for value in add:
            set.add(value)

    if hasattr(set, 'difference_update'):
        set.difference_update(discard)
    else:
        for value in discard:
            set.discard(value)


class TransactionSet(collections.MutableSet):
    '''
    Supports **sort of** mutation during iteration.
    Changes made against one iterator can't be seen in that iterator

    Only supports one transaction at a time - consecutive calls to begin_transaction do nothing
    The same is true of commit_transaction
    '''
    def __init__(self, iterable=None, internal_set=set):
        self._struct = internal_set
        self._set = self._struct()
        if iterable is not None:
            self._set = self._struct(iterable)
        self._lock = False
        self._struct = internal_set

    def begin_transaction(self):
        if not self._lock:
            self._update_lock()

    def commit_transaction(self):
        if self._lock:
            self._update_lock()

    def _update_lock(self):
        self._lock = not self._lock
        if self._lock:
            self._transaction = [self._struct(), self._struct()]
        else:
            apply_set_diffs(self._set, *self._transaction)
            self._transaction = None

    def add(self, value):
        if not self._lock:
            self._set.add(value)
        else:
            if value not in self._set:
                self._transaction[0].add(value)
            self._transaction[1].discard(value)

    def discard(self, value):
        if not self._lock:
            self._set.discard(value)
        else:
            if value in self._set:
                self._transaction[1].add(value)
            self._transaction[0].discard(value)

    def __contains__(self, value):
        if not self._lock:
            return value in self._set
        else:
            return (value in self._transaction[0]
                or value in self._set and not value in self._transaction[1])

    def __len__(self):
        if not self._lock:
            return len(self._set)
        else:
            return len(self._set) + sum(map(len, self._transaction))

    def __iter__(self):
        if not self._lock:
            return iter(self._set)
        else:
            snapshot = self._struct(self._set)
            apply_set_diffs(snapshot, *self._transaction)
            return iter(snapshot)

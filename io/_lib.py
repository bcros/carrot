import os
import errno
import shutil


def blank(file):
    '''Creates a blank (empty) file, or if one exists, overwrites it with a blank file.'''
    with open(file, 'w') as f:
        f.write("")


def ensure_file(file):
    '''Ensures a file exists, but does not modify it.'''
    with open(file, 'a') as f:
        pass


def mkdir(path):
    '''
    Tries to make the directories necessary for the given path.
    Raises any errors that are not EEXIST
    '''
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def rel_path(__file__):
    '''
    Returns the directory containing the script this command is called from.
    You should always pass in __file__ from the script.
    '''
    return os.path.dirname(os.path.realpath(__file__))


def rm(file):
    '''Remove a file'''
    os.remove(file)


def rmdir(path):
    '''
    Tries to remove a directory, regardless of its contents.
    Raises any errors that are not ENOENT
    '''
    try:
        shutil.rmtree(path)
    except OSError as exception:
        if exception.errno != errno.ENOENT:
            raise

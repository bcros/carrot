from contextlib import contextmanager


@contextmanager
def list_open(filename):
    '''
    Open the file as a list of strings.
    Modifications to the list are saved once the context is lost.
    '''
    with open(filename, 'r') as f:
        data = f.read()

    lines = data.split("\n")
    original = lines[:]  # If the file is large, we don't want to force re-write unless something changes
    yield lines

    if lines != original:
        with open(filename, 'w') as f:
            for line in lines:
                f.write("%s\n" % line)

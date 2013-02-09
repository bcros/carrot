import re


def replace(string, replacements):
    """
    replacements:: dict of old:new replacements.

    Because dictionaries are unordered, all replacements are
    applied at once.  Longer replacements take precedence.

    Example:
    replacements = {
        'swap': 'swapped',
        'd': '___',
        'dict': 'dictionary',
        'dictionary': 'dict'}
    string = 'swap dict with dictionary'
    print replace(string, replacements)
    # prints 'swapped dictionary with dict'
    # notice that even though 'd' could have been replaced with '___'
    # it wasn't, because a longer match was made instead.
    """
    keys = sorted(replacements.keys(), key=len, reverse=True)
    joined_keys = "|".join(map(re.escape, keys))

    pattern = re.compile("(%s)" % joined_keys)
    repl = lambda m: replacements[m.group()]

    return pattern.sub(repl, string)

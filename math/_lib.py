

def clamp(val, L1, L2):
    """Clamps val between (inclusive) L1, L2"""
    low, high = min(L1, L2), max(L1, L2)
    val = min(val, high)
    val = max(val, low)
    return val


def gcd(n, m):
    """n, m are positive ints"""
    n = int(abs(n))
    m = int(abs(m))
    while m:
        n, m = m, n % m
    return n


def lerp(a, b, t):
    """Standard lerp from a to b"""
    return a + float(t) * (b - a)


def wrap(val, L1, L2):
    """Returns the wrapped integer in [min(L1, L2), max(L1, L2)]"""
    val, L1, L2 = int(val), int(L1), int(L2)
    low, high = min(L1, L2), max(L1, L2)
    nlow = -low
    return ((val + nlow) % (high + nlow)) - nlow

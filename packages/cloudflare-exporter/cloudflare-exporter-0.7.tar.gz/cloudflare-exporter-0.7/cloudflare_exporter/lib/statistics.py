# TODO: Use statistics.quantiles with python 3.8
# From https://github.com/python/cpython/blob/3.8/Lib/statistics.py
def quantiles(data, *, n=10, method='exclusive'):
    """Divide *data* into *n* continuous intervals with equal probability.
    Returns a list of (n - 1) cut points separating the intervals.
    Set *n* to 4 for quartiles (the default).  Set *n* to 10 for deciles.
    Set *n* to 100 for percentiles which gives the 99 cuts points that
    separate *data* in to 100 equal sized groups.
    The *data* can be any iterable containing sample.
    The cut points are linearly interpolated between data points.
    If *method* is set to *inclusive*, *data* is treated as population
    data.  The minimum value is treated as the 0th percentile and the
    maximum value is treated as the 100th percentile.
    """
    if n < 1:
        raise ValueError('n must be at least 1')
    data = sorted(data)
    ld = len(data)
    if ld < 2:
        raise ValueError('must have at least two data points')
    if method == 'inclusive':
        m = ld - 1
        result = []
        for i in range(1, n):
            j = i * m // n
            delta = i * m - j * n
            interpolated = (data[j] * (n - delta) + data[j + 1] * delta) / n
            result.append(interpolated)
        return result
    if method == 'exclusive':
        m = ld + 1
        result = []
        for i in range(1, n):
            j = i * m // n  # rescale i to m/n
            j = 1 if j < 1 else ld - 1 if j > ld - 1 else j  # clamp to 1 .. ld-1
            delta = i * m - j * n  # exact integer math
            interpolated = (data[j - 1] * (n - delta) + data[j] * delta) / n
            result.append(interpolated)
        return result
    raise ValueError(f'Unknown method: {method!r}')

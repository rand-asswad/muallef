from numpy import array as nparray


def array_difference(array, direction=None, numpy=False):
    diff = []
    a = array[0]
    for i in range(1, len(array)):
        b = array[i]
        diff.append(b - a)
        a = b
    dir = direction.lower() if direction else None
    if dir == 'forward':
        diff.append(0)
    elif dir == 'backward':
        diff.insert(0, 0)
    if numpy:
        return nparray(diff)
    return diff

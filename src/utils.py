from numpy import array as nparray
from matplotlib import pyplot as plt
from subprocess import call
from threading import Thread


def array_difference(array, direction=None, numpy=False):
    """
    Fuction that returns array of differences of consecutive elements in an array
    :param array: an array-like object
    :param direction: value in ('forward'|'backward'|None)
    :param numpy: boolean value to determine return type as python list or numpy array
    :return: array of differences
    """
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


def play_wav(filename):
    """
    Plays wave file in a new thread
    :param filename: wave file path
    """
    p = Thread(target=call, args=(['aplay', filename], ))
    p.setName("play:" + filename)
    p.start()


def plot_step_function(x, y, where='post'):
    """
    Plots piecewise constant function with no vertical line segments.
    An alternative function for pyplot.step()
    :param x: an array-like object containing x coordinates
    :param y: an array-like object containing y coordinates
    :param where: values in ('post'|'pre'|'mid') - default: 'post'
    """
    for i in range(len(x)-1):
        y_seg = None
        if where == 'post':
            y_seg = [y[i]] * 2
        elif where == 'pre':
            y_seg = [y[i+1]] * 2
        elif where == 'mid':
            y_seg = [(y[i] + y[i+1]) / 2] * 2
        plt.plot([x[i], x[i+1]], y_seg, 'r')

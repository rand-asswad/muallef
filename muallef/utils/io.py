from subprocess import call
from threading import Thread
from scipy.io import wavfile
from matplotlib import pyplot as plt
import numpy as np

def read_wav(inputFile):
    fs, data = wavfile.read(inputFile)
    return data.astype(float), fs


def play_wav(inputFile):
    """Plays wave file in a new thread
    :param inputFile: wave file path
    """
    p = Thread(target=call, args=(['aplay', inputFile], ))
    p.setName("play:" + inputFile)
    p.start()


def plot_step_function(x, y, where='post', color='b'):
    """
    Plots piecewise constant function with no vertical line segments.
    An alternative function for pyplot.step()
    :param x: an array-like object containing x coordinates
    :param y: an array-like object containing y coordinates
    :param where: values in ('post'|'pre'|'mid') - default: 'post'
    :param color: default blue
    """
    for i in range(len(x)-1):
        y_seg = None
        if where == 'post':
            y_seg = [y[i]] * 2
        elif where == 'pre':
            y_seg = [y[i+1]] * 2
        elif where == 'mid':
            y_seg = [(y[i] + y[i+1]) / 2] * 2
        plt.plot([x[i], x[i+1]], y_seg, color)

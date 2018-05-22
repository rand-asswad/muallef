from os import path, remove
from tempfile import mkstemp
from subprocess import call
from threading import Thread

from matplotlib import pyplot as plt
from scipy.io import wavfile
from pydub import AudioSegment


def read_audio(file_path):
    file, ext = path.splitext(file_path)
    sound = AudioSegment.from_file(file_path, ext[1:])
    if ext == ".wav":
        tmp = None
        wav = file_path
    else:
        _, tmp = mkstemp()
        sound.export(tmp, format="wav")
        wav = tmp
    fs, data = wavfile.read(wav)
    if tmp:
        remove(tmp)
    return fs, data


def play_audio(file_path):
    """Plays audio file in a new thread
    :param file_path: audio file path
    :return thread
    """
    p = Thread(target=call, args=(['aplay', file_path], ))
    p.setName("play:" + file_path)
    p.start()
    return p


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
            y_seg = [(y[i] + y[i+1]) / 2.0] * 2
        plt.plot([x[i], x[i+1]], y_seg, color)

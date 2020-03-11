from os import path, remove
from tempfile import mkstemp
from subprocess import call
from threading import Thread

import numpy as np
from scipy.io import wavfile
from pydub import AudioSegment

import warnings
warnings.filterwarnings('ignore')


class AudioLoader(object):
    """
    class source for reading an audio file
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.sampleRate, data = read_audio(file_path)
        signal = data if data.ndim == 1 else data[:, 0]
        self.signal = signal.astype(dtype=float)
        self.size = self.signal.size
        self.duration = self.size / float(self.sampleRate)
        self.player = None

    def time(self, n_samples=None):
        if n_samples:
            return np.linspace(0, self.duration, n_samples, endpoint=False)
        return np.arange(self.size) / float(self.sampleRate)
        #if not n_samples:
        #    n_samples = self.size
        #return np.arange(n_samples) / float(self.sampleRate)
        #return np.arange(n_samples) * (self.duration / float(self.sampleRate))

    def cut(self, start=None, stop=None):
        start_f = int(start * self.sampleRate) if start else 0
        stop_f = int(stop * self.sampleRate) if stop else self.size
        self.signal = self.signal[start_f:stop_f]
        self.size = self.signal.size
        self.duration = self.size / float(self.sampleRate)

    def play(self):
        self.player = play_audio(self.file_path)


def read_audio(file_path):
    file, ext = path.splitext(file_path)
    sound = AudioSegment.from_file(file_path, ext[1:])
    # convert to wav
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
    # convert to mono-channel
    if data.ndim > 1:
        n_channels = data.shape[1]
        data = data.sum(axis=1) / n_channels
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

import numpy as np
from muallef.utils.io import read_audio, play_audio


class source(object):
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

    def get_time(self, n_samples=None):
        if not n_samples:
            n_samples = self.size
        #return np.arange(n_samples) / float(self.sampleRate)
        n_ratio = self.duration / float(n_samples)
        return np.arange(n_samples) * n_ratio

    def cut(self, start=None, stop=None):
        start_f = int(start * self.sampleRate) if start else 0
        stop_f = int(stop * self.sampleRate) if stop else self.size
        self.signal = self.signal[start_f:stop_f]
        self.size = self.signal.size
        self.duration = self.size / float(self.sampleRate)

    def play(self):
        thread = play_audio(self.file_path)

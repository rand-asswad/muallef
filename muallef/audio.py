from os import path, remove
from tempfile import mkstemp
from scipy.io import wavfile
import numpy as np
from pydub import AudioSegment


class source(object):
    """
    class source for reading an audio file
    """
    def __init__(self, file_path):
        self.sampleRate, data = read_file(file_path)
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


def read_file(file_path):
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


__all__ = ["source"]
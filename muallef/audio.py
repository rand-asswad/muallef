from os import path, remove
from tempfile import mkstemp
from scipy.io import wavfile
import numpy as np
from pydub import AudioSegment as seg


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
        samples = np.arange(start=0, stop=n_samples, dtype=float)
        return samples / float(self.sampleRate)


def read_file(file_path):
    file, ext = path.splitext(file_path)
    sound = seg.from_file(file_path, ext[1:])
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
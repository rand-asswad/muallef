from abc import ABC, abstractmethod
from itertools import zip_longest
import numpy as np

from aubio import pitch as aubiopitch
from muallef.pitch.klapuri import PitchKlapuri


class Pitch(ABC):
    def __init__(self, signal, sampleRate, frameSize=2048, fftBins=4096):
        self.signal = signal
        self.sampleRate = sampleRate
        self.frameSize = frameSize
        self.fftSize = fftBins

    def __call__(self, signal=None):
        if signal is not None:
            return self._func(signal)
        pitch = []
        start, stop = 0, self.frameSize
        while stop <= self.signal.size:
            f0 = self._func(self.signal[start:stop])
            pitch.append(f0)
            start, stop = stop, stop + self.frameSize
        return np.array(pitch)

    @abstractmethod
    def _func(self, signal):
        return 0


class MonoPitch(Pitch):
    def __init__(self, signal, sampleRate, frameSize=2048, fftBins=4096, method='yinfft'):
        signal = signal.astype(np.float32)
        self.method = method.lower()
        if self.method not in ['yinfft', 'yin']:
            raise ValueError("Unsupported method: try 'yinfft' or 'yin'")
        super().__init__(signal, sampleRate, frameSize, fftBins)
        self._aubio = aubiopitch(self.method, self.fftSize,
                                 self.frameSize, self.sampleRate)
        self._aubio.set_unit('Hz')
        self._aubio.set_tolerance(0.8)
        self.confidence = []
    
    def __call__(self, signal=None):
        f0 = super().__call__(signal)
        self.confidence = np.asarray(self.confidence)
        if self.method == 'yinfft':
            self.confidence = self.confidence.max() - self.confidence
            self.confidence /= self.confidence.max()
        return f0

    def _func(self, signal):
        pitch = self._aubio(signal)[0]
        self.confidence.append(self._aubio.get_confidence())
        return pitch


class MultiPitch(Pitch):
    def __init__(self, signal, sampleRate, frameSize=2048, fftBins=4096, method='klapuri', **kwargs):
        super().__init__(signal, sampleRate, frameSize, fftBins)
        self.estimate_f0 = None
        method = method.lower()
        if method == 'klapuri':
            poly = kwargs.pop('max_polyphony', 6)
            self.estimate_f0 = PitchKlapuri(max_poly=poly)
        else:
            raise ValueError("Unsupported method: try 'klapuri'")

    def __call__(self, signal=None):
        f0 = self.estimate_f0(self.signal, self.sampleRate)
        return np.array(list(zip_longest(*f0, fillvalue=np.nan)))

    def _func(self, signal):
        return []

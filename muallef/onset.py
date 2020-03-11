import essentia
essentia.log.infoActive = False                  # deactivate the info level
essentia.log.warningActive = False               # deactivate the warning level
essentia.log.debugLevels -= essentia.EAll        # deactivate all debug modules
import essentia.standard as es

import numpy as np


class Onset(object):
    def __init__(self, signal, sampleRate, frameSize=1024,
                 hopSize=512, method='complex', window='hann'):
        self.signal = signal.astype(np.float32)
        self.sampleRate = sampleRate
        self.frameSize = frameSize
        self.hopSize = hopSize

        self.calcOnsetFunc = es.OnsetDetection(method=method)
        self.window = es.Windowing(type=window)

    def __call__(self):
        self.calculate_function()
        return self.find_peaks()

    def calculate_function(self):
        onset_func = []
        fft = es.FFT()
        c2p = es.CartesianToPolar()
        for frame in es.FrameGenerator(self.signal,
                                       frameSize=self.frameSize, hopSize=self.hopSize):
            mag, phase, = c2p(fft(self.window(frame)))
            onset_func.append(self.calcOnsetFunc(mag, phase))
        self.onsetFunction = np.array(onset_func, dtype=np.float32)
        self.onsetTime = np.arange(len(onset_func)) * (self.hopSize / self.sampleRate)

    def find_peaks(self):
        getOnsets = es.Onsets()
        self.onsets = np.array(getOnsets(np.array([self.onsetFunction]), [1]))
        return self.onsets

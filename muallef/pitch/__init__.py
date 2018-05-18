from muallef.utils import units
from . import yin, yinfft
import numpy as np

__name__ = "muallef.pitch"
__package__ = "muallef.pitch"


def detect(signal, sampleRate, bufferSize=2048, unit='Hz', method='yin', timeUnit='frames', tolerance=None):
    """Pitch detect function returns pitch and time.
    :param signal: input signal as numpy array
    :param sampleRate: signal sample rate
    :param bufferSize: number of samples per frame
    :param unit: pitch output unit.
        {Hz, MIDI} - default: "Hz"
    :param method: pitch detection method.
        {yin, yinfft} - default: "yin"
    :param timeUnit: time output unit.
        {frames, samples, seconds} - default: "frames"
    :param tolerance: detection error tolerance value in [0,1]
        if not set, a value is set by default depending on method
    :return: tuple (time, pitch)
        time: numpy array of time in timeUnit
        pitch: numpy array of pitch values in unit
    """

    #raise value errors for invalid parameters
    if method == 'yin':
        get_pitch = yin.yin_detect
        if not tolerance:
            tolerance = 0.15
        kwargs = dict(tolerance=tolerance)
    elif method == 'yinfft':
        get_pitch = yinfft.yinfft_detect
        w = yinfft.spectral_weights(bufferSize, sampleRate)
        if not tolerance:
            tolerance = 0.85
        kwargs = dict(sampleRate=sampleRate, weight=w, tolerance=tolerance)
    else:
        raise ValueError("Method not found")

    pitch = []
    time = []
    t = 0
    start, stop = 0, bufferSize
    while stop <= signal.size:
        buffer = signal[start:stop]
        p = get_pitch(buffer, **kwargs)
        if p > 0:
            p = sampleRate / p
        pitch.append(p)
        time.append(t)
        start, stop = stop, stop + bufferSize
        t += 1

    time = units.convertTime(np.array(time), fromUnit="frames", to=timeUnit)
    pitch = units.convertFreq(np.array(pitch), fromUnit="hz", to=unit)

    return time, pitch


#__all__ = ['detect']

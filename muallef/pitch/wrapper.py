from muallef.util import units, normalize
from muallef.pitch import yin, yinfft
import numpy as np

from aubio import pitch as aubiopitch
from essentia.standard import PitchYin


def get_pitch(signal, sampleRate, bufferSize=2048, unit='Hz', method='yinfft',
                 timeUnit='seconds', tolerance=None, confidence=0.5):
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
        func = yin.yin_detect
        if not tolerance:
            tolerance = 0.15
        kwargs = dict(tolerance=tolerance)
    elif method == 'yinfft':
        func = yinfft.yinfft_detect
        w = yinfft.spectral_weights(bufferSize, sampleRate)
        if not tolerance:
            tolerance = 0.9
        kwargs = dict(sampleRate=sampleRate, weight=w, tolerance=tolerance)
    elif method == 'aubio':
        pitch_obj = aubiopitch('yin', bufferSize, bufferSize, sampleRate)
        pitch_obj.set_unit('Hz')
        pitch_obj.set_tolerance(0.8)
        kwargs = {}
        def func(window, **kwargs):
            pitch = pitch_obj(window.astype(np.float32))[0]
            return pitch, pitch_obj.get_confidence()
    elif method == 'essentia':
        pitch_obj = PitchYin(frameSize=bufferSize, sampleRate=sampleRate)
        kwargs = {}
        def func(window, **kwargs):
            return pitch_obj(window)
    else:
        raise ValueError("Method not found")

    pitch = []
    conf = []
    start, stop = 0, bufferSize
    while stop <= signal.size:
        buffer = signal[start:stop]
        p, c = func(buffer, **kwargs)
        if p > 0 and method not in ['aubio', 'essentia']:
            p = sampleRate / p
        pitch.append(p)
        conf.append(c)
        start, stop = stop, stop + bufferSize

    pitch = units.convertFreq(np.array(pitch), fromUnit="hz", to=unit)

    # process confidence values
    #conf = np.power(conf, 3)
    conf = normalize(np.array(conf))
    conf[conf <= confidence] = 0

    if timeUnit == "frames":
        time = np.arange(pitch.size)
    elif timeUnit == "samples":
        time = np.arange(pitch.size) * bufferSize
    elif timeUnit == "seconds":
        time = np.arange(pitch.size) * (bufferSize / float(sampleRate))
    else:
        raise ValueError("Time unit not valid")

    return time, pitch, conf

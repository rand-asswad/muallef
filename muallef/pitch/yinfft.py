from muallef.utils import math
from muallef.utils.units import dB_to_power
from scipy.signal import hann
import numpy as np

freqsMask = [
    0.,    20.,    25.,   31.5,    40.,    50.,    63.,    80.,   100.,   125.,
    160.,   200.,   250.,   315.,   400.,   500.,   630.,   800.,  1000.,  1250.,
    1600.,  2000.,  2500.,  3150.,  4000.,  5000.,  6300.,  8000.,  9000., 10000.,
    12500., 15000., 20000., 25100
]

weightMask = [
    -75.8,  -70.1,  -60.8,  -52.1,  -44.2,  -37.5,  -31.3,  -25.6,  -20.9,  -16.5,
    -12.6,  -9.60,  -7.00,  -4.70,  -3.00,  -1.80,  -0.80,  -0.20,  -0.00,   0.50,
    1.60,   3.20,   5.40,   7.80,   8.10,   5.30,  -2.40,  -11.1,  -12.8,  -12.2,
    -7.40,  -17.8,  -17.8,  -17.8
]


def yinfft_detect(signal, sampleRate, weight, tolerance=0.85):
    length = signal.size
    half = int(length // 2)

    windowed_signal = np.multiply(signal, hann(signal.size, sym=False))
    re, im = math.fft_parts(windowed_signal)
    im = np.append(im, 0)

    # square magnitude of the spectrum, with applied weights, and calculate its sum
    #weight = spectral_weights(length, sampleRate)
    first = re[0] * re[0] * weight[0]
    tmp = np.power(re[1:], 2) + np.power(im, 2)
    tmp = np.multiply(tmp, weight[1:])
    mid = tmp[-1]
    np.delete(tmp, -1)
    sqr_mag = np.append(np.append(first, tmp), np.append(mid, tmp[::-1]))
    s = np.sum(sqr_mag) * 2.0

    # calculate the fft of the squared magnitude
    fftout = math.fft_tail(sqr_mag)
    yin = np.zeros(half + 1, dtype=float)
    yin[0] = 1
    tmp = 0
    for tau in range(1, yin.size):
        # compute the square differences
        yin[tau] = s - fftout[tau]
        # compute the cumulative mean normalized difference function
        tmp += yin[tau]
        if tmp != 0:
            yin[tau] *= tau / tmp
        else:
            yin[tau] = 1

    # find best candidates
    tau = np.argmin(yin)
    short_period = int(round(sampleRate / 1300.0))
    if yin[tau] < tolerance:
        if tau > short_period:
            peak_position = tau
            pitch = math.quadratic_peak_position(yin, tau)
        else:
            half_period = int(tau / 2.0 + 0.5)
            peak_position = half_period if yin[half_period] < tolerance else tau
            pitch = math.quadratic_peak_position(yin, peak_position)
    else:
        peak_position = 0
        pitch = 0.0
    # get pitch confidence
    confidence = 1.0 - yin[peak_position]
    return pitch, confidence


def spectral_weights(bufferSize, sampleRate):
    weight = np.zeros(int(bufferSize / 2) + 1)
    j = 1
    factor = (1.0 / float(bufferSize)) * sampleRate
    for i in range(weight.size):
        freq = i * factor
        while freq > freqsMask[j]:
            j += 1
        a0, a1 = float(weightMask[j - 1]), float(weightMask[j])
        f0, f1 = float(freqsMask[j - 1]), float(freqsMask[j])
        if f0 == 0:
            weight[i] = (a1 - a0) / f1 * freq + a0
        else:
            weight[i] = (a1 - a0) / (f1 - f0) * freq + a0 - (a1 - a0) / (f1 / f0 - 1.0)
        while freq > freqsMask[j]:
            j += 1
        weight[i] = dB_to_power(weight[i] / 2.0)
    return weight

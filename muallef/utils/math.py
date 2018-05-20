from scipy.fftpack import rfft
from scipy.signal import get_window
import numpy as np


def quadratic_peak_position(array, position):
    """Finds exact peak index by quadratic interpolation.
    source : Quadratic Interpolation of Spectral Peaks - Julius O. Smith III
    :param array: 1D-vector
    :param position: index of peak in array
    :return: exact peak position of interpolated maximum or minimum
    """
    x, pos = array, position
    if pos == 0 or pos == (x.size - 1):
        return pos
    x0 = pos if pos < 1 else pos - 1
    x2 = pos + 1 if pos < (x.size - 1) else pos

    if x0 == pos:
        return pos if x[pos] <= x[x2] else x2
    if x2 == pos:
        return pos if x[pos] <= x[x0] else x0
    s0, s1, s2 = x[x0], x[pos], x[x2]
    return pos + 0.5 * (s0 - s2) / (s0 - 2*s1 + s2)


def moving_avg(x, windowSize, window="hann"):
    """Apply windowed moving average on data.
    :param x: input signal array
    :param windowSize:
    :param window: window type
    :return: numpy array
    """
    if x.size < windowSize:
        raise ValueError("Input vector has to be larger than the window size.")

    if window == "flat":
        w = np.ones(windowSize, dtype=float)
    elif window in ['boxcar', 'triang', 'blackman', 'hamming', 'hann', 'bartlett']:
        w = get_window(window, windowSize, fftbins=False)
    else:
        raise ValueError("Unknown window type")

    return np.convolve(x, w/np.sum(w), mode='same')


def fft_tail(x, n=None):
    re, im = fft_parts(x, n)
    return np.append(re, im[::-1])


def fft_parts(x, n=None):
    if not n:
        n = len(x)
    z = rfft(x, n)
    re = np.append([z[0]], z[1::2])
    im = z[2::2]
    return re, im

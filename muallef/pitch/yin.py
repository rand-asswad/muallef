import numpy as np
from numpy.linalg import norm
from muallef.util import quadratic_peak_position


def yin_detect(signal, sampleRate, tolerance=0.15):
    N = int(signal.size / 2)
    x = signal[:N]

    # calculate square difference functions
    d = np.array([norm(x[tau:] - np.roll(x, tau)[tau:], ord=2)**2 for tau in range(N)])
    cumusum = np.cumsum(d)
    yin = np.arange(N) * np.divide(d, cumusum)
    yin[0] = 1

    # detect pitch from cumulative sum
    candidates = yin < tolerance
    candidates[0] = candidates[-1] = False
    for tau in np.nonzero(candidates)[0]:
        if yin[tau] < yin[tau + 1]:
            period = quadratic_peak_position(yin, tau)
            f0 = sampleRate / period if period > 0 else 0
            confidence = 1 - yin[tau]
            return f0, confidence

    # get best estimate
    peak_pos = np.argmin(yin)
    period = quadratic_peak_position(yin, peak_pos)
    f0 = sampleRate / period if period > 0 else 0
    confidence = 1 - yin[peak_pos]
    return f0, confidence


def yin_detect_old(signal, tolerance=0.15):
    buffer = int(signal.size / 2)
    yin = np.zeros(buffer, dtype=float)

    cum = 0.0
    for tau in range(1, buffer):
        # calculate difference function
        for i in range(buffer):
            yin[tau] += (signal[i] - signal[i + tau]) ** 2

        # calculate cumulative sum
        cum += yin[tau]
        yin[tau] = yin[tau] * tau / cum if cum else 1

        # detect pitch from cumulative sum
        period = tau - 3
        if tau > 4 and yin[period] < tolerance and yin[period] < yin[period + 1]:
            return quadratic_peak_position(yin, period)

    # get best estimate
    peak_pos = np.argmin(yin)
    return quadratic_peak_position(yin, peak_pos)

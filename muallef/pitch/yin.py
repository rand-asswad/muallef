from muallef.utils import math
import numpy as np


def yin_detect(signal, tolerance=0.15):
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
            return math.quadratic_peak_position(yin, period)

    # get best estimate
    peak_pos = np.argmin(yin)
    return math.quadratic_peak_position(yin, peak_pos), 0.0

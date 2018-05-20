from scipy.signal import stft as calculate_stft
import numpy as np

princarg = lambda phase: ((phase + np.pi) % (-2 * np.pi)) + np.pi
square = lambda x: np.multiply(x, x)


def onset_function(signal, sampleRate, windowSize, overlap=None,
                   method="complex", normalize=False, unit="seconds"):
    """ Onset detection function wrapper.
    :param signal: input signal as numpy array
    :param sampleRate: sample rate of the input signal
    :param windowSize: window size for STFT transform
    :param overlap: STFT overlap size (if None, overlap = windowSize // 2)
    :param method: detection method - default: 'complex'
    :param normalize: normalize into interval [0, 1]
    :param unit: ('seconds'|'samples'|'seconds") - default: 'seconds'
    :return: time, onset function
    """
    # calculate STFT
    if not overlap:
        overlap = windowSize // 2
    stft = calculate_stft(signal, sampleRate, nperseg=windowSize, noverlap=overlap)

    # call proper method
    method = method.lower()
    call = {
        "hfc": high_frequency_content,
        "phase": phase_deviation,
        "complex": complex_distance,
        "hfc-complex": hfc_complex,
    }
    t, odf = call[method](stft)
    t, odf = np.delete(t, -1), np.delete(odf, -1)

    # normalize onset function into [0,1]
    if normalize:
        odf -= odf.min()
        odf /= odf.max()

    # convert time unit
    if unit == "frames":
        time = np.arange(t.size)
    elif unit == "samples":
        time = np.arange(t.size) * (windowSize - overlap)
    elif unit == "seconds":
        time = t
    else:
        raise ValueError("Time unit not valid")

    return time, odf


def high_frequency_content(stft):
    f, t, s = stft
    mag = square(np.abs(s))
    coefs = np.arange(X.shape[0])
    spectral_mag = np.dot(coefs, mag)
    return t, spectral_mag


def phase_deviation(stft):
    f, t, s = stft

    # extract phase from STFT
    phase = np.angle(s)

    # find the second partial derivative of the phase wrt time
    phase_diff2 = np.diff(phase, n=2, axis=-1)

    # calculate princarg of the second derivative
    vfunc = np.vectorize(princarg)
    phase_dev = vfunc(phase_diff2)

    # sum along frequency axis
    odf = np.sum(np.abs(phase_dev), axis=0)
    return t, odf


def complex_distance(stft):
    f, t, s = stft

    # extract phase from STFT
    phase = np.angle(s)

    # find the second partial derivative of the phase wrt time
    phase_diff2 = np.diff(phase, n=2, axis=-1)
    zero_cols = np.zeros((f.size, 2))

    # calculate princarg of the second derivative
    vfunc = np.vectorize(princarg)
    phase_dev = vfunc(phase_diff2)
    phase_dev = np.hstack((phase_dev, zero_cols))

    # generate prediction for the current spectral frame
    mag_dev = np.multiply(np.abs(s), np.exp(1j * phase_dev))

    # distance between measured and predicted
    diff = square(np.abs(mag_dev - s))
    distance = np.sum(diff, axis=0)
    return t, distance


def hfc_complex(stft):
    t, hfc = high_frequency_content(stft)
    t, c = complex_distance(stft)
    return t, np.multiply(hfc, c)

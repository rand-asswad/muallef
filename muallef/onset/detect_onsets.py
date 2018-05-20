from muallef.onset.detection_functions import onset_function
from muallef.onset.peak_picker import peak_pick


def detect_onsets(signal, sampleRate, threshold=0.1, windowSize=2048,
                  overlap=None, unit='frames', method='complex'):
    """Onset points detector that picks peaks from a signal envelope.
    Calls onset.get_envelope()
    :param signal: input signal as numpy array
    :param sampleRate: sample rate of the input signal
    :param threshold: onset function threshold parameter (value in [0,1])
    :param windowSize: window size for STFT transform
    :param overlap: STFT overlap size (if None, overlap = windowSize // 2)
    :param unit: ('frames'|'samples'|'seconds') default is 'frames'
    :param method: ('complex', 'energy') default is 'complex'
    :return: numpy array of detected onset points
    """
    # calculate onset function
    time, odf = onset_function(signal, sampleRate, windowSize, overlap=overlap,
                               method=method, normalize=True, unit=unit)

    # select peak indices
    onsets = peak_pick(onset_function, threshold)

    return time[onsets]

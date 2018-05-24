import numpy as np
from muallef.utils.math import normalize
from muallef.pitch import detect as detect_pitch
from muallef.onset import detect as detect_onsets


def detect_notes(signal, sampleRate, bufferSize=2048, overlap=None,
                 unit="seconds", pitchMethod="yinfft", onsetMethod="complex",
                 onsetThreshold=0.02, confidenceThreshold=0.5, localThreshold=0.7):
    """Detects notes in a signal.
    :param signal: input signal as numpy array
    :param sampleRate: sample rate of the input signal
    :param bufferSize: buffer size for detecting pitch and onsets
    :param overlap: overlap size for STFT
    :param unit: time output unit (frames, samples, or seconds)
    :param pitchMethod: yinfft or yin
    :param onsetMethod: ...
    :param onsetThreshold: onset threshold for peak selection (value in [0,1])
    :param confidenceThreshold: pitch confidence threshold (value in [0,1])
    :param localThreshold: pitch confidence threshold in interval (value in [0,1])
    :return: (onsets, notes)
        onsets: onset time in :param unit
        notes: corresponding notes (midi)
    """
    # detect pitch
    time, pitch, confidence = detect_pitch(signal, sampleRate, bufferSize=bufferSize,
                             unit="midi", method=pitchMethod, timeUnit=unit,
                             tolerance=None, confidence=confidenceThreshold)
    pitch = np.rint(pitch)

    # detect onsets
    if not overlap:
        overlap = int(0.75 * bufferSize)
    onsets = detect_onsets(signal, sampleRate, threshold=onsetThreshold,
                           windowSize=bufferSize, overlap=overlap,
                           unit=unit, method=onsetMethod)

    # synchronize onset with pitch time axis
    onsets_indices = get_onset_indices(time, onsets)

    # call note detector
    onsets, notes = detect_notes_core(time, pitch, confidence, onsets_indices, localThreshold)

    return onsets, notes


def detect_notes_core(time, pitch, confidence, onsets, threshold=0.5):
    notes = np.zeros(onsets.shape, dtype=pitch.dtype)
    i = 0
    for j in range(1, len(onsets)):
        pitch_buffer = pitch[onsets[i]:onsets[j]]
        conf_buffer = confidence[onsets[i]:onsets[j]]
        notes[i] = segment_pitch(pitch_buffer, conf_buffer, threshold)
        i = j
    return time[onsets], notes


def get_onset_indices(time_array, onsets):
    onsets_indices = [np.abs(time_array - o).argmin() for o in onsets]
    return np.array(onsets_indices)


def segment_pitch(pitch, conf, threshold):
    # take first half of pitch
    if pitch.size > 1:
        size = pitch.size // 2
        pitch = pitch[:size]
        conf = conf[:size]

    # normalize confidence
    conf = normalize(conf)

    # select pitches with high confidence
    if conf.any():
        index = np.where(conf > threshold)
        pitch = pitch[index]
        conf = conf[index]
        if conf.any():
            return int(round(np.average(pitch, weights=conf)))
    return -1

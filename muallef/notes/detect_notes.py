import numpy as np
from muallef.utils.math import normalize


def detect_notes(pitch_array, onsets):
    time, pitch, confidence = pitch_array
    onsets = get_onsets(time, onsets)

    notes = np.zeros(onsets.shape, dtype=pitch.dtype)
    i = 0
    for j in range(1, len(onsets)):
        pitch_buffer = pitch[onsets[i]:onsets[j]]
        conf_buffer = confidence[onsets[i]:onsets[j]]
        notes[i] = segment_pitch(pitch_buffer, conf_buffer, 0.7)
        i = j
    return time[onsets], notes


def get_onsets(time_array, onsets):
    onsets = [np.abs(time_array - o).argmin() for o in onsets]
    return np.array(onsets)


def segment_pitch(pitch, conf, threshold=0.5):
    # take first half of pitch
    if pitch.size > 1:
        size = pitch.size // 2
        pitch = pitch[:size]
        conf = conf[:size]

    # normalize confidence
    if conf.any():
        conf = normalize(conf)
        index = np.where(conf > threshold)
        pitch = pitch[index]
        conf = conf[index]
        if conf.any():
            return np.average(pitch, weights=conf)
    return -1

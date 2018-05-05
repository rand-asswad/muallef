import numpy as np
from numpy.linalg import norm

from .notes import sci_pitch

C_major = np.array([1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=bool)
sharp_indices = [6, 1, 8, 3, 10, 5, 0]
flat_indices = [10, 3, 8, 1, 6, 11, 4]


class Scale(object):
    def __init__(self, note_index, type='major'):
        self.base_note = note_index
        self.vect = np.array(shift_array(C_major, note_index), dtype=bool)

    def __str__(self):
        sig = self.scale_signature()
        tone = ""
        if sig[1] == "sharp":
            tone = " #"
        elif sig[1] != "none":
            tone = " ♭"
        output = "Key signature: " + str(sig[0]) + tone
        return output

    def scale_signature(self):
        sharps = 0
        while self.vect[sharp_indices[sharps]]:
            sharps += 1
            if sharps == 7:
                break
        flats = 0
        while self.vect[flat_indices[flats]]:
            flats += 1
            if flats == 7:
                break
        if sharps or flats:
            if not flats:
                tone = "sharp"
                number = sharps
            elif not sharps:
                tone = "flat"
                number = flats
            else:
                if sharps < flats:
                    tone = "sharps"
                    number = sharps
                elif sharps == flats:
                    tone = "same"
                    number = 6
                else:
                    tone = "flats"
                    number = flats
        else:
            tone = "none"
            number = 0
        return number, tone


def find_scale(part_vect):
    d = np.array([norm(s.vect-part_vect) for s in scales], dtype=float)
    #index = d.argsort()
    #order = np.array(scales)[index]:
    return scales[int(np.argmin(d))]


def shift_array(arr, index):
    n = len(arr)
    result = [0] * n
    result[index:] = arr[:n - index]
    result[:index] = arr[n - index:]
    return result


scales = [Scale(i) for i in range(12)]

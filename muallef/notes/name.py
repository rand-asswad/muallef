import numpy as np
from . import scale


def note_name(midi, tone, name_system="solfege"):
    if midi <= 0:
        return "S"
    note = int(midi) % 12
    octave = midi // 12
    name_system = name_system.lower()
    if name_system == "scientific":
        return sci_name[note] + str(octave)
    if name_system == "solfege":
        name = solfege_name
    elif name_system == "alphabet":
        name = alpha_name
    else:
        raise ValueError("Name system not valid")
    return octave_note_name(note, tone, name_system=name) + str(octave)


sci_name = ['C', 'C#/D♭', 'D', 'D#/E♭', 'E', 'F', 'F#/G♭', 'G', 'G#/A♭', 'A', 'A#/B♭', 'B']

alpha_name = {
    0: 'C',
    2: 'D',
    4: 'E',
    5: 'F',
    7: 'G',
    9: 'A',
    11: 'B',
}

solfege_name = {
    0: 'Do',
    2: 'Re',
    4: 'Mi',
    5: 'Fa',
    7: 'Sol',
    9: 'La',
    11: 'Si',
}
_sharp = "#"
_flat = "♭"


def octave_note_name(note, tone, name_system=solfege_name):
    if scale.C_major[note]:
        return name_system[note]
    if tone == -1:
        sym = name_system[note + 1] + _flat
    else:
        sym = name_system[note - 1] + _sharp
    return sym



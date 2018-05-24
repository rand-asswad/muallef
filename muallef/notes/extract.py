import numpy as np
from midiutil.MidiFile import MIDIFile
from muallef.notes.tempo import detect_tempo


def extract_midi(time, notes, output_file):
    tempo, notes = detect_tempo(time, notes)
    notes = np.rint(notes).astype(dtype=int)
    #tempo = tempo.astype(dtype=int)
    time = np.delete(np.insert(np.cumsum(tempo), 0, 0), -1)
    if len(notes) != len(tempo) or len(tempo) != len(time):
        raise Exception('Dimension error')

    midi = MIDIFile(1)
    midi.addTempo(track=0, time=time[0], tempo=120)

    silence = np.argwhere(notes > 0).squeeze()
    time = time[silence]
    tempo = tempo[silence]
    notes = notes[silence]

    for i in range(len(notes)):
        midi.addNote(track=0, channel=0, pitch=notes[i], time=time[i], duration=tempo[i], volume=100)

    with open(output_file, "wb") as midi_out:
        midi.writeFile(midi_out)
import numpy as np
from midiutil.MidiFile import MIDIFile
from muallef.notes.tempo import detect_tempo


def extract_midi(time, notes, output_file):
    tempo, notes = detect_tempo(time, notes)
    notes = np.rint(notes).astype(dtype=int)
    #time = np.delete(np.insert(np.cumsum(tempo), 0, 0), -1)
    tempo = tempo.astype(dtype=int)

    mf = MIDIFile(1)
    track = 0
    time = 0
    mf.addTrackName(track, time, "Name")
    mf.addTempo(track, time, 120)

    channel = 0
    volume = 100

    for i in range(len(notes)):
        mf.addNote(track, channel, pitch=notes[i], time=time, duration=tempo[i], volume=100)
        time = time + tempo[i]

    with open(output_file, "wb") as out:
        mf.writeFile(out)
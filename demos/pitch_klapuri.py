import sys
from os import path
project_root = path.abspath(path.join(path.dirname(path.abspath(__file__)), '..'))
sys.path.append(project_root)

from muallef.io import AudioLoader
from muallef.pitch import MultiPitch
from muallef.util.units import Hz_to_MIDI

import numpy as np
import matplotlib.pyplot as plt

# matplotlib options
from matplotlib import rcParams
rcParams['savefig.transparent'] = True
rcParams['text.usetex'] = True


def demo_klapuri(audio):
    fs = audio.sampleRate
    x = audio.signal
    frameSize = 2048

    klapuri = MultiPitch(x, fs, method='klapuri', frameSize=frameSize)
    pitch = Hz_to_MIDI(klapuri())
    time = np.arange(pitch.shape[1]) * (frameSize / fs)

    fig, ax = plt.subplots()
    fig.suptitle("Multi-pitch estimation using Klapuri's iterative method", fontsize=16)
    ax.set_title("Piano roll of Beethoven's \"Für Elise\"")
    for m in range(pitch.shape[0]):
        ax.scatter(time, pitch[m])
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Pitch (MIDI)')
    ax.set_ylim(20, 109)
    plt.show()


if __name__ == '__main__':
    if len(sys.argv) > 3:
        print("Wrong number of arguments", file=sys.stderr)
        print("Usage: python %s [filename] [duration_in_seconds]" % sys.argv[0], file=sys.stderr)
        sys.exit(1)
    elif len(sys.argv) > 1:
        audio_file = sys.argv[1]
        audio = AudioLoader(audio_file)
        if len(sys.argv) == 3:
            audio.cut(stop=sys.argv[2])
    else:
        audio_file = "../samples/polyphonic/furElise.wav"
        audio = AudioLoader(audio_file)
        audio.cut(stop=10)
        print("Using first ", 10, " seconds of ", audio_file)
    
    demo_klapuri(audio)

import sys
from os import path
project_root = path.abspath(path.join(path.dirname(path.abspath(__file__)), '..'))
sys.path.append(project_root)

from muallef.io import AudioLoader
from muallef.onset import Onset

import numpy as np
import matplotlib.pyplot as plt

# matplotlib options
from matplotlib import rcParams
rcParams['savefig.transparent'] = True
rcParams['text.usetex'] = True

method = {
    'HFC': 'hfc',
    'Complex': 'complex',
    'Phase Deviation': 'complex_phase',
}


def plot_odf(audio):
    fs = audio.sampleRate
    x = audio.signal
    t = audio.time()

    fig, ax = plt.subplots(len(method)+1, 1, sharex=True)
    i = 0
    ax[i].plot(t, x)
    ax[i].yaxis.set_ticklabels([])
    ax[i].set_ylabel("Signal")
    for key in method.keys():
        i += 1
        onset = Onset(x, fs, method=method[key])
        onsets = onset()
        ax[i].plot(onset.onsetTime, onset.onsetFunction)
        ax[i].yaxis.set_ticklabels([])
        ax[i].set_ylabel(key)

    ax[-1].set_xlabel('Time (s)')
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
    
    plot_odf(audio)

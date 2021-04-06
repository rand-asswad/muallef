import sys
from os import path
project_root = path.abspath(path.join(path.dirname(path.abspath(__file__)), '..'))
sys.path.append(project_root)

from muallef.io import AudioLoader
from muallef.pitch import MonoPitch
from muallef.onset import Onset
from muallef.util.units import convertFreq, Hz_to_MIDI
from muallef.util import normalize

from matplotlib import pyplot as plt
from sys import argv
import numpy as np


def demo_yin(audio):
    fs = audio.sampleRate
    x = audio.signal

    yin = MonoPitch(x, fs, method='yin')
    yin_f0 = yin()
    yin_conf = yin.get_confidence(normalize=True)
    yinfft = MonoPitch(x, fs, method='yinfft')
    yinfft_f0 = yinfft()
    yinfft_conf = yinfft.get_confidence(normalize=True)
    time = audio.time(len(yin_f0))

    fig, ax = plt.subplots()
    ax.scatter(time, yinfft_f0, c='red', s=10*yinfft_conf)
    ax.scatter(time, yin_f0, c='blue', s=10*yin_conf)
    _ = ax.set_ylim(0, 2000)

    #f0 = MonoPitch(x, fs, method='yinfft')()
    #pitch = Hz_to_MIDI(f0)
    #t = audio.time(len(f0))
    #
    #detect_onsets = Onset(x, fs)
    #onsets = detect_onsets()
    #
    #plt.plot(detect_onsets.onsetTime, detect_onsets.onsetFunction)
    #for onset in onsets:
    #    plt.axvline(x=onset, color='red')

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
        audio_file = '../samples/monophonic/czardas_cut.wav'
        audio = AudioLoader(audio_file)
        audio.cut(stop=10)
        print("Using first ", 10, " seconds of ", audio_file)
    
    demo_yin(audio)

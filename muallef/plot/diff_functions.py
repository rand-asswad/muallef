import numpy as np
from numpy.linalg import norm
from scipy.fft import rfft, rfftfreq
from matplotlib import pyplot as plt

from muallef.util import normalize

square_diff = lambda x: np.array([norm(x[tau:] - np.roll(x, tau)[tau:], ord=2)**2 for tau in range(len(x))])

def yin_diff(x):
    d = square_diff(x)
    s = np.cumsum(d)
    yin = np.arange(len(d)) * np.divide(d, np.cumsum(d))
    yin[0] = 1
    return yin

func = {
    'ACF' : lambda x: np.array([np.dot(x[tau:], np.roll(x, tau)[tau:]) for tau in range(len(x))]),
    'AMDF': lambda x: np.array([norm(x[tau:] - np.roll(x, tau)[tau:], ord=1) for tau in range(len(x))]) / len(x),
    'SDF' : square_diff,
    'YIN' : yin_diff,
}

def time_domain_plots(signal, sample_rate, pitch=None):
    fig, ax = plt.subplots(len(func)+1, 1, sharex=True)
    fig.set_figheight(8)

    if pitch:
        t0 = 1000 / pitch
        for ax_ in ax:
            ax_.axvline(t0, linestyle='--', color='black')

    time = np.arange(0, len(signal)) * (1000 / sample_rate)
    t_unit = 'ms'

    i = 0
    ax[i].plot(time, signal)
    ax[i].yaxis.set_ticklabels([])
    ax[i].set_ylabel("signal")
    ax[i].set_xlabel(f"time ({t_unit})")
    for key in func.keys():
        i += 1
        ax[i].plot(time, func[key](signal))
        ax[i].yaxis.set_ticklabels([])
        ax[i].set_ylabel(key)
    ax[-1].set_xlabel(f"lag ({t_unit})")

    plt.show()


def spectral_plots(signal, sample_rate, pitch=None):
    N = len(signal)
    X = rfft(signal, N)
    Xmag = np.abs(X)
    freq = rfftfreq(N, 1/sample_rate)

    fig, ax = plt.subplots(3, 1, sharex=True)
    fig.set_figheight(5)
    if pitch:
        for ax_ in ax:
            ax_.axvline(pitch, linestyle='--', color='black')

    ax[0].plot(freq, Xmag)
    ax[0].yaxis.set_ticklabels([])
    ax[0].set_ylabel('spectrum')

    ax[1].plot(freq, np.abs(func['ACF'](Xmag)))
    ax[1].yaxis.set_ticklabels([])
    ax[1].set_ylabel('ACF')

    Nh = 10 # for example
    hps = 20 * np.log10([np.sum(Xmag[k:Nh*k:k]) for k in range(1, len(freq))])
    hss = np.array([20 * np.sum(np.log(Xmag[k:Nh*k:k])) for k in range(1, len(freq))])
    ax[2].plot(freq[1:], normalize(hps), label='product')
    ax[2].plot(freq[1:], normalize(hss), label='sum')
    ax[2].legend()
    ax[2].yaxis.set_ticklabels([])
    ax[2].set_ylabel('harmonic sum/product')


    ax[-1].set_xlim(0, 5000)
    ax[-1].set_xlabel('frequency (Hz)')

    plt.show()


if __name__ == '__main__':
    from muallef.io import read_audio
    fs, data = read_audio('samples/instrument_single/oboe_a4.wav')
    x = data[int(0.5 * fs):]
    end = int(0.01 * fs)
    time_domain_plots(x[:end], fs, pitch=440)
    spectral_plots(x[:4096], fs, pitch=440)

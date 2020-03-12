# Pitch analysis

## Introduction

Pitch analysis is the task of estimating the fundamental
frequency of a periodic signal that is the inverse
of the period which is defined as
"the smallest positive member of the infinite set of time
shifts leaving the signal invariant" [@yin_2002].
As music signal frequencies vary through time,
the pitch analysis is usually performed on a short time frame (window)
allowing to express the obtained pitch as a function of time,
we will consider henceforth the analysis on a single frame.

Furthermore, the physical model we have considered
for the signal formula is based on physical hypotheses.
In fact, we considered a signal formed by a perfectly
harmonic instrument travelling in a perfectly undisturbed
homogenuous medium with no other iterfering waves.
Since such conditions are almost never met, we base our
analysis on *imperfect conditions*.
Indeed, the recorded signal represents the pressure function
at the receptors position.
Consequently, the recorder captures the pressure
at its position from *all* surrounding stimuli,
recording surrounding noise, resonance effects,
and the reflected wave with a certain lag.
As a result, we express the observed signal
as the sum of the harmonic signal $\x$ and
the residual $z$. [@yeh_thesis]
$$x(t) = \x(t) + z(t)$$

Before we move on, let's consider the *harmonicity* of a sound.
In the case of perfectly harmonic instrument the frequency
of harmonic partials is expressed as a proper multiple
of the fundamental frequency $f_h = h f_0$.
However, most musical instruments are not perfectly harmonic,
for example the $h^\text{th}$ harmonic frequency
of a vibrating string is given as
$$ f_h = h f_0 \sqrt{1 + Bh^2} \qtext{where}
    B = \frac{\pi^3 Ed^4}{64l^2T}$$
where $B$ is the inharmonicity factor of the string,
$E$ is Young's modulus, $d$ is the diameter of the string,
$l$ is its length and $T$ is its tension.
We refer to such signals as **quasi-periodic**.
Pitch analysis therefore has to take into account
the inharmonicity of a signal in the process of estimating
its fundamental frequencies in order to prevent
cases of false negatives (missed pitches).
[source needed]

Pitch analysis deals with both monophonic and polyphonic signals,
a monophonic signal is a signal produced by a single harmonic
source whereas polyphonic signals have multiple sources,
in the case of the latter the
task is significantly harder.
Nevertheless, pitch estimation methods for both
single and multiple sourced harmonics can be
classified into two categories: methods that
estimate the *period* in the signal time domain
and methods that estimate the $f_0$ from the harmonic
patterns in the signal spectrum.

## Single pitch

Single pitch estimation is based on finding the fundamental
frequency of a monophonic sound.
The quasi-periodic monophonic signal $\x$ is expressed as
$$\x(t)=\sum_{h=1}^{\infty} A_h\cos(2\pi f_0 t + \phi_h)$$
For practical reasons, a finite number of harmonic
partials $H$ is used to approximate the signal.
$$\x(t)\approx\sum_{h=1}^{H} A_h\cos(2\pi f_0 t + \phi_h)$$

The estimation of $f_0$ can be approached in two
different ways: by analysing the time function $x(t)$
or by analysing the signal spectrum $X(f)$.

### Time domain

Time domain methods analyse the repetitiveness of the wave
by comparing the signal with a delayed version of itself.
This comparison is achieved using special functions that
represent the pattern similarity or dissimilarity
as a function of the **time lag** $\tau$.

We will study and compare a the functions that
appear the most in litterature.

#### Autocorrelation function {-}

The autocorrelation function (ACF) comes immediately to mind.
By definition, autocorrelation is the similarity
function between observations.
Given a discrete signal of $N$ samples, the autocorrelation
function is defined as
$$r[\tau] = \sum_{t=1}^{N-\tau} x[t]x[t+\tau]$$

The value is of the ACF is at a local maximum when the lag is equal
to the signal's period or its multiples.
Autocorrelation is sensitive to structures in signals,
making it useful to applications of speech detection.
However, in the case of music signals, resonance structures
appear hence the need for a better adapted function.

#### Difference function {-}

The Average Magnitude Difference Function (AMDF) [@ross_average_1974]
is the average unsigned difference between $x(t)$ and $x(t+\tau)$.
$$d_{\text{AM}}[\tau] = \frac{1}{N}
    \sum_{t=1}^{N-\tau} \abs{x[t]-x[t+\tau]}$$
The difference function is at its local minima for lags equal to
proper multiples of the signals period.
AMDF is more adapted than autocorrelation for applications
in music processing.

#### Squared difference function {-}

The Squared Difference Function (SDF) is very similar to AMDF,
it accentuates however the dips at the signals period
therefore indicate local extrema more clearly.
$$d[\tau] = \sum_{t=1}^{N-\tau}(x[t]-x[t+\tau])^2$$

**YIN algorithm** [@yin_2002] employs the SDF as an auxiliary
function for calculating the **cumulative mean normalized
difference function** that divides SDF by its average
over shorter lags and starts at 1 rather than 0 (in the case
of SDF and AMDF); it tends to stay large at short lags
and drops when SQD falls under its average.

$$d_{\text{YIN}}[\tau] = \begin{cases}
    1 &\text{if}~\tau = 0\\
    d[\tau] / \frac{1}{\tau}\sum\limits_{t=0}^{\tau} d[t]
        &\text{otherwise}
\end{cases}$$

```{python time_psf}
from muallef.io import AudioLoader
from muallef.plot import diff_functions as df

cello = AudioLoader('samples/instrument_single/cello_csharp2.wav')
cello.cut(start=2, stop=2.06)
df.time_domain_plots(cello.signal, cello.sampleRate, pitch=69.3)
```

### Spectral domain

Fourier transform is the most adapted mathematical tool
for analysing periodicity in functions.
The transform produced a complex function of frequency,
where the magnitude of the transform attains its local
maxima at the signal's frequency and its *harmonics*.

<video width="800" controls>
    <source src="plot/fourier.mp4" type="video/mp4">
</video>

Spectral domain methods analyse the fourier transform
of the signal, which usually gives better results.
Nevertheless, similar comparison functions are employed
in order to get the fundamental frequency.

#### Spectral autocorrelation {-}

Autocorrelation measures repititive patterns, since harmonics
appear at almost fixed frequency intervals, ACF allows
to identify harmonic partials. [@lahat_spectral_1987]
The autocorrelation is applied to the spectrum of the signal,
that is the magnitude of the fourier transform.
The function attains its local maxima at frequency shifts
that are multiples of $f_0$, otherwise the function
is attenuated since the partial peaks are not well aligned.

For a spectrum $S[f]=\abs{X[f]}$ with $K$ spectral bins
$$R[f] = \sum_{k=1}^{K-f} S[k]S[k+f]$$

#### Harmonic sum {-}

A *frequency histogram* represents the number of occurrences
of each frequency, it does not however reflect the *amplitudes*
of the harmonics of frequencies.
Schroeder proposes to *weight* the contribution of each harmonic
to the histogram with a monotonically increasing function
of its amplitude, this is done using *log compression*
where spectral harmonic bins are compressed with a logarithm.
Finally, Schroeder proposed two functions of frequency that
sum the compressed weighted histogram. [@schroeder_period_1968]

- **Harmonic sum:** $$\Sigma(f)=\sum_{m=1}^M 20\log_{10}S(nf)$$
- **Harmonic product:** $$\Sigma'(f)=20\log_{10}\sum_{m=1}^M S(nf)$$

The sum inside the logarithm in the harmonic product
can be viewed as a product because of the properties
of the logarithm function.

```{python spectral_psf}
oboe = AudioLoader('samples/instrument_single/oboe_a4.wav')
oboe.cut(start=0.5)
df.spectral_plots(oboe.signal[:4096], oboe.sampleRate, pitch=440)
```

#### Spectral YIN {-}

```{python monopitch}
from muallef.pitch import MonoPitch

czardas = AudioLoader('samples/monophonic/czardas_cut.wav')

yin = MonoPitch(czardas.signal, czardas.sampleRate, method='yin')
yin_f0 = yin()
yin_conf = yin.confidence
yinfft = MonoPitch(czardas.signal, czardas.sampleRate, method='yinfft')
yinfft_f0 = yinfft()
yinfft_conf = yinfft.confidence
time = czardas.time(len(yin_f0))

fig, ax = plt.subplots()
fig.set_figheight(8)
ax.scatter(time, yin_f0, c='blue', s=10*yin_conf)
ax.scatter(time, yinfft_f0, c='red', s=10*yinfft_conf**2)
_ = ax.set_ylim(0, 2000)
plt.show()
```

## Multiple pitch

In polyphonic music analysis, we are interested in detecting
the fundamental frequences for concurrent signals,
the signals can be produced by several instruments simultanuously.

There are generally two approaches to this problem:
iterative estimation and joint estimation.
In iterative estimation, the most prominent $f_0$ is extracted
at each iteration until no additional $f_0$ can be estimated.
Generally, iterative estimation models tend to accumulate errors
at each iteration step, they are however computationally cheap.
Whereas joint estimation methods evaluation $f_0$ combinations
which leads generally to more accurate estimates, however
the computational cost is significantly increased.[@benetos_2013]

Let's start by establishing a formalism of the task.
The harmonic signal $\x(t)$ can be expressed as the
sum of $M$ harmonic signals.
$$\x(t)=\sum_{m=1}^M \x_m(t)$$
where $\x_m(t)$ is a harmonic monophonic signal
similar to signals we've seen so far.
It follows, simiilarly to before that:
$$x(t)\approx \sum_{m=1}^{M} \sum_{h=1}^{H_m}
    A_{m,h} \cos(2\pi h f_{0,m}t + \phi_{m,h}) + z(t)$$

### Iterative estimation

#### Klapuri 2006

```{python klapuri}
from muallef.pitch import MultiPitch
from muallef.util.units import Hz_to_MIDI

fur_elise = AudioLoader('samples/polyphonic/furElise.wav')
fur_elise.cut(stop=3)

klapuri = MultiPitch(fur_elise.signal, fur_elise.sampleRate, method='klapuri')
multif0 = Hz_to_MIDI(klapuri())
time = fur_elise.time(multif0.shape[1])

fig, ax = plt.subplots()
for m in range(multif0.shape[0]):
    pitch = multif0[m]
    ax.scatter(time, pitch, c='blue')
_ = ax.set_ylim(20, 109)
plt.show()
```

### Joint estimation

### Results
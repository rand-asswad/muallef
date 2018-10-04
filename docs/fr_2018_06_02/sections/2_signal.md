# Signaux sonores

## Musique & Son

L'humain fait le lien entre la musique et le son dans son cerveau instantanément sans
le moindre d'efforts. Néanmoins, nous voudrions établir ce lien de façon scientifique.

Un son possède des les caractéristiques suivants:

- Hauteur tonale (fréquence)
- Durée
- Intensité (énergie)
- Timbre (source sonore)

La musique se caractérise par:

- **La mélodie:** la suite de phrases ou motifs sonores monophones
- **L'harmonie:** l'ensemble de son différents simultanés
- **Le rythme:** la suite de durées du son
- **La nuance:** l'intensité relative du son
- **Le timbre:** la nature du son / son source / son empreinte

Nous allons expliquer dans ce projet les notions de base de ce lien.

## Son harmonique

Le son d'un résonateur acoustique comme une chorde ou une colonne d'air
est une onde stationnaire. On dit que tel son évoque un **pitch défini**.
Dans le cas des instruments de percussion, le son présente une *inharmonicité*.
On dit que tel son évoque un **pitch indéfini**.
Dans ce projet on ne s'intéressera qu'au sons harmoniques de pitch défini.

![Les harmoniques d'une chorde vibrante](img/harmonic-string.png){height=35%}

Un signal sonore de pitch défini, est une série harmonique de sons purs, représenté par
des ondes sinusoïdales dont les fréquences sont des multiples **entiers**
d'une fréquence dîte la **fondamentale** (où le **pitch**) notée $f_0$.

$$ x(t) = \sum\limits_{k\in\mathbb{N}} A_k\cdot\cos(2\pi k f_0 t) $$
où $A_k$ est l'amplitude de la k^ème^ harmonique.

On cherche donc à indentifier $f_0$ dans un signal harmonique donnée.

## Discrétisation et échantillonnage

La numérisation d'un signal consiste à prélever des valeurs du signal à intervalles définis.
Les valeurs obtenues sont appelées des *échantillons*.

La *période d'échantillonnage* $T_s$ est l'intervalle de temps entre deux échantillons, on définit
$f_s=\frac{1}{T_s}$ le nombre d'échantillons prélevés par secondes, $f_s$ est dît
*fréquence d'échantillonnage* ou en anglais **sample rate**.

On note $x[n] = x(t_n)$ où $t_n = n\cdot T_s = \frac{n}{f_s}$. Dans le reste du projet, on notera toujours
$[\cdot]$ les valeurs discrètes.

L'échantillonnage d'un signal consiste à choisir une fréquence d'échantillonnage sans perdre de valeurs importantes
du signal. En traitement de signaux sonores, $f_s$ est souvent égale à $44.1 kHz, 22.05 kHz, 16 kHz,\text{ou } 8kHz$.
La numérisation d'un signal dépend aussi d'autre facteurs comme le *bit depth*
(i.e. le nombre de bits pour stocker chaque échantillon), mais nous ne nous intéressons pas par les détails;
les bases de l'échantillonnage de signaux sont expliquées et démontrées par le théroème d'échantillonnage de **Nyquist-Shannon**.

## La transformée de Fourier (FT)
La transformée de Fourier se définit par:
$$\hat{x}(f) = \int\limits_{-\infty}^{\infty} x(t)\cdot e^{-2\pi j ft}\mathrm{d}t$$

Cette transformation permet d'identifier la fréquence d'une fonction périodique.
En effet, La transformée de Fourier représente l'intensité d'une fréquence dans un signal,
donc ses pics correspondent aux fréquences du signal.

<video width="800" controls>
    <source src="../../figures/out/fourier.mp4" type="video/mp4">
</video>

Comme la transformée de Fourier est linéaire, la transformée d'un signal
harmonique produit plusieurs pics.

![Linéarité de la transformée de Fourier](../../figures/out/fourier_linearity.png)

## La transformée de Fourier discrète (DFT)

Soit $N$ le nombre d'échantillons pris sur l'intervalle $[0,t_{\text{max}}[$, soit $f_s$ la fréquence
d'échantillonage. Pour $n=0,1,\dots,N-1$ on a:

\begin{align*}
\hat{x}(f) &= \int\limits_{0}^{t_{\text{max}}} x(t)\cdot e^{-2\pi j ft}\mathrm{d}t \\
    &= \lim\limits_{f_s\rightarrow\infty} \sum\limits_{n=0}^{N-1} x(t_n)\cdot e^{-2\pi j ft_n}\\
    &= \lim\limits_{f_s\rightarrow\infty} \underbrace{\sum\limits_{n=0}^{N-1} x[n]\cdot e^{-2\pi j f \frac{n}{f_s}}}_{\hat{x}[f]}\\
    &= \lim\limits_{f_s\rightarrow\infty} \hat{x}[f]
\end{align*}

La DFT de $x[n]$ se définit donc par:
$$ \hat{x}[k] = \sum\limits_{n=0}^{N-1} x[n]\cdot e^{-2\pi j k \frac{n}{f_s}} $$

**Remarque:** La DFT se calcule souvent matriciellement pour économiser les calculs. De plus, dans le cas
où $N=2^p,p\in\mathbb{N}$ on calcule la transformée de Fourier rapide (FFT) qui utilise le symétrie
pour minimiser le nombre de calculs.

## Fenêtrage
Nous avons souvent besoin de traiter le signal sur une durée limitée, on définit donc une fonction
à support compact $w$ et on étudie le produit de convolution du signal avec la fenêtre.

Voici quelques exemples de fenêtres:

- Fonction rectangulaire:
$$ \mathrm{rect}_{[0,T]}(t) = \begin{cases} 1 &\text{si } t\in[0,T]\\0 &\text{sinon} \end{cases} $$
- Fenêtre Hann:
$$ w(t) = \sin^2 \left( \frac{\pi t}{T} \right) \cdot\mathrm{rect}_{[0,T]}(t) $$
- Fenêtre Welch (fenêtre parabolique):
$$ w(t) = 1 - \left( \frac{2t - T}{T} \right) \cdot\mathrm{rect}_{[0,T]}(t) $$

Nous avons choisi d'utiliser la fenêtre de Hann dans notre projet car elle attenue le phénomène **aliasing** qui rend les signaux
indisntinguables lors de l'échantillonnage.

$$w[n] = \sin^2\left(\frac{\pi n}{N -1}\right)
    = \frac{1}{2}\left(1-\cos\left(\frac{2\pi n}{N -1}\right)\right)$$

![La fenêtre Hann est sa transformée de Fourier](img/Hann.png){width=70%}

## La transformée de Fourier à court terme (STFT)

La transformée de Fourier nous permet d'obtenir les fréquences d'un signal harmonique.
Or, la fréquence d'un signal peut changer en fonction du temps, on voudrait donc
avoir la transformée de Fourier en fonction de la fréquence *et* du temps.

La transformée de Fourier à court terme $X(t,f)$ est la transformée de Fourier
de $x$ sur une fenêtre glissante $w$ centrée en $t$ (i.e. $w(\tau-t)$).

$$X(t, f) = \int\limits_{-\infty}^{\infty} x(\tau)\cdot w(\tau-t)\cdot e^{-2\pi j f\tau} \mathrm{d}\tau $$

De même, la STFT discrète se définit:
$$X[n, k] = \sum\limits_{n=0}^{N-1} x[m]\cdot w[m-n]\cdot e^{-2\pi j k \frac{m}{f_s}}$$

## Spectrogramme

Le spectrogramme permet de visualiser les changement de fréquences en fonction du temps, il se définit par:
$$ S(t,f) = \left\lvert X(t,f) \right\rvert $$

**Remarque:** Si on voudrait visualiser la puissance spectrale d'un signal, on prend le carré de la module
de la STFT.

## Méthodes d'analyse

Ils existent deux types d'analyse de signaux harmoniques:

1. **Analyse temporelle:** il s'agit d'étudier le signal sans passer par la transformée de Fourier.
2. **Analyse fréquentielle/spéctrale:** il s'agit d'étudier le spectre du signal (sa transformée de Fourier).

On obtient toujours des meilleurs résultats par l'analyse fréquentielle, mais la transformée de Fourier
demande un calcul coûteux.
Dans le cas d'un signal simple (e.g. percussion, rythmique, etc) on privilégie l'analyse temporelle.
Sinon, dans le cas d'un signal complexe (e.g. instruments mélodiques, signal polyphône, etc) l'analyse
fréquentielle est privilégié.

## Implémentation

On lit un fichier audio grâce à la class `source` qu'on a défini
```{python}
from muallef.utils import source
audio_file = project_path + "sounds/violin/violin-czardas-cut.wav"
sound = source(audio_file)
x = sound.signal
fs = sound.sampleRate
t = sound.get_time()
```

On trace le signal à l'aide de la librairie `matplotlib`
```{python}
from matplotlib import pyplot as plt
plt.clf()
plt.plot(t, x)
plt.show()
plt.clf()
```

\pagebreak
On trace le spectrogramme du signal
```{python}
from figures import plot_spectrogram
fig = plt.figure()
ax = fig.add_subplot(111)
ax, out = plot_spectrogram(signal=x, sample_rate=fs, axis=ax, color_map='inferno')
plt.show()
plt.clf()
```



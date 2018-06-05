# Signaux sonores

## Son harmonique

Le son d'un résonateur acoustique comme une chorde ou une colonne d'air
est une onde stationnaire. On dit que tel son évoque un **pitch défini**.
Dans le cas des instrument de percussion, le son présente une *inharmonicité*.
On dit que tel son évoque un **pitch indéfini**.
Dans ce projet on ne s'intéressera qu'au sons harmoniques de pitch défini.

Un signal sonore de pitch défini, est une série harmonique de sons purs, représenté par
des ondes sinusoïdales dont les fréquences sont des multiples **entiers**
d'une fréquence dîte la **fondamentale** (où le **pitch**) notée $f_0$.

$$ x(t) = \sum\limits_{k\in\mathbb{N}} A_k\cdot\cos(2\pi k f_0 t) $$
où $A_k$ est l'amplitude de la k^ème^ harmonique.

On cherche donc à indentifier *f_0* dans un signal harmonique donnée.

## La transformée de Fourier et ses variantes
La transformée de Fourier permet d'identifier la fréquence d'une fonction périodique.
$$\hat{x}(f) = \int\limits_{-\infty}^{\infty} x(t)\cdot e^{-2\pi j ft}\mathrm{d}t$$
<video width="800" controls>
    <source src="plot/fourier.mp4" type="video/mp4">
</video>
Le pic de $\hat{x}(f)$ correspond à la fréquence du signal $x(t)$.
Comme la transformée de Fourier est linéaire, la transformée d'un signal
harmonique produit plusieurs pics.

![Linéarité de la transformée de Fourier](plot/fourier_linearity.png)

## La transformée de Fourier à court terme
Grâce à la transformée de Fourier et sa linéarité on peut obtenir les fréquences
d'un signal harmonique. Or, en pratique, un signal sonore change souvent
de fréquences, on voudrait donc obtenir la transformée de Fourier en fonction
du temps **et** de la fréquence, la transformée de Fourier à court terme
(anglais: *Short-Time Fourier Transform*) souvent dîte **STFT**
permet d'obtenir tel fonction.

La STFT se calcule à l'aide d'une **fonction de fenêtrage** $w$, qui est
une fonction à support compact. En effet, la STFT est la transformée
de Fourier d'une fonction pondérée avec une fenêtre $w$ de support
compact suffisamment petit. Le principe de cette transformée est
analogue au produit de convolution.

$$X(t, f) = \int\limits_{-\infty}^{\infty} x(\tau)\cdot w(\tau-t)\cdot e^{-2\pi j f\tau} \mathrm{d}\tau $$

## La transformée de Fourier discrète
Dans ce projet, on voudrais analyser un son enregistré, on étudie donc
le signal sur un intervalle fermé en temps discret.

Soit $N$ le nombre d'échantillons pris sur l'intervalle $[0,t_{\text{max}}[$.
On introduit la fréquence d'échantillonnage $f_s$ dîte en anglais *sample rate* ou *sampling frequency*.
On a donc $t_n = \frac{n}{f_s}$

On note $x[n] = x(t_n)$ avec $t_n=\frac{n}{f_s}$ où $f_s$ est la fréquence d'échantillonnage
dîte en anglais *sample rate* ou *sampling frequency*.

Sur une intervalle de temps $$, 

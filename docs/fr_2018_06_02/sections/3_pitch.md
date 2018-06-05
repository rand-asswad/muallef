# Pitch
Ils existent plusieurs algorithmes de détection de fréqences fondamentales,
il y'en a deux types : applications sur le domaine temporel et sur le domaine fréquenciel.
Les applications sur le domaine fréquenciel calculent les fréquences à partir de la transformée
de Fourier du signal, où les méthodes du domaine temporel les calcules à partir du signal
sans passer par la transformée de Fourier.

Chaque type présente des avantages et des inconvénients. Nous avons décidé d'implémenter
une de chaque type:

## YIN
L'algorithme de YIN *(Kawahara et de Cheveigné, 2002)* est une méthode
robuste pour la reconnaissance du pitch, il s'agit d'un modèle temporel.
Son principe est la séléction de fréquences candidats parmi toutes les fréquences
détéctés sur l'intervalle de fenêtrage.

La méthode propose que l'expression $x(t)-x(t+\tau)$ atteint son minimum
quand $\tau$ est égale à la période du signal (i.e. $\frac{1}{f_0}$).
En diffinissant la fonction de différence à l'instant $t$ fixé:
$$ d_t(\tau) = \int\limits_{t}^{t+T_w} \left(x(t)-x(t+\tau)\right)^2 \mathrm{d}t $$
où $T_w$ est la taille de la fenêtre $w$, on appelle $\tau$ le *retard* (anglais: *lag*).

Soit en temps discret:
$$ d_n[m] = \sum\limits_{i=n+1}^{n+N_w} \left(x[n]-x[n+m]\right)^2 $$

Par la suite, on calcule la fonction de la moyenne cumulative définie par:
$$d_t'(\tau) = \begin{cases}
1 &\text{si} \tau = 0\\
d_t(\tau) / \frac{1}{\tau}\int\limits_{0}^{\tau}d_t(u)\mathrm{d}u &\text{sinon}
\end{cases}$$
Soit en temps discret:
$$d_n'[m] = \begin{cases}
1 &\text{si} m = 0\\
d_n[m] / \frac{1}{m}\sum\limits_{i=0}^{m}d_t[i] &\text{sinon}
\end{cases}$$

Les candidats sont les minimums locaux de $d_n'$.

## YIN spectrale
L'algorithme de YIN spectrale *(Paul Brossier, 2006)* est une méthode qui utilise
la même logique de l'algorithme de YIN et l'applique sur la STFT.

La fonction de différence est définie par:
$$ \hat{d}_n[m] = \frac{2}{N}
\sum\limits_{k=0}^{\frac{N}{2}+1}
\left\lvert\left( 1-e^{2\pi jkm/N} \right)   X[n,k]  \right\rvert^2 $$

La fonction de la moyenne cumulative se calcule de façon analogue à l'algorithme de YIN.
L'algorithme cherche le minimum globale de cette dernière.
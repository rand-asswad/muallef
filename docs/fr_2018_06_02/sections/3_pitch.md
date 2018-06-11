# Pitch
Dans cette partie, nous allons étudier des méthodes de reconnaissance de la fréquence fondamentale
d'un signal.

## YIN
L'algorithme de YIN *[@yin]* est une méthode robuste pour la reconnaissance du pitch dans le domaine temporel.
Son principe est la séléction de fréquences candidates parmi toutes les fréquences détéctées
sur l'intervalle de fenêtrage.

La méthode propose que l'expression $x(t)-x(t+\tau)$ atteint son minimum
quand $\tau$ est égale à la période du signal (i.e. $\frac{1}{f_0}$).
En diffinissant la fonction de différence à l'instant $t$ fixé:

$$ d_t[\tau] = \sum\limits_{i=t+1}^{t+W} \left(x[t]-x[t+\tau]\right)^2 $$
où $W$ est la taille de la fenêtre $w$, on appelle $\tau$ le *retard* (anglais: *lag*).

Par la suite, on calcule la fonction de la moyenne cumulative définie par:
$$d_t'[\tau] = \begin{cases} 1 &\text{si} \tau = 0\\
d_t[\tau] / \frac{1}{\tau}\sum\limits_{i=0}^{\tau}d_t[i] &\text{sinon}
\end{cases}$$

Les candidats sont les minimums locaux de $d_t'$.
On séléctionne les candidats avec $d_t'[\tau]$ inférieur à un seuil fixé (les auteurs
recommandent un seuil de 0.1).

## YIN spectrale
L'algorithme de YIN spectrale *[@yinfft]* est une méthode qui utilise
la même logique de l'algorithme de YIN et l'applique sur le spectre du signal.

La fonction de différence est définie par le carré de la différence spéctrale:
\begin{align*}
\hat{d}_t[\tau] &= \frac{4}{N} \sum\limits_{k=0}^{\frac{N}{2}+1} \left\lvert X[t,k] \right\rvert^2
       - \frac{2}{N} \sum\limits_{k=0}^{\frac{N}{2}+1} \left\lvert X[t,k] \right\rvert^2
       \cdot \cos \left( \frac{2\pi k\tau}{N} \right) \\
    &= \frac{2}{N} \sum\limits_{k=0}^{\frac{N}{2}+1} \left\lvert X[t,k] \right\rvert^2
       \cdot \left( 2 - \cos \left( \frac{2\pi k\tau}{N} \right) \right) \\
    &= \frac{2}{N} \sum\limits_{k=0}^{\frac{N}{2}+1}
       \left\lvert\left( 1-e^{2\pi jk\tau/N} \right) X[t,k] \right\rvert^2
\end{align*}

La fonction de la moyenne cumulative se calcule de façon analogue à l'algorithme de YIN.
L'algorithme cherche le minimum globale de cette dernière.

Cette méthode est la plus utilisée pour la détection de pitch car elle donne de très bonnes résultats
et a pour complixité $O(n\log n)$

## Implémentation

```{python}
import numpy as np
from muallef import pitch

t, f, conf = pitch.detect(signal=x, sampleRate=fs, bufferSize=2048, method='yinfft')
# t: le temps en secondes
# f: la fréquence en Hz
# conf: le taux de confiance

size = np.power(conf, 3)

fig = plt.figure()
ax = fig.add_subplot(111, ylim=(170, 600))
ax.scatter(t, f, marker='o', s=size)
ax.set_xlabel("Time (s)")
ax.set_ylabel("Frequency (Hz)")

plt.show()
plt.clf()
```

\pagebreak

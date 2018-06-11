# Segmentation temporelle
L'étape fondamentale dans la reconnaissance du son est la segmentation temporelle.
Il s'agit de trouver les frontières des objets sonores, c'est-à-dire:

+ Le début de la note – dît **_onset_**.
+ La fin de la note – dît **_offset_**.

![](img/onset.png){width=50%}

<p class=caption>
    Attack, transient, decay, onset</br>
    IEEE TRANSACTIONS ON SPEECH AND AUDIO PROCESSING, VOL. 13, NO. 5, SEPTEMBER 2005
</p>

Cette étape dépend fortement sur le type du son produit; les instrument
à chordes pincées (guitare, piano, oud, etc.) ont un profile différent de celui
des instruments à cordes frottées (la famille du violon) ou de celle des instruments à vent.

Dans cette partie on expliquera les méthodes implémentés pour la reconnaissance du **onset**.

## Méthode
La lecture scientifique nous a donné une méthode rigoureuse qu'on a simplifié pour
obtenir des résultats rapidement.

Il s'agit de définir une fonction qui permet de quantifier la perturbation du signal
à un moment donné, cette fonction est souvent appelée **Onset Detection Function**
ou **Onset Strength Signal**, dans ce projet on fera référence à cette dernière
par **Onset Detection Function** ou **_ODF_**.

Théoriquement, les maximums locaux de l'ODF sont les onsets du signal,
mais en pratique il s'agit d'un sous-ensemble de ces points.
En effet, l'ODF est souvent très sensible et détectera la moindre des perturbations.

Ce problème pourra être résolu en définissant un seuil au dessous duquel
aucun onset est considéré. Ils existent plusieurs méthodes pour définir tel seuil.

Soit un seuil fixe, ce qui minimise le coût des calculs au prix de la qualité des résultats.
Soit de calculer un seuil variable, il s'agit de lisser la fonction ODF par des méthodes
classiques comme la moyenne mobile.

La méthode consiste donc en trois étapes:

1. Calcul de l'**Onset Detection Function**.
2. **Thresholding**: calcul du seuil.
3. **Peak-picking**: la selection des onsets.

Une méthode heuristique est proposée par [@ismir] pour séléctionner les onsets, 
il s'agit de trouver les points $t_n$ tels que, pour $a,b,\tau\in\mathbb{N}, \delta\in{R_+}$ fixés:
- $x[n] = \max\limits_{n+a \leq i\leq n + b} x[i]$
- $x[n] \geq \delta + \frac{1}{a+b+1}\sum\limits_{n+a \leq i\leq n + b} x[i]$
- Si $O$ est l'ensembles d'onsets, $\forall n,m\in O, \lvert n - m \rvert > \tau$

Cette méthode permet de vérifier que le point choisi est un maximum local et suffisament
loin du point précédant, l'avantage de cette méthode est sa rapidité.

## Onset Detection Function (ODF)
Ils existent plusieurs fonction de détéction d'onsets, on expliquera
quelques unes qui se basent sur la STFT.

### High Frequency Content (HFC)
Il s'agit de priviligier les fréquences élevées dans un signal.
$$ D_{HFC}[n] = \sum\limits_{k=1}^{N}k\cdot\left\lvert X[n,k]\right\rvert^2 $$
[@hfc]

### Phase Deviation (Phi)
Il s'agit de calculer les différences de phases en dérivant l'argument complex
de la STFT, on note
$$ \varphi(t, f) = \mathrm{arg}(X(t, f)) $$
$$\hat{\varphi}(t, f) = \mathrm{princarg}
\left( \frac{\partial^2 \varphi}{\partial t^2}(t, f)  \right) $$
où
$$ \mathrm{princarg}(\theta) = \pi + ((\theta + \pi) mod (-2\pi)) $$
donc la ODS de phase se calcule par la formule:
$$ D_{\Phi}[n] = \sum\limits_{k=0}^{N}\left\lvert \hat{\varphi}[n, k] \right\rvert $$
[@phase]

Dans notre implémentation, nous avons approximé la dérivée partielle seconde
de la phase par un schéma de Taylor d'ordre 2.

### Complex Distance
Cette méthode permet de qualifier les changements spectraux du signal
ainsi que les changements en phase. Il s'agit de calculer une prédiction
du spectre du signal, et puis le comparer par sa valeur.
On reprend la fonction calculée en $\hat{varphi}(t, f)$ de la méthode précédante.
On définit la prédiction :
$$ \hat{X}[n, k] = \left\lvert X[n, k] \right\rvert \cdot e^{j\hat{\varphi}[n, k]} $$

Donc la distance complexe se calcule:
$$ D_{\mathbb{C}}[n] = \sum\limits_{k=0}^{N} \left\lvert  \hat{X}[n, k] - X[n, k] \right\rvert ^2 $$ 
[@complex]

## Thresholding
Nous avons décidé de lisser la fonction ODF par une moyenne mobile echelonnées
par la fenêtre Hann, il s'agit du produit de convolution de l'ODF avec la fonction Hann.

## Résultats

Au premier lieu, nous avons effectués des tests sur des morceaux de violon joués par Rand et nous avons obtenus
de très mauvaises résultats de segmentation temporelle. Nous avons ensuite essayé des morceaux
plus facile joués par des musiciens plus expérimentés mais nous n'avons pas obtenu des meilleurs résultats.

On a donc considéré d'autres instruments, nottamment ceux à chordes pincées comme le piano et la guitare.
Nous avons directement obtenu des très bons résultats.

Ceci s'explique par le fait que la famille de violon (chordes frottées) produit un son **_Legato_**,
la segmentation temporelle dépend donc moins sur l'énergie du signal (ou son spectre) et plus sur
la fréquence fondamentale.

![Comparaison entre les profiles temporels du violon et du piano](../../figures/out/onset.png)

On voit bien que les onsets sont bien détectés dans le cas du piano. Voici le morceau fameux
de Beethoven **Für Elise**.

```{python}
from muallef.onset import onset_function
from muallef.onset.peak_picker import peak_pick

piano_sound = project_path + "sounds/piano/FurElise-mono.wav"
fur_elise = source(piano_sound)

plt.clf()
fig = plt.figure()
ax1 = fig.add_subplot(211)
ax1.plot(fur_elise.get_time(), fur_elise.signal)
ax1.set_title("Piano signal")


ax2 = fig.add_subplot(212)
t, odf = onset_function(signal=fur_elise.signal, sampleRate=fur_elise.sampleRate,
                                windowSize=2048, method="complex", normalize=True)
ax2.plot(t, odf, label="Complex Distance")
onsets = peak_pick(odf, delta=0.05, wait=4)
ax2.plot(t[onsets], odf[onsets], marker="x", ls="", label="Peaks")
ax2.legend(loc="upper right")
ax2.set_title("Onset Detection Function & Selected Peaks")

plt.subplots_adjust(hspace=0.5)
plt.show()
```

\pagebreak

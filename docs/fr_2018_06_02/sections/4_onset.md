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
La lecture scientifique indique une méthode rigoureuse qu'on a simplifier pour
obtenir des résultats rapide.

Il s'agit de définir une fonction qui permet de quantifier la perturbation du signal
à un moment donné, cette fonction est souvent appellée **Onset Detection Function**
ou **Onset Strength Signal**, dans ce projet on fera référence à cette dernière
par **Onset Detection Function** ou **_ODF_**.

Théoriquement, les maximums locaux de l'ODF sont les onsets du signal,
mais en pratique il s'agit d'un sous-ensemble de ces points.
En effet, l'ODF est souvent très sensible et détectera la moindre des perturbations.

Ce problème pourra être résolu en définissant un seuil au dessous duquel
aucun onset est considéré. Ils existent plusieurs méthodes pour définir tel seuil.

Soit un seuil fixe, ce qui minimise le coût des calculs au prix de la qualité des résultats.
Soit de calculer un seuil variable par des méthodes classiques comme la moyenne mobile.

La méthode consiste donc en trois étapes:
1. Calcul de l'**Onset Detection Function**.
2. **Thresholding**: calcul du seuil.
3. **Peak-picking**: la selection des onsets.

## Onset Detection Function (ODF)
Ils existent plusieurs fonction de détéction d'onsets, on expliquera
quelques unes qui se basent sur la STFT.

### High Frequency Content (HFC)
Il s'agit de priviligier les fréquences élevées dans un signal:
$$ HFC[n] = \sum\limits_{k=1}^{N}k\cdot\left\lvert X[n,k]\right\rvert^2 $$

### Phase Deviation
### Complex Distance




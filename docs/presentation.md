---
title: Algorithme CORDIC
author: Rand ASSWAD
subtitle: Jack E. Volder
institute: Université de Rouen Normandie
lang: fr-FR
---

# Plan

- Codage de réels sur machine
- Fonctions trigonométriques
- Algorithme Cordic
- Guarantie de précision
- Implémentation
- Alternatifs
- Questions

# Les fonctions trigonométriques

---

![](img/trig.gif)

## Applications

### Directes

- Exponentielles complexes
- Résolutions des EDO linéaires d'ordre 2
- Résolutions des EDP
- Séries et transformations de Fourier

### Indirectes

- Acoustique et musique
- Transmission des signaux (radio, télé, etc)
- Navigation, GPS
- Imagerie
- ...

# Codage de réels sur machine

## Virgule Fixe

Codage similaire aux entiers

![](img/fixed_point.gif)

---

**exemple :** $20.75_{10} = 10100.1100_2$

| Puissance | $2^5$ | $2^4$ | $2^3$ | $2^1$ | $2^0$ | $2^{-1}$ | $2^{-2}$ | $2^{-3}$ | $2^{-4}$ |
|:----------|:-----:|:-----:|:-----:|:-----:|:-----:|:--------:|:--------:|:--------:|:--------:|
| Valeur    |  16   |   8   |   4   |   2   |   1   |   0.5    |   0.25   |  0.125   |  0.0625  |
| Bit Mask  |   1   |   0   |   1   |   0   |   0   |    1     |    1     |    0     |    0     |



- **Avantage :** simple donc calculs robustes
- **Inconvénient :** compromis entre l'amplitude et la précision
  + pour $n$ bits, un précision $p$, l'amplitude est de $2^{n-p}$
  + pour avoir 3 chiffres décimaux après la virgule, il faut 10 bits de précision
  + Le plus grand représentable sur 32 bits avec 3 bits de précision est $2~097~151.875$
  + un nombre comme $11!$ ne pourrais pas être représenté !

## Virgule Flottante

$$ x = (-1)^s 2^e (1 + m) $$

- **Signe :** $s\in\{0,1\}$
- **Exposant :** $e\in \mathbb{Z}$
- **Mantisse :** $m\in \left[0,1\right[$

Il s'agit de la notation scientifique en base 2

---

### Standard IEEE-754

$$ x = (-1)^s 2^e (1 + m) $$

![](img/ieee-754.png)

- l'exposant se stocke sur $q$ bits
- la mantisse se stocke sur $p$ bits


|     | single (32 bits) | double(64 bits) |
|:----|:----------------:|:---------------:|
| $q$ |        8         |       11        | 
| $p$ |        23        |       52        | 

---

### Quelques remarques sur le standard IEEE-754

- la valeur de la mantisse est $m=k\cdot 2^{-p}$ où $k\in\left\{0,\ldots,2^p-1\right\}$
- la plage de représentation de l'exposant $e\in\left\{-2^{q-1}+2,\ldots,2^{q-1}-1\right\}$
- on réserve la valeur maximale de l'exposant pour $\infty$ et `NaN`
  et la valeur minimale pour le zéro et les nombres dénormalisés
- on stocke un exposant biaisé d'un biais $\Delta$ afin de représenter les exposants négatifs
  donc on stocke $E=e+\Delta$ où $\Delta = 2^{q-1} -1$ donc $E\in\left\{1,\ldots,2^q - 2\right\}$

# Algorithme CORDIC

## Historique

- CORDIC a été inventé en 1956 par Jack E. Volder
- Le but de CORDIC était de remplacer le résolveur (transducteur électromagnétique)
  dans les ordinateurs du bombardier Convair B-58 Hustler par une solution digitale
  plus *précise* et plus *performante* en temps réel.
- L'algorithme a été publié en 1959, et a été ensuite adopté dans les ordinateurs de navigation.

---

- Une variante de CORDIC (décimal) a été intégrée dans une machine HP en 1966,
  qui a résulté dans le premier ordinateur intégrant des fonctions scientifiques en 1968, le **hp 9100A**.
- CORDIC a été implémnté dans les FPU de Intel des années 80s.
- CORDIC est très utilisé dans les calculatrices pour son économie de mémoire et son efficacité.

## Principe

On souhaite approcher l'angle $t\in\left[-\frac{\pi}{2},\frac{\pi}{2}\right]$ par $\theta_n$

Les coordonnées du vecteur unitaires $v_n$ d'angle $\theta_n$ sont
$\left(\cos\theta_n,\sin\theta_n\right)$

- On commence avec $\theta_0 = 0$ donc $v_0=(1, 0)$
- On ajuste $\theta_n$ par l'angle $\alpha_n = \arctan 2^{-n}$
  + si $t > \theta_n$, on rajoute l'angle $\alpha_n$
  + sinon on soustrait l'angle $\alpha_n$
- On applique une rotation d'angle $\alpha_n$ à $v_n$ dans vers $t$
- On s'arrête à la précision souhaitée

---

![](img/CORDIC-illustration.png)

---

## Formellement

$$\begin{cases}
\alpha_n &= \arctan 2^{-n} \\
\delta_n &= \mathrm{sign}\left(t - \theta_n\right) \\
\theta_{n+1} &= \theta_n + \delta_n \alpha_n
\end{cases}$$

On définit les vecteurs et les rotations à l'aide des nombres complexes
$$\begin{cases}
v_n &= e^{i\theta_n} = x_n + iy_n \\
R_n &= e^{i\delta_n\alpha_n}
\end{cases}\quad
\Rightarrow v_{n+1} = R_n v_n$$

---

\begin{align}
R_n &= e^{i\delta_n\alpha_n}\\
    &= \cos\alpha_n+i\delta_n\sin\alpha_n\\
    &= \cos\alpha_n\left(1 + i\delta_n\tan\alpha_n\right)\\
    &= \cos\alpha_n\left(1 + i\delta_n\tan(\arctan 2^{-n})\right)\\
    &= \cos\alpha_n\left(1 + i\delta_n 2^{-n}\right)\\
    &= K_n \left(1 + i\delta_n 2^{-n}\right)\\
\end{align}

le nouveau vecteur s'obtient donc

\begin{align}
v_{n+1} &= R_n v_n\\
    &= K_n \left(1 + i\delta_n 2^{-n}\right) (x_n + iy_n)\\
    &= \underbrace{K_n \left(x_n + \delta_n 2^{-n} y_n\right)}_{x_{n+1}} +
       i\cdot\underbrace{K_n\left(\delta_n 2^{-n} x_n + y_n\right)}_{y_{n+1}}
\end{align}

---

Ayant les valeurs de $K_n$ et $\delta_n$, les seules opérations
à faire sont des des additions, des multiplications, et des divisions par 2 (décalages).

Supposons qu'on souhaite faire $N$ itérations:

- Il suffit de stocker les valeurs de $\alpha_n$ dans un tableau
  afin de pouvoir en déduire les valeurs de $\delta_n$
  qui sont nécessaires pour calculer $\theta_n$ et $v_n$.
- Il suffit de stocker les valeurs de $K_n=\cos\alpha_n$ pour calculer les $v_n$.

---

### Optimisation essentielle

- On peut facilement déduire que $v_N = v_0\prod\limits_{n=0}^{N-1} R_n$
- De plus, $\prod\limits_{n=0}^{N-1} R_n
  = \prod\limits_{n=0}^{N-1} K_n \prod\limits_{n=0}^{N-1} \left(1 + i\delta_n 2^{-n}\right)$
- Il suffit alors de stocker la valeur de $K = \prod\limits_{n=0}^{N-1} K_n$
- $K_n = \cos\alpha_n = \cos\arctan 2^{-n} = \frac{1}{\sqrt{1+2^{-2n}}}$
- Par conséquent, $v_N=K v_0 \prod\limits_{n=0}^{N-1} \left(1 + i\delta_n 2^{-n}\right)$
- En initialisant $v_0 = (K, 0)$ on aura simplement
  $v_n = v_0\prod\limits_{n=0}^{N-1} \left(1 + i\delta_n 2^{-n}\right)$

---

- Cette optimisation économise $N$ multiplications et la taille de $N$ nombres en mémoire
- Mode de convergence:

![](img/cordic_opti.png){width=65%}

## Adaptation pour virgule flottante

$$t\in\left[-\frac{\pi}{2},\frac{\pi}{2}\right]\subset\left]-2,+2\right[$$

donc l'exposant est nul $t=(-1)^s (1+m)$

d'où l'application de l'algorithme sur la mantisse est suffisante

# Guarantie de précision

## Proposition 1

Si $\forall n\in\mathbb{N}, 0\leq \frac{\alpha_n}{2} \leq \alpha_{n+1} \leq \alpha_n$
alors, $\forall t$ telle que $\lvert t\rvert\leq 2\alpha_0$ la suite définie
par $\theta_{n+1} = \sum\limits_{k=0}^n \delta_k \alpha_k$.

$$\forall n\in\mathbb{N}, \lvert \theta_{n+1} - t \rvert \leq \alpha_n $$

*Preuve par récurrence sur le tableau*

## Proposition 2

$\alpha_n = \arctan 2^{-n}$ vérifie
$\forall n\in\mathbb{N}, 0\leq \frac{\alpha_n}{2} \leq \alpha_{n+1} \leq \alpha_n$

*Preuve par récurrence sur le tableau*

## Conclusion

$$\forall n\in\mathbb{N}, \lvert \theta_{n+1} - t \rvert \leq \arctan 2^{-n} \leq 2^{-n} $$


# Implémentation

---

```c
vec2 cordic(double t) {
    double theta = 0; // theta[n]
    double pow2 = 1;  // 2^(-n)

    // v[0] := (K, 0)
    vec2 v;
    v.x = K;
    v.y = 0;

    double tmp;
    for (uint8_t n = 0; n < BITS; n++) {
        tmp = v.x;
        if (t >= theta) { // delta = +1
            theta += alpha[n];
            v.x -= pow2 * v.y; // x' = x - y/2^n
            v.y += pow2 * tmp; // y' = x/2^n + y
        } else { // delta = -1
            theta -= alpha[n];
            v.x += pow2 * v.y; // x' = x - y/2^n
            v.y -= pow2 * tmp; // y' = x/2^n + y
        }
        pow2 /= 2;
    }
    return v;
}
```
Opérations par itération:

- 3 additions/soustractions
- 1 multiplications
- 1 division par 2


# Merci pour votre attention

Avez-vous des questions ?

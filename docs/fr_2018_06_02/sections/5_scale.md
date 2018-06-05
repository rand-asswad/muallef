# Théorie de musique
## Introduction du problème
L'espace de notes est un espace linéaire discrèt, mais l'espace de fréquences est continue non-linéaire.
Le problème consiste à trouver une fonction qui associe les fréquences fondamentales obtenues avec des valeurs entières.

## Gammes et intervalles
En acoustique, un **intervalle** désigne le rapport de fréquences de deux sons.
Or, chaque intervalle est caractéristique d'une échelle musicale, elle-même varie selon le type de musique.

En musique, une **gamme** (*en:* **scale**) est une suite de notes conjointes où la fréquence de la dernière est le double de celle de la première.
Une gamme se caractérise par sa première note et la suite d'intervalles qui séparent les notes conjointes.

L'**armure** — ou l'**armature** (*en:* **key signature**) — est un ensemble d'altérations réunies à la clé.
Elle est composée soit exclusivement de dièses, soit exclusivement de bémols — en dehors du cas particulier constitué par le changement d'armure.
Ces altérations correspondent à la tonalité principale des mesures suivant la clé.

À chaque tonalité majeure est associée une tonalité en mode mineur, présentant la même armure de clef et appelée relative mineure.

![Le cycle des quintes](img/cycle-de-quintes.png){width=50%}

Pour simplifier, on va considérer la théorie de la musique occidentale basée sur l'accord tempéré (depuis le XVIII^e^ siècle).
Dans ce cas, l'intervalle séparant la première et la dernière note d'une gamme est dite *octave*, une octave se divise en 12 écarts égales appelés *demi-tons*.
La dernière note porte le même nom de la première dans la gamme.

![Les intervalles sur un piano](img/intervalles-piano.png){width=100%}

## Nomenclature
Ils existent plusieurs systèmes de nomenclature de notes de musique.
Le système utilisé en France adopte les noms en termes de *Do-Ré-Mi-Fa-Sol-La-Si*.
De plus, il existe un système basé sur l'alphabet latin : *C-D-E-F-G-A-B*.
Les deux systèmes sont très utilisés, dans ce projet on utilisera le dernière pour simplifier.

Vu que les noms des notes se répètent au bout d'un octave, il faut distinguer une note *LA* de fréquence $440Hz$ d'une autre de fréquence $220Hz$ ou $880Hz$.

Le système de notation scientifique **Scientific Pitch Notation** identifie une note par sont nom alphabetique avec un nombre identifiant l'octave dans laquelle elle se situe, où l'octave commence par une note *C*.
Par exemple la fréquence $440Hz$ représente $A_4$ sans ambiguité, et les fréquences $220Hz$ et $880Hz$ représentent les notes $A_3, A_5$ respectivement.

Dans le protocole **MIDI**, le notes sont représentées par un nombre entier, il permet de coder plus de 10 octave en partant de la note $C_{-1}$.

![La notation scientifique sur un piano](img/piano-keys.png){width=100%}

## Reconnaissance des notes

Un demi-ton est l'écart entre deux touches voisines sur un piano.
On voudrais savoir le rapport $r$ de fréquences associé à un demi-ton, sachant que l'octave double la fréquence on peut conclure facilement :
$$ r^{12} = 2 \Rightarrow r=2^{1/12} $$

On souhaite ramener l'espace de fréquences $(\mathbb{R},\times)$ à l'espace $(\mathbb{N},+)$ tel que $\boxed{\text{demi-ton}\equiv 1}$.
On définit donc une bijection
$$\forall f\in]0,\infty[, f\mapsto 12 \log_2 f $$
En arrondissant le résultat à la valeur entière la plus proche, on obtient un espace linéaire discrèt correspondant aux notes.

Il sera convenient d'obtenir les mêmes notes du protocole **MIDI** vu qu'il est très bien établi et très utilisé.
Pour cela, on effectue une petite translation, en partant de la note de référence
$A4\equiv 69_{\text{MIDI}} \equiv 440Hz$.

$$\begin{cases}
\varphi:f\mapsto 12\log_2 f + c_{\text{ref}}\\
\varphi(440) = 69
\end{cases}\Rightarrow c_{\text{ref}} = 69 - 12\log_2 440$$
Par conséquent, la bijection $\varphi$ est définit par :
$$\varphi: ]0,\infty[ \rightarrow \mathbb{R} : f \mapsto 12\log_2 f + c_{\text{ref}}
\quad\text{avec } c_{\text{ref}}=69 - 12\log_2 440$$
On note $\bar{\varphi}$ la fonction définit par
$\bar{\varphi}(f)=\left\lfloor\varphi(f)\right\rceil\in\mathbb{Z}$
où $\lfloor\cdot\rceil$ est la fonction d'arrondissement à l'entier le plus proche.

On peut donc obtenir les nombres MIDI de notes à partir des fréquences fondamentales grâce à la fonction $\bar{\varphi}$.

Néanmoins, le nombre MIDI n'est pas suffisant pour identifier une note, car certaines notes ont la même fréquence en accord tempéré et donc le même nombre midi (i.e. la même touche sur un piano),
par exemple $\text{MIDI}(C\#)=\text{MIDI}(D\flat)$.
Pour distinguer ces notes il est nécessaire de trouver la gamme du morceau.

## Reconnaissance de la gamme/l'armature

Dans cette étude, on ne s'intéressera aux notes dans une octave. On introduit donc la fonction $\psi$ :
$$\psi: ]0,\infty[ \rightarrow [0,12[ : f \mapsto \psi(f) \mod 12$$
De même, on définit la fonction $\bar{\psi}$ telle que
$\bar{\psi}(f)=\left\lfloor\psi(f)\right\rceil$.
On voit que $\mathrm{Im}(\bar{\psi})=\mathbb{Z}/12\mathbb{Z}$

|       Note      | C |   | B |   | E | F |   | G |   | A |   | B |
|-----------------|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| $\bar{\psi}(f)$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10| 11|

En musique classique, ils existent 4 types de gammes, on ne s'intéressera qu'à un : *la gamme majeure*.
Comme on l'a déjà dit, une gamme est caractérisée par sa première note et la suite des intervalles.
Dans la gamme majeure, les intérvalles en fonction du ton sont :
1--1--½--1--1--1--½.

La gamme *Do/C Majeur* contient donc les notes {0, 2, 4, 5, 7, 9, 11}.

De même, la gamme *Sol/G Majeur* contient les notes {7, 9, 11, 0, 2, 4, 6}.
Ces gammes diffèrent par une note, la note 5$\equiv$F est remplacée par la note 6 qui correspond à F# ou G$\flat$. Dans le contexte du Sol Majeur, on sait que 6$\equiv$F# car la gamme contient déjà 7$\equiv$G.

On voit bien que l'identification de la gamme est *nécessaire* pour la distinction entre certaines notes.

Une gamme peut être alors identifié par son ensemble de notes qu'on notera $G$ tel que
$G\subset\mathbb{Z}/12\mathbb{Z}, |G|=7$.
On définit le vecteur $g\in\left\{0,1\right\}^{12}$ associé à $G$ tel que
$$ g_i = \mathbb{1}_G(i) =
\begin{cases} 1 & \text{si } i\in G\\ 0 &\text{sinon}\end{cases}$$
On définit donc $E$ l'ensemble de gammes majeures.

Soit $F$ l'ensemble de fréquences fondamentales obtenues,
soit $S=\bar{\psi}(F)\subset\mathbb{Z}/12\mathbb{Z}$,
soit $p:{Z}/12\mathbb{Z}\rightarrow\mathbb{N}:n\mapsto\text{le nombre d'occurances de $n$ dans le morceau}$.
On note $p_{\max}=\max\limits_{n\in S} p(n)$.
On définit le vecteur $x\in\left[0,1\right]^{12}$ tel que $x_i=\frac{p(i)}{p_{\max}}$.

La gamme du morceau est alors la solution du problème d'optimisation
$$ \min\limits_{g\in E}\quad \lVert g-x \rVert $$
En musique classique, $\lvert E\rvert = 12$ donc le problème d'optimisation ne nécessite pas une résolution mathémtique avancée.

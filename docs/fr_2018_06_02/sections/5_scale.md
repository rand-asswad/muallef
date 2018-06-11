# Théorie de musique
La théorie de la musique permet, à la fois de réglementer la musique et
de la libéraliser.

## Notions de base

La **note** est le plus petit objet musical, porte un nom, et caractérise la hauteur tonal du son (fréquence).
Dans le contexte d'un morceau musical, une note caractérise aussi la durée de cet objet.

Un **intervalle** se définit musicalement par l'écart de hauteur tonal entre deux notes.
Scientifiquement, un intervalle est le ratio de fréquences fondamentales de deux notes.

On appelle **_octave_** l'intervalle correspondant au ratio $2:1$
Les notes d'un octave porte le même nom.

Une **échelle** musicale est une suite d'intervalles conjoints.
Une **gamme** musicale est une suite de notes conjointes, la dernière répétant
la première à l'octave.

L'**armure** — ou l'**armature** (*en:* **key signature**) — est un ensemble d'altérations réunies à la clé.
Elle est composée soit exclusivement de dièses, soit exclusivement de bémols — en dehors du cas particulier constitué par le changement d'armure.
Ces altérations correspondent à la tonalité principale des mesures suivant la clé.

Ils existent plusieurs théories de musique qui diffèrent principalement
par la composition d'échelles et de gammes.
Dans ce projet nous avons considéré la théorie de la musique occidentale
basée sur l'accord tempéré.

## Tonalité

### Généralités
- L'unité de tonalité est le **_ton_**.
- En musique classique, le plus petit intervalle est d'un **_demi-ton_**.
- Un octave est composée de 6 tons, soit 12 demi-tons.
- L'échelle majeure classique est composée des intervalles:
1--1--½--1--1--1--½.
- La gamme majeure classique est composée de 7 notes distinctes
(la 8^ème^ est à l'octave de la première).
- **Le dièse (#)** est une altération qui lève une note d'un demi-ton.
- **Le bémol ($\flat$)** est une altération qui baisse une note d'un demi-ton.

### Les notes
Les notes principales sont les touches blanches d'un piano.
Les touches noirs d'un piano sont des notes altérées.

![](img/intervalles-piano.png)

- Noms français: do-ré-mi-fa-sol-la-si
- Noms alphabétiques: C-D-E-F-G-A-B

**Remarque:** Certaines notes altérées sont des touches blanches
(e.g. Mi#=Fa$\equiv$touche blanche), sans détailler sur les altérations
composées (doubles dièses, doubles bémols).

### Nomenclature
Ils existent plusieurs systèmes de nomenclature de notes de musique.
Le système utilisé en France adopte les noms en termes de *Do-Ré-Mi-Fa-Sol-La-Si*.
De plus, il existe un système basé sur l'alphabet latin : *C-D-E-F-G-A-B*.
Les deux systèmes sont très utilisés, dans ce projet on utilisera le dernière pour simplifier.

Vu que les noms des notes se répètent au bout d'un octave, il faut distinguer une note *LA* de fréquence $440Hz$ d'une autre de fréquence $220Hz$ ou $880Hz$.

Le système de notation scientifique **Scientific Pitch Notation** identifie une note par sont nom alphabetique avec un nombre identifiant l'octave dans laquelle elle se situe, où l'octave commence par une note *C*.
Par exemple la fréquence $440Hz$ représente $A_4$ sans ambiguité, et les fréquences $220Hz$ et $880Hz$ représentent les notes $A_3, A_5$ respectivement.

Dans le protocole **MIDI**, le notes sont représentées par un nombre entier, il permet de coder plus de 10 octave en partant de la note $C_{-1}$.

![La notation scientifique sur un piano](img/piano-keys.png){width=100%}

### Les gammes classiques

À chaque tonalité majeure est associée une tonalité en mode mineur, présentant la même armure de clef et appelée relative mineure.

![Le cycle des quintes](img/cycle-des-quintes.png){width=50%}

Pour simplifier, on va considérer la théorie de la musique occidentale basée sur l'accord tempéré (depuis le XVIII^e^ siècle).
Dans ce cas, l'intervalle séparant la première et la dernière note d'une gamme est dite *octave*, une octave se divise en 12 écarts égales appelés *demi-tons*.
La dernière note porte le même nom de la première dans la gamme.

![Les intervalles sur un piano](img/intervalles-piano.png){width=100%}

## Tonalités & Fréquences

L'espace de notes est un espace linéaire discrèt, mais l'espace de fréquences est continue non-linéaire.
Par exemple, la l'intervalle entre A3 et A4 est un octave, celui entre A4 et A5 également.
En revanche, $f(A3)=220Hz, f(A4)=440Hz, f(A5)=880Hz$, on voit bien que la relation est logarithmique.
Le problème consiste à trouver une fonction qui associe les fréquences fondamentales obtenues avec des valeurs entières.

### Le protocole MIDI

On voudrais savoir le rapport $r$ de fréquences associé à un demi-ton, sachant que l'octave double la fréquence
on peut conclure facilement:
$$ r^{12} = 2 \Rightarrow r=2^{1/12} $$

On souhaite ramener l'espace de fréquences $(\mathbb{R},\times)$ à l'espace $(\mathbb{N},+)$
tel que $\boxed{\text{demi-ton}\equiv 1}$. On définit donc une bijection
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
On voit que $\mathrm{Im}(\bar{\psi})=\mathbb{Z}/12\mathbb{Z}$.

\vspace{-1em}
|       Note      | C |   | D |   | E | F |   | G |   | A |   | B |
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
$$ g_i = 1_G(i) =
\begin{cases} 1 & \text{si } i\in G\\ 0 &\text{sinon}\end{cases}$$
On définit donc $E$ l'ensemble de gammes majeures.

Soit $F$ l'ensemble de fréquences fondamentales obtenues,
soit $S=\bar{\psi}(F)\subset\mathbb{Z}/12\mathbb{Z}$.

On définit $p:{Z}/12\mathbb{Z}\rightarrow\mathbb{N}:n\mapsto\text{le nombre d'occurances de $n$ dans le morceau}$.

On note $p_{\max}=\max\limits_{n\in S} p(n)$.
On définit le vecteur $x\in\left[0,1\right]^{12}$ tel que $x_i=\frac{p(i)}{p_{\max}}$.

La gamme du morceau est alors la solution du problème d'optimisation
$$ \min\limits_{g\in E}\quad \lVert g-x \rVert $$
En musique classique, $\lvert E\rvert = 12$ donc le problème d'optimisation ne nécessite pas une résolution mathémtique avancée.

## Implémentation

Nous pouvons tester cet algorithme sur notre morceau:

```{python}
from muallef.utils.units import convertFreq
from muallef.notes import scale, name
from muallef.utils.io import plot_step_function

midi = convertFreq(f, "Hz", "MIDI")
plt.clf()
fig = plt.figure()
ax = fig.add_subplot(111, ylim=(50,80))
plot_step_function(t, midi)
plt.show()

base_note = scale.detect_scale(midi)
nb_alt, tone = scale.scale_signature(base_note)
print("Major scale: ", name.octave_note_name(base_note, tone))

key_signature = ""
if tone > 0:
    for i in range(nb_alt):
        key_signature += name.octave_note_name(scale.sharp[i], tone) + " "
    key_signature += "\t/\t"
else:
    for i in range(nb_alt):
        key_signature += name.octave_note_name(scale.flat[i], tone) + " "
print("Key signature: ", key_signature)
```

En comparant avec la partition original de la fameuse Csárdás:

![Partition de la Largo de Csárdás (Vittorio Monti) pour violon](img/czardas_partition.png)

On voit bien un bémol à la clé *(Fa majeur)*.

## Tempo et rythme

le temps en musique se définit par le tempo et le rythme.

On définit d'abord **un temps** (en: **_beat_**) l'unité de temps en musique.

Le **tempo** du morceau est sa vitesse, il peut être décrit en **BPM** (Beats per minute, fr: *temps par minute*)
ou bien par un mot clé en italien: *Largo, Andante, Allegro, Moderato, Lento, Presto, etc* ce qui
est moins précis mais bien compris par les musiciens.

Le **rythme** du morceau est sa structure répétitive qui définit une pulsation régulière.

La **mesure** est une structure *rythmique* constitutées de plusieurs *temps* qui se répète périodiquement. 

![Rythme et tempo](img/rythme.png)

La **métrique** (la division du temps) est le nombre de temps par mesure *et* la valeur d'un temps.
Ce sont les 2 chiffres au début d'un morceau, celui en bas indique le temps:

| **Temps**  | ronde | blanche | noire | croche | double-croche |
|:----------:|:-----:|:-------:|:-----:|:------:|:-------------:|
| **Nombre** |   1   |    2    |   4   |   8    |      16       |

Celui en haut indique le nombre de temps (beats) par mesure, par exemple $\frac{3}{4}$ est la métrique
qui contient 3 noires par mesure. Les unités les plus utilisées sont les noires et les croches,
et rarement la blanche.

## Relation entre le temps et tempo

Il se peut que la métrique soit changé dans un morceau. De plus, le tempo n'est pas forcément constant.
Même son évolution au cours du morceau n'est pas toujours linéaire, on peut ralentir au milieu d'un
morceau jusqu'à l'arrêt total pour reprendre en plein vitesse d'un seul coup.

On n'a donc aucune guarantie sur la régularité du tempo.

En revanche, afin de pouvoir tirer des résultats de notre analyse précédantes on a dû prendre
des cas particuliers suffisamment réguliers. Par la suite, nous avons définit un **pseudo-PGCD**
de durées de notes, et nous avons divisés toutes les durées par ce nombre, et puis en arrondissant
le résultats nous avons obtenus des résultats qu'on a écrit en format MIDI.

## Ecriture en format MIDI

On reprend le morceau du piano afin d'obtenir une fonction constante par morceau
avec le temps en *beats*, ce qu'on enregistra en format MIDI
grâce à la librarie python `midiutil`

```{python}
from muallef import notes

time, pitch = notes.detect(fur_elise.signal, fur_elise.sampleRate)
plt.clf()
plot_step_function(time, pitch)
plt.show()

notes.extract.extract_midi(time, pitch, "fur_elise.midi")
```

On compare la partition obtenue avec la partition originale:

![Partition obtenue](img/fur_elise_midi.png)

![Partition obtenue](img/fur_elise_partition.png)

On n'a pas obtenu les résultats qu'on espérait avoir, ceci pourra être expliqué
par 3 raisons:

- Notre implémentation ne traitent que les son monophones, mais ce morceau
contient plusieurs notes simultanées différentes.
- Le morceau est en La mineur (même armure que Do majeur), une gamme sans altérations.
Or, dans les 2 lignes qu'on a traités nous avons croisé 3 dièses, d'où l'erreur
dans le choix de la gamme.
- Notre traitement du tempo est très élèmentaire, ici on a une métrique composée
ce qui est un cas assez délicat pour tel programme.


En revanche, la ségmentation temporelle et la détéction de pitch sont bien réussis.

\pagebreak

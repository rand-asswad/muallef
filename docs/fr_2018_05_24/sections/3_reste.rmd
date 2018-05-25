# Le traitement en cours de développement
## Post-traitement
Les résultats obtenus sont certainement intéressants.
Or, il y a des notes courtes enregistrés qui ne sont que du bruit capté lors des changements de notes.
On a essayé d'éliminer ces notes en supprimant les notes courtes, mais on a perdu certaines notes importantes.

Nous avons observé une relation entre les maximums locaux de l'envelope du signal et le changement de notes, ce qui nous a poussé à trouver une solution qui permet d'identifier ces changements correctement.
Nous avons donc cherché une méthode mathématique perméttant d'extraire telle fonction. Par conséquent, on a trouvé plusieurs méthodes intéressantes dites en anglais **Onset Detection**.

Notre idée de base ne constitue qu'une partie de la solution.
En effet, l'identification des *Onsets* ou *Débuts* s'effectue en deux étapes:

1. Calculer une fonction dite **Onset Detection Function** ou parfois **Onset Strength Signal (OSS)** dont les maximums locaux correspondent aux *Onsets*.
2. **Peak Selection** : il s'agit d'une méthode de sélection de maximums locaux.

Ils existent plusieurs fonctions OSS utilisées dans le domaine temporel, fréquentiel, ou complexe. Qui permettent de quantifier l'énergie du signal et/ou les changements dans la fréquence fondamentale.

Pour la deuxième étape, on introduit souvent un seuil afin d'éliminer les points avec un OSS petit.
En général, le seuil n'est pas constant, il se calcul à partir de la fonction OSS par des méthodes statistiques comme la moyenne mobile.

On choisira après les points de l'OSS supérieurs au seuil et maximals dans un voisinage petit qu'on fixe.

## La reconnaissance du rythme
Sans le rythme, la partition ne peut être écrite. Vu qu'on n'a pas encore fini le traitement, nous ne pouvons pas passer à cette étape, le projet se restreint à un outil de conversion en format MIDI.

Si vous pouvez nous guider dans cette étape, ça sera encore mieux pour nous.

## Etape finale
Une fois le *tempo* indentifié, les résultats se transforment facilement en format MusicXML qui peut être extrait facilement en format PDF grâce aux libraries existantes.

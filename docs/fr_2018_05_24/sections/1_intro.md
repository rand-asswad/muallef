# Introduction

## Idée du projet
Le but du projet est de créer un logiciel de transcription automatique de morceaux de musique, dans le cadre du projet semestriel on vise créer un version capable de traiter des morceaux monophoniques.

## Idée de traitement
On part du principe qu'un signal sonore est une série harmonique, ce qui sera expliqué en détails dans le rapport final du projet.

A partir du signal harmonique on extrait la fréqence fondamentale en fonction du temps, par la suite on transforme les fréqences en notes.
Par la suite, on analyse les notes pour obtenir une suite de notes associées avec des durées.

L'étape finale fait appelle à la théorie de musique, elle consiste à extraire le *tempo* à partir des durées des notes, et de reconnaitre la *gamme* du morceau à partir des notes obtenues.


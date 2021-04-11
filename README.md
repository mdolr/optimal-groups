# Projet

## Sources & documentation

- [The Hungarian Method, Mark J. Becker, Wolfgang F. Riedl, Aleksejs Voroncovs; Technische Universität München](https://www-m9.ma.tum.de/graph-algorithms/matchings-hungarian-method/index_en.html)
- [Hungarian Algorithm II, Yasen Hu](https://yasenh.github.io/post/hungarian-algorithm-2/)

## Fonctionnement

Application de l'algorithme d'association optimale de Kuhn

## Exemple

### Avant optimisation

Graphique représentant les groupes reliés aux différents projets avec leurs préférences propres à chaque projet.

![Graph de départ](https://i.imgur.com/ZDgmpm9.png)

### Après optimisation

Graphique représentant chaque groupe assigné à un projet selon l'algorithme d'association optimale de Kuhn.

![Graph du résultat](https://i.imgur.com/D3OjzFH.png)

# Mode d'emploi

## Prérequis

- Python > 3.6.5
- pip > 20.0.2

## Installation

1. `git clone repository_url`
2. `pip install -r requirements.txt` ou `pip3 install -r requirements.txt` selon environnement.

## Utilisation

Pour lancer le programme sans arguments `python main.py`

### Arguments

- `--debug` pour observer le fonctionnement de l'algorithme étape par étape avec une visualisation des graphs.
- `-g /chemin/vers/le/fichier.csv` pour préciser le fichier d'entrée contenant les groupes et leurs préférences
- `-p /chemin/vers/le/fichier.csv` pour préciser le fichier d'entrée contenant les projets et leur capacité
- `-o /chemin/vers/le/fichier.txt` pour préciser l'endroit où le fichier de sortie sera créé.

## Données

Les fichiers d'entrée doivent être au format CSV.

### Groupes

En-tête du fichier des groupes, [voir exemple](https://github.com/mdolr/affectation-groupe/blob/main/groupes.csv)

```
Groupe,Preference1,Preference2,Preference3,Preference4,Preference5
```

### Projets

En-tête du fichier des projets, [voir exemple](https://github.com/mdolr/affectation-groupe/blob/main/projet.csv)

```
projectName,capacity
```

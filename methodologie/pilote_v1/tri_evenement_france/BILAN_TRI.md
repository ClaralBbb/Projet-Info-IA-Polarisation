# Tri documentaire du pilote : France entière

Le tri des 50 commentaires du pilote est terminé. Il s’agit de propositions de rattachement documentaire, pas d’une vérification des images ou des événements. Les annotations d’opinion et le dashboard n’ont pas été modifiés.

## Résultat au niveau des commentaires

| Rattachement proposé | Nombre |
| --- | ---: |
| Lien plausible avec la mobilisation, non confirmé | 17 |
| Contexte général ou comparaison | 23 |
| Autre événement explicitement évoqué | 4 |
| Informations insuffisantes | 6 |

Ces nombres décrivent un petit échantillon sélectionné, pas la fréquence des opinions dans l’ensemble du corpus. Le contexte général reste utile pour l’analyse des arguments, mais ne doit pas devenir une preuve de faits survenus le 17.

## Vérification des vidéos distincte de celle des commentaires

Les métadonnées publiques des 50 vidéos ont été récupérées par l’API YouTube : titres, chaînes déclarées, dates de publication et descriptions. Sur cette base, 43 vidéos présentent un lien plausible, 4 concernent des suites ou d’autres dates liées, 1 évoque 1961, 1 présente une contradiction de date et 1 manque d’indices de datation des faits.

La date de publication ne suffit jamais à dater les scènes. Les descriptions sont celles disponibles lors de la récupération, pas nécessairement celles publiées initialement. Les noms de chaînes ne certifient ni l’authenticité de l’éditeur ni la véracité du contenu. Une chaîne étrangère peut présenter des événements français.

## Cas qui changent l’interprétation

- **N001** : la vidéo décrit la France, mais le commentaire parle de la police indienne. Les deux niveaux sont séparés.
- **N006** : la description de FRANCE 24 conteste l’authenticité des images d’un couple prétendument agressé. Le commentaire peut être analysé comme discours sur une information contestée; il ne prouve pas cette agression. Aucune vérification indépendante effectuée ici.
- **N011** : référence explicite à 1961, malgré une publication en 2026. Hors du corpus principal de la mobilisation recherchée.
- **N015 et N025** : allégations graves de décès attribué à la police, non corroborées dans cette revue.
- **N017, N018 et N050** : les descriptions rattachent les débats rétrospectifs au 17; une publication ultérieure n’est pas un motif d’exclusion.
- **N023, N032, N035 et N037** : nouveaux rassemblements ou appels ultérieurs, conservés comme suites distinctes.
- **N026** : titre « 7 octobre », description « 17 octobre »; contradiction laissée ouverte.
- **N028** : publication le 17 et mention de Paris, mais pas de datation des scènes dans le titre ou la description.

## Méthode et traçabilité

Lecture documentaire par l’assistant des textes, parents disponibles, titres et descriptions. Les décisions explicites figurent dans `decisions_documentaires_50.json`, avec preuves textuelles et motifs. `metadata_api_snapshot.json` archive les métadonnées obtenues. `construire_tri.py` exporte ces décisions sans les inventer : il ne constitue pas un classificateur généralisable. Aucun modèle via API, visionnage ou validation humaine supplémentaire n’a été exécuté.

Le fichier `TRI_50_FRANCE.xlsx` contient les commentaires et parents complets, les métadonnées, les deux statuts et les signalements. Ouvrir une cellule pour lire les textes longs. Les cellules sont du texte, pas des formules. Aucune nouvelle annotation n’est demandée à l’utilisatrice pour ce livrable.

## Suite

Le tri permet de distinguer les candidats au corpus principal, le contexte et les exclusions. Il ne valide pas encore un corpus de 10 000 commentaires. Avant une extension, il reste à résoudre les rattachements incertains, fixer le traitement des suites et des informations contestées dans les statistiques, puis adapter le script LLM au JSON V1. Le futur test doit comparer les sorties automatiques à des annotations humaines indépendantes. Aucun appel LLM payant n’est lancé par cet export.

Relancer l’export depuis la racine du dépôt :

```sh
.venv/bin/python methodologie/pilote_v1/tri_evenement_france/construire_tri.py
```

Les décisions sont rejouables sur ces 50 commentaires. Des commentaires supplémentaires nécessitent de nouvelles décisions documentaires ou un classificateur évalué.

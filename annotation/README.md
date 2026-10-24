# Pilote : positions sur la police et les violences

## Ordre de travail

1. Ouvrir **exemples_ia_20.xlsx** : 20 commentaires, leurs parents disponibles,
   et 22 positions proposées par l'assistant conversationnel. Lire Guide,
   Commentaires puis Positions IA. Noter les corrections dans Relecture humaine.
   Ce sont des propositions à discuter, pas une vérité de référence.
2. Discuter les cas ambigus et stabiliser la grille (version 0.1 actuellement).
   Ces exemples pourront servir d'exemples de consigne pour la classification.
3. Ensuite seulement, ouvrir **evaluation/pilote_police_violences_100.xlsx**.
   Annoter les commentaires et leurs positions sans consulter de prédictions IA.
   Ce lot ne contient aucun des commentaires ni aucune des vidéos des 20 exemples.
4. L'assistant annotera ce même second lot séparément, après gel de la grille.
   Comparer sur les mêmes textes : pertinence, acteur, objet, position, preuve et
   positions oubliées. L'IA doit pouvoir produire plusieurs positions par texte.
   Conserver les annotations humaines et IA séparément.
5. Si la grille est modifiée à partir des résultats du second lot, celui-ci
   devient un lot de développement. Prévoir alors un nouveau test indépendant.

Aucun appel à une API LLM et aucun coût API supplémentaire pour ces fichiers.
Les annotations IA du lot pilote ont été rédigées par l'assistant dans la
conversation, guidé par la grille et les exemples fictifs, pas par un script
ayant appelé un modèle à distance. Le modèle et sa version ne sont pas figés :
ce pilote ne constitue donc pas encore une procédure automatique reproductible.

## Fichiers et sélection

- `exemples_ia_20.xlsx` : démonstration annotée et onglet de relecture humaine.
- `exemples_ia_20.json` : décisions proposées, version de grille et exclusions.
- `evaluation/pilote_police_violences_100.xlsx` : contexte + annotations vides.
- `evaluation/selection.json` : identifiants, lexique et graine du deuxième lot.
- `grille.md` : consignes de décision communes.

Présélection par mots-clés uniquement. La pertinence n'est pas garantie.
Les textes complets ne sont pas réduits aux mots-clés. Pour une réponse, le
parent référencé est joint; il ne représente pas tout le fil de discussion.
Les titres de vidéos sont disponibles, mais aucune vidéo n'a été visionnée
ou validée pour ce pilote. Des titres mentionnent d'autres villes ou dates.
La pertinence du sujet et celle de la vidéo pour Paris le 17 octobre sont
**deux questions distinctes**.

Le lot de travail initial utilise la graine 20261024, 50 commentaires principaux
et 50 réponses, des textes normalisés distincts et deux commentaires maximum
par vidéo. Ses 20 premiers commentaires constituent la démonstration IA.
L'évaluation utilise les mêmes règles après exclusion des vidéos du pilote.
Ce sont des échantillons d'apprentissage de la méthode, pas des échantillons
représentatifs de l'opinion publique ou des commentaires du corpus.

Reproduire le lot initial : `.venv/bin/python prepare_annotation.py`.
Reproduire le lot d'évaluation :

```bash
.venv/bin/python prepare_annotation.py \
  --exclude annotation/exemples_ia_20.json --output annotation/evaluation
```

Les textes peuvent contenir des propos offensants et des données personnelles.
Ne pas attribuer aux auteurs les opinions exprimées seulement dans leur parent.

## Qu'est-ce qui a réellement été exécuté ?

| Élément | Statut | Où le voir |
| --- | --- | --- |
| Sélection lexicale, échantillonnage, jointure du parent, export Excel | Code Python exécuté | `../prepare_annotation.py` |
| 20 commentaires et 22 positions proposés par l'assistant | Annotation conversationnelle, sans appel API | `exemples_ia_20.xlsx`, `exemples_ia_20.json` |
| Grille des catégories et règles de décision | Document de méthode pilote | `grille.md` |
| Consigne structurée avec exemples d'entrée/sortie | Proposition pour les prochains traitements, pas journal d'exécution | `prompt_classification.md` |
| Classification automatique few-shot des commentaires | **Non implémentée et non exécutée** | Aucun script de classification API à ce stade |

Il n'existe donc pas de programme ni de journal d'appels permettant de rejouer
exactement les 20 décisions conversationnelles. Les citations justificatives
permettent de les contrôler, mais ne sont pas une trace des calculs internes du
modèle. La consigne proposée est explicite et inspectable; elle ne doit pas être
présentée comme le prompt exact d'un appel automatique déjà réalisé.

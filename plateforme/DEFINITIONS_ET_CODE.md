# Où regarder les définitions et les regroupements

## 1. Sujet, acteurs et actions

Voir [`actor_scope.py`](../actor_scope.py) :

- `SUBJECT` : sujet unique « Violences et dégâts ».
- `ACTORS` : catégories d'acteurs évalués.
- `ACTIONS` : actions discutées, distinctes des acteurs.
- `RULES` et les appels à `group(...)` : revue explicite des positions existantes.
- `project(ordre, index)` : projection d'une position dans la nouvelle présentation.
- `aggregate(items)` : calcul commentaire×acteur, catégorie mixte et pourcentages.

Un couple `(65, 0)` désigne la première position du commentaire numéro65 du lot;
il se retrouve dans `annotations_lot02.json`, via `ordre_lot` et l'ordre de
`annotation.positions`. Ce n'est ni une règle universelle ni une extraction LLM.

Les commentaires initialement pertinents au sens large ne sont pas tous retenus
pour cette comparaison : les lignes exclues restent présentes dans le nouvel
Excel avec un motif. L'attribution de l'acteur est une décision de lecture,
pas une vérification de qui a matériellement commis les faits.

## 2. Familles d'arguments

Voir [`actor_scope.py`](../actor_scope.py), les constantes `ARGUMENT_FAMILIES`
et la fonction `argument_families(ordre, index, arguments)`.

Familles : coût et conséquences matérielles; protection des personnes/commerces;
violences antérieures ou punition invoquées; absence d'écoute/dialogue; risque
d'escalade; autres justifications explicites.

Les couples `(numéro, position)` sont des décisions de regroupement **manuelles
et exploratoires**. Par exemple `(87,0)` invoque des violences antérieures,
mais `(87,1)` invoque le risque d'escalade : les deux positions d'un même texte
ne doivent pas recevoir automatiquement le même argument.

Ces listes ne suffisent pas pour classifier les commentaires restants, ne prouvent
pas la validité d'un argument et peuvent être contestées. Le texte exact de chaque
argument reste affiché avec sa preuve. Sans argument enregistré, aucune famille
n'est attribuée. Les familles sont non exclusives; leur somme peut dépasser le
nombre de commentaires.

[`build_platform.py`](../build_platform.py) assemble ces définitions et annotations
pour l'affichage; ce n'est pas un programme de classification des opinions.

## 3. Les annotations qui alimentent les règles

- [`annotations_60.json`](annotations_60.json) : premier lot.
- [`annotations_lot02.json`](annotations_lot02.json) : commentaires61–90.
- [`pilote_revise.json`](pilote_revise.json) : corrections du pilote humain.
- [`grille0.3`](../annotation/grille_v03_sujet_acteur_action.md) : méthode actualisée.

Ces résultats viennent de lectures de l'assistant dans la conversation, pas d'un
programme ayant appelé un LLM via API. Le programme de site affiche les décisions;
il ne les invente pas à partir de la présence d'un mot-clé.

## 4. Nouvel Excel

`ANALYSE_V4_sujet_acteurs_positions.xlsx` sépare le sujet, l'acteur évalué, l'action,
la position, les arguments, les preuves et les incertitudes. Toutes les118 positions
sont conservées;66 sont retenues pour le sujet avec les règles actuelles, avant
filtre de lecture explicite. Ne pas confondre118 positions et90 commentaires.
Le fichier n'écrase pas la relecture humaine et ne demande aucune annotation nouvelle.

## 5. Chaînes

Le lot de500 provient de188 chaînes déclarées : médias et autres comptes trouvés
par recherche YouTube. La présence d'un média connu n'est pas une sélection
exhaustive de ses vidéos ni une validation d'authenticité de son compte. Les
comparaisons concernent les commentaires sous les vidéos, pas l'avis des chaînes.

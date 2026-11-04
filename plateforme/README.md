# Tableau de bord de résultats — version 3

**90 commentaires traités, 118 positions proposées, 410 commentaires restants.**
Aucune nouvelle annotation n'est demandée à l'utilisatrice. Cette version présente
les résultats et leurs limites; la lecture détaillée est facultative.

## Consulter

- `RESULTATS_V3_90_commentaires.html` : télécharger et ouvrir dans un navigateur.
- `apercu_resultats.png` : aperçu des graphiques, visible directement sur GitHub.
- `tableau_de_bord.html` et `../docs/index.html` : même version de l'interface.

Le nouveau nom évite de rouvrir une ancienne copie déjà téléchargée. Le fichier
est autonome, sans clé ni serveur. L'adresse web publique n'est pas activée.
L'API GitHub de configuration Pages a renvoyé Forbidden depuis cet environnement;
l'hébergement n'a donc pas pu être configuré ou vérifié ici. Si disponible dans
le dépôt : Settings → Pages → Deploy from a branch → main → /docs. Vérifier sa
visibilité avant publication. Le fichier téléchargé fonctionne sans cette étape.

## Ce qui a changé

1. Graphiques recalculés par objet, chaîne et type de commentaire, avec option
   de ne retenir que les lectures explicites.
2. Comparaison des critiques, soutiens, nuances et observations **sur le même
   objet**. Critique d'une force excessive et reproche d'inaction sont séparés.
3. Familles d'arguments explicitement enregistrés : coûts matériels, protection,
   violences antérieures invoquées, absence d'écoute/dialogue, autres raisons.
4. Tableau des objets et des positions, exemples contrastés lorsqu'ils existent.
5. Comparaisons par chaîne et vidéo avec effectifs et avertissement de faible
   volume. Ce ne sont pas les opinions des médias et leurs comptes ne sont pas
   authentifiés par cette analyse.
6. Synthèse de la sélection et export CSV des effectifs filtrés.
7. Commentaires, parents et preuves accessibles depuis les résultats. Aucun
   nouveau formulaire de relecture obligatoire.

Les anciens exports de relecture locale restent récupérables depuis une section
repliée, si le navigateur et l'origine utilisés les ont conservés. Une copie
locale HTML et une URL HTTP ont des stockages séparés; aucun transfert automatique.

## Corrections humaines intégrées

`../revise_pilot.py` applique des révisions explicites au pilote; les propositions
initiales et la relecture humaine restent intactes. Résultat : `pilote_revise.json`.

- C003 : précision génération Z / jeunes manifestants.
- C005 : explication causale, pas soutien automatique à la violence.
- C006 : parti de Mélenchon et violence attribuée au parti, pas dégâts matériels
  automatiquement déduits.
- C007 : comportements non précisés, argument non inventé, position supplémentaire
  sur Sarkozy. Ajouter une position ne remplace pas celle sur les manifestants.
- C008 : contestation ciblée sur les retraités, pas rejet de tout le parent.

14 lignes de retour humain renseignées; 8 sans verdict restent non relues.
Le désaccord sur C002 est conservé, pas résolu automatiquement. Ce pilote a servi
à développer la grille, pas à calculer une précision indépendante du modèle.
La section « corrections intégrées » du tableau présente ces changements.

## Données et méthode

`annotations_60.json` conserve le premier lot; `annotations_lot02.json` ajoute
30 textes (lignes 61–90). Les décisions sont proposées dans la conversation par
l'assistant après lecture des textes et parents. Aucun appel API, aucun modèle
API/version figés; ce n'est pas une exécution automatique de Structured Outputs.
Chaque résultat est contrôlé contre le schéma local et chaque preuve contre le
texte source. La justesse sémantique reste à évaluer.

`build_platform.py` ne classe pas les commentaires : il rassemble les résultats
et leur applique des regroupements exploratoires explicites pour l'affichage.
Pour les interventions, une liste documentée de numéros de commentaires sépare
force/répression, présence/efficacité et autres jugements. Les familles d'arguments
ne sont attribuées que si un argument est déjà enregistré. Ces regroupements
restent des choix analytiques, consultables dans le code et à valider.

Les effectifs comptent les commentaires distincts **par catégorie**; un texte
multi-position peut contribuer à plusieurs catégories. Seules les positions
attribuées à l'auteur sont agrégées. La sélection initiale repose sur des
mots-clés et un maximum de deux commentaires par vidéo. Les résultats ne
représentent ni les 500 textes non entièrement traités ni l'opinion publique.
La couverture de Paris le 17 octobre et les accusations ne sont pas vérifiées.

`positions_analysees.csv` contient les 118 positions. `positions_60.csv` conserve
l'ancien export historique de 82 positions. `bilan.json` et `protocole.json`
présentent le statut actuel. L'empreinte des annotations et celle des entrées
permettent d'identifier les données affichées.

## Reproduire et vérifier

```bash
.venv/bin/python revise_pilot.py
.venv/bin/python build_platform.py
.venv/bin/python -m unittest -v
```

Contrôles navigateur, avec Playwright et Chromium disponibles :

```bash
python3 -m http.server 8765 --bind 127.0.0.1 --directory docs
# Dans un autre terminal :
node scripts/test_platform.cjs
```

Vérifiés : filtres des graphiques, comptages distincts, sélection d'une chaîne,
lectures explicites, accès aux exemples, export CSV et affichage mobile.
Le navigateur de cet environnement bloque les URL file://, donc le test utilise
un serveur local. Le HTML reste autonome, sans ressource distante ni traceur.

## Suite

Poursuivre les lots restants, valider le corpus et contrôler les erreurs avant
conclusions générales. Les convergences/divergences affichées sont des pistes
sur des objets comparables; pas de score arbitraire de clivage, de profils de
personnes ou de mesure validée de polarisation. Les textes peuvent contenir
insultes, données personnelles et accusations; l'étude ne les endosse pas.

## Version4 — sujet unique, acteurs et actions séparés

Le sujet principal est désormais **Violences et dégâts**. L'interface sépare
l'acteur évalué, l'action et la position. Les groupes d'acteurs principaux sont
police, manifestants et casseurs/pillards/émeutiers; autres autorités, autres acteurs
et acteur non établi restent séparés, sans attribution forcée.

Les pourcentages sont calculés par unité commentaire×acteur, avec dénominateur
séparé et une catégorie mixte si plusieurs attitudes coexistent. Par défaut,
lectures et attributions explicites seulement. Les positions portent sur des
actes précis et ne signifient pas un soutien global à une personne ou un groupe.

Code des définitions : `../actor_scope.py` (`ACTORS`, `ACTIONS`, `RULES`,
`ARGUMENT_FAMILIES`). Les familles d'arguments sont maintenant indexées par
position, afin de ne pas confondre deux raisons dans un même commentaire.
Le script `../build_platform.py` assemble les données sans classifier de nouveaux
textes. Voir `DEFINITIONS_ET_CODE.md` et la grille0.3.

Nouveaux fichiers :
- `RESULTATS_V4_acteurs_violences.html` : interface actualisée.
- `ANALYSE_V4_sujet_acteurs_positions.xlsx` : 118 positions conservées, sujet,
  acteur, action, position et contexte;66 retenues dans le sujet avant filtres.
- `statistiques_acteurs.json` : pourcentages et effectifs par acteur avec le
  filtre par défaut (lectures et attributions explicites).

Les annotations d'origine et la relecture humaine ne sont pas écrasées.
188 chaînes déclarées sont présentes dans le lot500 : pas seulement des médias.
Authenticité et couverture de l'événement ne sont pas validées.

### Lecture côte à côte — fichier V5

`VERIFICATION_V5_commentaires_et_positions.xlsx` s'ouvre sur **Vérification simple** :
commentaire complet, parent et classification/justification côte à côte. Les
colonnes avis/remarque sont facultatives. Les données détaillées V4 sont conservées
dans Positions et acteurs. Les textes ne sont pas tronqués; agrandir la barre de
formule pour les très longs commentaires. Aucun nouveau travail d'annotation
exhaustive n'est demandé. Les fichiers de relecture humaine existants sont intacts.

# Révision proposée après la relecture humaine reçue

Ouvrir **REVISION_01_retours_parent_arguments.xlsx**, onglet **Révision côte à côte**.
Le fichier conserve les20 commentaires /29 lignes et montre côte à côte les textes,
parents, propositions ajustées, retours humains exacts et décisions expliquées.
Les colonnes jaunes v2 sont facultatives et laissées vides. L'onglet Lecture
verticale permet de lire les textes longs sans masquage par la hauteur Excel.

## Ce qui a été revu

- **L033** : 1 commentaire,3 lignes de positions/fonctions, pas3 commentaires.
  La réponse défend les manifestants face à une généralisation du parent. Cette
  fonction interactionnelle est désormais explicite. La critique policière reste
  présente dans le texte; le parent ne l'annule pas. Aucune réfutation factuelle
  du reproche de non-travail n'est inventée. La hiérarchie des fonctions reste
  une proposition analytique à valider.
- **L059** : argument précis conservé; ARG_AUTRE signifie identifiable mais hors
  dictionnaire, pas absent. Candidat utilité préventive discuté séparément.
- **L005-P1** : A05 retiré; argument ambigu. Le non-travail est affirmé dans le
  texte, mais son rôle justificatif et le mécanisme de paiement ne sont pas
  suffisamment stabilisés pour coder un coût économique aux classes moyennes.
- **L005-P2** : allusion au karsher conservée pour trace mais retirée du périmètre
  principal conformément au retour humain.
- **L063-P1** : résumé précis conservé, A07 suspendu au profit d'ARG_AUTRE. Une
  catégorie sur des motivations opportunistes est proposée, sans l'activer.
- **L037-P1** : jugement général de police exclu du sujet précis. L037-P2 reste
  non exploitable, avec absence de verdict humain explicitée pour cette ligne.

16 lignes ont un retour;13 n'en ont pas. Aucun blanc n'est transformé en accord,
aucune précision du modèle calculée. Les accords sur un résumé ne valent pas
validation automatique de sa famille ou de toutes les positions du commentaire.

## Parent : nouvelle distinction proposée

Le parent peut être indispensable, utile ou sans nécessité selon la position.
Un commentaire répondant à un parent n'est ni automatiquement pertinent ni
automatiquement inutile. La pertinence dépend de ce qu'il exprime pour le sujet.

Pour L033, la critique policière peut être lue seule, mais le parent aide à
comprendre la défense du mouvement. Pour L070, le parent est indispensable pour
savoir quelle généralisation est contestée. Pour L042, il précise l'intervention
à laquelle renvoie « Pas sans raison ». La prise de position du parent n'est
jamais automatiquement attribuée à la réponse.

## Comment le dictionnaire a été constitué

Les A01–A12 et M01 sont des propositions manuelles issues de la lecture exploratoire
des90 textes. Aucune catégorie n'a été apprise automatiquement. La cible et la
valence ne définissent pas une famille : critiquer la police pour inaction et
pour force indiscriminée mobilise deux raisonnements différents.

Une famille doit réunir des raisonnements comparables, avec définition, critères,
frontières et citations. Avant toute généralisation, il faut relire les résumés
précis, chercher des récurrences et examiner les contre-exemples. ARG_AUTRE conserve
les arguments identifiables non couverts; on ne doit pas les forcer dans une
famille existante pour améliorer artificiellement les effectifs.

Les candidats du nouvel onglet ne sont pas validés :

- **Utilité préventive de l'intervention** : L059, un exemple clair dans le lot20.
  Ne pas inventer de second exemple ni fusionner automatiquement avec la critique
  de défaillance A01.
- **Motivations opportunistes attribuées aux auteurs de dégâts** : à discuter pour
  L063; rapprochements proposés avec les textes L046 et L085 déjà collectés.
  Les trois textes sont reproduits dans Exemples de récurrence. Leur présence ne
  valide pas encore la catégorie et les accusations des auteurs ne sont pas des faits.

Les définitions A01–A12/M01 originales sont conservées dans un onglet distinct.
La revue propose de retirer certains rattachements sans réécrire silencieusement
le dictionnaire validé (qui n'existe pas encore à ce stade).

## Traçabilité

- `relecture_humaine_recue.xlsx` : copie binaire intacte de la pièce jointe.
- `revision_proposee.json` : retours source exacts, journal avant/après, propositions
  et limites. Les parentés et citations sont contrôlées dans les textes source.
- `reviser_validation.py` : export des décisions explicites proposées dans cette
  conversation; aucun appel API, aucune nouvelle classification complète.

Le script régénère la copie révisée. Ne pas l'utiliser pour écraser un fichier
sur lequel une humaine a déjà saisi sa seconde relecture : sauvegarder celle-ci
sous un autre nom. Le dashboard, les annotations historiques et l'Excel source
restent inchangés. Seul ce nouveau dossier est ajouté au dépôt.

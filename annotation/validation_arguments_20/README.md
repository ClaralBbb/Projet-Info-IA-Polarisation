# Validation humaine — 20 commentaires et arguments provisoires

Ouvrir **VALIDATION_20_ARGUMENTS_PROVISOIRES.xlsx**, onglet **Vérification**.
Commentaire original, parent et proposition d'annotation sont côte à côte.
Les colonnes jaunes sont vides et réservées aux corrections humaines.

Le fichier reprend exactement les20 commentaires de la proposition conversationnelle :
L003, L002, L015, L033, L042, L065, L068, L090, L059, L005,
L027, L069, L063, L070, L074, L077, L045, L037, L029 et L013.
Un repère Lnnn désigne ordre_lot=nnn du lot500, pas le repère Cnnn du pilote initial.
Les20 commentaires donnent29 lignes : les positions envers plusieurs cibles et
les positions contextuelles sont conservées séparément, sans devenir automatiquement
une position « mitigée ». Toutes les annotations sont des propositions à valider.

## Onglets

- **Vérification** : lecture côte à côte, avis et correction libre.
- **Annotations détaillées** : cible, proposition, position, code/intitulé,
  argument précis, preuves de position et d'argument, statut, ambiguïtés,
  exploitation possible et colonnes structurées de correction vides.
- **Lecture sans masquage** : chaque texte et parent en petits blocs verticaux,
  pour contourner la hauteur maximale d'Excel. Les cellules des autres onglets
  conservent aussi les textes complets.
- **Dictionnaire provisoire** : définitions A01–A12, M01, critères et exemples.
  ARG_ABSENT, ARG_AUTRE et ARG_AMBIGU sont des diagnostics réservés.
- **Guide** : consignes de lecture et limites de la proposition.

La preuve argumentative est distincte de la preuve de position. Un résumé vide
pour un argument absent ou ambigu est intentionnel : il évite d'inventer une
raison. Une position favorable à une action ne signifie pas soutien global à
un acteur. La pertinence thématique ne garantit pas l'exploitation statistique.
Les accusations restent celles des auteurs, sans vérification factuelle.

Le JSON joint conserve les propositions, le dictionnaire et l'empreinte des textes
sources. Le script `preparer_excel.py` exporte les décisions rédigées dans la
conversation; il ne classifie pas les textes et n'appelle aucune API. Il ne doit
pas être lancé sur une copie du classeur où une humaine a déjà saisi des corrections,
car il régénère le fichier. Conserver la relecture humaine sous un autre nom.

Aucun changement n'est apporté aux annotations historiques, au dashboard ni aux
fichiers de relecture existants. Seul ce nouveau dossier est ajouté.

# Méthodologie et suivi

Commencer par **[SUIVI_DU_PROJET.md](SUIVI_DU_PROJET.md)** : historique, passes1/2,
choix de périmètre, limites et étapes restant à définir.

## Dossier piloteV1

Un protocole pilote version1 est une première version écrite des règles à essayer.
Ce n'est pas un modèle entraîné ni une validation définitive de la méthode.

1. [Protocole](pilote_v1/PROTOCOLE_V1.md) : périmètre, unités, parent, positions,
   arguments, incertitude et exploitation.
2. [Dictionnaire versionné](pilote_v1/dictionnaire_v1.json) : A01–A12/M01 et
   diagnostics, plus candidats non actifs; pas un nouveau dictionnaire concurrent.
3. [Décisions et exemples](pilote_v1/decisions_et_exemples.md) : retours des passes
   précédentes et contre-exemples.
4. [Schéma JSON strict](pilote_v1/schema_annotation_v1.json) : futur contrat LLM,
   pas preuve qu'un appel Structured Outputs a eu lieu.
5. [Bilan de l'essai50](pilote_v1/BILAN_ET_DECISIONS.md) : résultats provisoires,
   difficultés et décisions restantes.
6. [Excel de consultation50](pilote_v1/ESSAI_50_PROPOSITIONS_PROTOCOLE_V1.xlsx) :
   textes/parents/positions côte à côte. Aucun nouveau devoir d'annotation exhaustive.
7. [Annotations proposées](pilote_v1/annotations_50_proposees.json) et
   [provenance](pilote_v1/execution_conversationnelle.json).

## Code exécuté et reproductibilité

`preparer_lot50.py` sélectionne des textes existants et joint les données; il ne
classifie pas. `valider_annotations.py` contrôle le contrat et les citations;
il ne valide pas la justesse sémantique. `exporter_essai.py` construit l'Excel et
les effectifs à partir des propositions enregistrées.

Les interprétations ont été faites directement par l'assistant dans la conversation,
sans API payante, modèle/version figés ni nouvel entraînement. Les fichiers
permettent de rejouer sélection/contrôles/export, pas de reproduire automatiquement
la génération des interprétations. Le pipeline API historique reste au contrat0.2
et n'a pas été connecté automatiquement au dashboard ou à ce nouveau schéma.

```bash
.venv/bin/python methodologie/pilote_v1/valider_annotations.py
.venv/bin/python -m unittest test_protocole_v1 -v
```

Pour régénérer uniquement sélection et export (sans classifier) :

```bash
.venv/bin/python methodologie/pilote_v1/preparer_lot50.py
.venv/bin/python methodologie/pilote_v1/exporter_essai.py
```

Les nouveaux fichiers sont séparés; les annotations historiques, les relectures
humaines et le dashboard ne sont pas modifiés par cette étape. Les cas hors
périmètre restent dans le lot pour ne pas masquer les erreurs de présélection.

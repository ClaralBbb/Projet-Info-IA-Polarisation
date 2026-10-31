# Tableau de bord — premier lot classifié

**60 commentaires traités, 82 positions proposées; 440 commentaires à traiter.**
Ce sont des annotations conversationnelles provisoires, non validées par une
humaine. Aucun appel API LLM, aucune dépense API, aucun modèle API figé.

## Ouvrir l'interface

Télécharger `tableau_de_bord.html`, puis l'ouvrir dans un navigateur moderne.
Le fichier contient toutes les ressources et fonctionne sans serveur ni clé.
Il charge les 500 commentaires mais attribue des annotations uniquement aux 60
réellement traités. Les 440 autres restent explicitement « À traiter ».

L'interface permet :

- de suivre l'avancement réel;
- de consulter des distributions descriptives sur le seul lot traité;
- de filtrer par position, thème, chaîne, incertitude ou mots;
- de lire ensemble commentaire, parent et positions avec citations;
- de noter accord, désaccord et corrections;
- d'exporter/importer une sauvegarde JSON, ou d'exporter la relecture en CSV.

Les corrections restent dans le navigateur si son stockage le permet; elles ne
sont pas automatiquement envoyées au dépôt ni au corpus validé. Exporter une
sauvegarde et transmettre le fichier pour une intégration ultérieure. Une
sauvegarde est liée aux empreintes exactes des données ET des annotations pour
éviter d'appliquer les corrections aux mauvaises positions après une mise à jour.

## Fichiers traçables

- `annotations_60.json` : positions proposées pour les 60 premières lignes du
  lot mélangé. Champs de grille 0.2, citations exactes et incertitudes.
- `protocole.json` : provenance, mode conversationnel et empreinte des données.
- `positions_60.csv` : export des 82 lignes de positions.
- `bilan.json` : effectifs et statut réel du traitement.
- `template.html` : code de l'interface, sans les données embarquées.
- `../build_platform.py` : assemblage des données et du tableau de bord.
- `../docs/index.html` : même interface, prête pour un hébergement statique.

Les décisions ont été proposées directement dans la conversation après lecture
des textes complets et des parents. Le script de construction ne classe rien :
il affiche les décisions enregistrées. Le pipeline API `classify_opinions.py`
n'a pas été utilisé pour ces annotations. Leur structure a été vérifiée avec
son validateur local, et chaque citation a été contrôlée dans le texte source.
Ce contrôle ne prouve pas la justesse sémantique des annotations.

## Bilan actuel

- 24 commentaires : intervention policière.
- 24 : violences au sens large.
- 6 : pertinence partielle.
- 6 : hors sujet du périmètre étudié.

Ces catégories concernent les commentaires, pas les positions. Des positions
secondaires hors périmètre peuvent être conservées sans être comptées comme
opinions sur la police. Les tableaux de positions comptent une fois chaque
commentaire par catégorie de position, avec auteur et périmètre explicités.
Un commentaire peut apparaître dans plusieurs catégories. Aucune extrapolation
aux 500 ou au corpus complet; aucune mesure validée de polarisation.

## Vérifications et reconstruction

```bash
.venv/bin/python build_platform.py
.venv/bin/python -m unittest -v
```

La vérification navigateur utilise Playwright et Chromium disponibles dans cet
environnement. Depuis la racine, servir uniquement `docs`, puis dans un second
terminal lancer le contrôle :

```bash
python3 -m http.server 8765 --bind 127.0.0.1 --directory docs
node scripts/test_platform.cjs
```

Le navigateur de l'environnement bloque les fichiers `file://`; le test a donc
utilisé ce serveur HTTP local. Les ressources externes sont bloquées dans le
test. Filtres, lecture, stockage local, export/import JSON et recherche ont été
exercés dans Chromium, avec vérification d'absence d'erreurs JavaScript.

## Adresse publique : pas encore activée

Le dépôt contient le site prêt à servir dans `docs`. Aucun hébergement public
n'a été activé ni vérifié. Si GitHub Pages est disponible pour le dépôt, choisir
**Settings → Pages → Deploy from a branch → main → /docs**. Vérifier les règles
et la visibilité du dépôt avant activation : ne pas publier de données privées
par inadvertance. Le fichier HTML téléchargé reste utilisable sans cette étape.

La validation des vidéos pour l'événement, la couverture médiatique et la qualité
des classifications restent à vérifier avant toute conclusion générale. Des
textes peuvent contenir insultes, propos discriminatoires, données personnelles
et accusations non vérifiées; l'étude les décrit sans les endosser.

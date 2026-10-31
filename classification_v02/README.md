# Extension à 500 commentaires — grille 0.2

**État : lot sélectionné, pas encore classifié par un modèle.** Aucun appel API
n'a été effectué. Le pipeline a été testé en simulation et avec des réponses
simulées. Sa compatibilité réelle avec un modèle et l'API reste à vérifier.

## Données et protocole

- `lot_police_violences_500.xlsx` : 500 commentaires complets avec parents et
  colonnes humaines vides. 50 lignes de contrôle sont proposées, sans obligation
  d'annoter les 500.
- `commentaires_500.jsonl` : entrées du futur classificateur.
- `selection.json` : graines, lexique, provenance et exclusions.
- `grille_et_prompt_v02.md` : consignes et exemples few-shot proposés.
- `schema.json` : schéma strict prévu pour Structured Outputs.
- `retours_humains_pilote.json` : relecture humaine reçue, distincte des décisions IA.

250 principaux, 250 réponses, au plus deux par vidéo; 401 vidéos distinctes.
Aucun commentaire ni vidéo des lots précédents (20 démonstrations et 100
réservés à l'évaluation) n'est inclus. Tous les parents référencés des réponses
sont disponibles. Aucun lien factuel avec Paris le 17 octobre n'est garanti.
La présélection lexicale peut manquer des commentaires sans mots-clés et les
quotas modifient les proportions : pas d'estimation représentative de l'opinion.

Les retours du pilote ont conduit à préciser l'acteur nommé, l'objet, la causalité
sans approbation, les citations de tiers et les relations partielles au parent.
Le désaccord sur C002 reste ouvert : humour du parent et pertinence de la réponse
ne doivent pas être confondus. Les cellules humaines vides restent non relues.

## Simulation — sans connexion et sans coût API

Depuis la racine du dépôt :

```bash
.venv/bin/python prepare_large_sample.py
.venv/bin/python classify_opinions.py --limit 500
.venv/bin/python -m unittest -v
```

`classify_opinions.py` ne fait aucun appel sans `--execute`. La simulation
contrôle le chargement et affiche l'empreinte du protocole, sans inventer de
résultats ni de coût estimé. Les retours humains ne sont pas régénérés par le
script de sélection : ils sont conservés tels que reçus.

## Exécution ultérieure — payante, non lancée

Choisir un identifiant de modèle compatible avec Responses et Structured Outputs,
vérifier sa disponibilité et sa tarification, estimer un budget, obtenir l'accord
de l'utilisatrice et configurer `CLASSIFICATION_API_KEY` de façon sécurisée.
ChatGPT Plus ne finance pas ces appels. Ne pas saisir la clé dans Git ou le chat.
Le nom de modèle doit être fixé; une option `--reasoning-effort` existe pour les
modèles qui l'acceptent. Aucun o1/o3 n'a été sélectionné ni testé ici.

Exemple de commande à adapter **uniquement après accord de dépense** :

```text
.venv/bin/python classify_opinions.py --execute --model IDENTIFIANT_VERIFIE --limit 10
```

Commencer par 10 pour vérifier la compatibilité, les résultats, les tokens et le
coût réel avant un passage à 500. La limite porte sur les premières entrées du
fichier; une relance saute les identifiants déjà validés avec le même protocole.
Un changement de modèle, prompt, schéma ou fichier d'entrée exige un autre dossier
de sortie. Les réponses brutes et usages retournés sont conservés localement.
Après interruption réseau, vérifier si une requête a été facturée avant de
relancer; aucune nouvelle tentative automatique n'est effectuée.

Le JSON est contrôlé localement (types, catégories, champs exacts, citations et
parents). Cela ne garantit pas la justesse sémantique. Les réponses incomplètes,
refus et citations non retrouvées arrêtent le traitement plutôt que d'être
comptés comme des annotations valides. Le validateur local couvre les contraintes
du schéma actuel; il ne prétend pas implémenter tout JSON Schema.

## Après la classification

1. Vérifier un sous-échantillon humain indépendant, les cas ambigus et les
   positions oubliées. Examiner les erreurs par catégorie. Ne pas traiter les
   corrections du pilote comme une mesure indépendante de performance.
2. Valider les vidéos et identifier les chaînes; éviter de présenter le corpus
   comme une couverture vérifiée de l'événement ou des médias.
3. Compter les commentaires portant une position, et non seulement les lignes
   de positions. Séparer auteur/citation, principaux/réponses et objets discutés.
4. Comparer les positions et arguments sur le même objet. Une cooccurrence de
   thèmes n'est pas une relation causale ou une opposition argumentative.
5. Produire un rapport HTML avec distributions, incertitudes, exemples et
   divergences/convergences, puis étudier la sensibilité aux vidéos dominantes.
6. Étendre les thèmes et le corpus après validation. Ne pas convertir la simple
   négativité en score de polarisation ni attribuer des profils aux personnes.

Les données publiées peuvent contenir des informations personnelles dans les
textes; limiter leur réutilisation au projet et ne pas ajouter les noms d'auteurs.

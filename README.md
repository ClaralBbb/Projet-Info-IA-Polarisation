# Dataset YouTube — manifestations à Paris, 17 octobre 2026

**Collecte via YouTube Data API v3.** Le classeur
`data/paris_2026-10-17.xlsx` contient les vidéos candidates et leurs commentaires
publics accessibles. Consulter Métadonnées et Erreurs pour connaître les limites
de la collecte. La pertinence des vidéos reste à vérifier : ce corpus de recherche
ne garantit pas que chaque vidéo concerne la manifestation parisienne ciblée.

## Installation et collecte

Python 3.12 recommandé. Depuis ce dépôt :

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m unittest -v
# Configurer YOUTUBE_API_KEY dans les paramètres sécurisés de l'environnement.
.venv/bin/python collect.py
```

Créer une clé pour YouTube Data API v3 dans Google Cloud et activer cette API.
Ne jamais transmettre la clé dans le chat ni l'ajouter à Git. Le réseau doit
permettre `www.googleapis.com`. Aucune autre authentification n'est nécessaire
pour les données publiques. Les quotas peuvent interrompre la collecte.

## Contenu et limites

Le collecteur recherche quatre expressions françaises/anglaises et parcourt les
pages que l'API expose. La publication est filtrée depuis le début du 17 octobre
2026 à Paris (16 octobre à 22 h UTC), sans date de fin pour inclure les mises en
ligne tardives. Ce filtre peut écarter des directs annoncés avant l'événement.
Il ne prouve ni l'existence d'une manifestation particulière ni la pertinence des
résultats : vérifier manuellement la colonne `relevance` avant analyse.

L'Excel contient Métadonnées, Vidéos, Commentaires, Erreurs. Les réponses sont
reliées au commentaire parent. Les vidéos sont des liens, pas des téléchargements.
Les noms des auteurs de commentaires sont omis; le texte peut contenir des données
personnelles et doit être examiné avant publication publique.

YouTube ne garantit pas tous les résultats de recherche. Seuls les commentaires
publics accessibles sont collectés : les commentaires supprimés, privés, modérés
ou désactivés ne peuvent pas être obtenus. Un onglet Erreurs et un code de sortie
non nul signalent les interruptions. Un JSON adjacent conserve les données avant
export Excel. Le collecteur utilise huit requêtes simultanées et un cache local ignoré par Git
(`.youtube-cache/`). Une relance réutilise les réponses déjà reçues pour reprendre
la collecte sans refaire ces requêtes. Pour un nouvel instantané, déplacer le cache
et les anciennes sorties avant de relancer. Les réponses en cache peuvent être
anciennes : une reprise ne constitue pas une actualisation de tous les commentaires.
Le JSON et le cache restent locaux; le classeur Excel est le dataset destiné à Git.

## Vérification locale

Les tests utilisent une API simulée et vérifient pagination, dédoublonnage,
réponses, erreurs et export Excel sans interprétation des textes comme formules.
Ils ne valident pas l'accès réel à YouTube. `--template` régénère le modèle vide.

Les erreurs ne sont pas masquées : des commentaires désactivés ou des échecs API
peuvent rendre le corpus partiel. Aucun fichier vidéo n’est téléchargé. Les textes
des commentaires peuvent contenir des informations personnelles : limiter leur
réutilisation au cadre du projet et respecter les conditions de YouTube.

## Première exploration des commentaires

Un [rapport HTML interactif](reports/rapport.html) et ses
[fichiers d'analyse](reports/README.md) sont disponibles. Télécharger le HTML et
l'ouvrir dans un navigateur pour consulter les comparaisons de fréquences et
les extraits filtrables. Aucun serveur ni appel à l'API n'est nécessaire.

Pour régénérer : `.venv/bin/python analyze.py` (JSON local ou Excel du dépôt).
Cette exploration lexicale prépare l'étude de polarisation; elle ne mesure
pas les opinions individuelles ni la polarisation à ce stade.

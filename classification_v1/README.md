# Classifier les opinions avec la grille V1

**État : préparation technique testée hors API. Aucun appel LLM payant exécuté, aucun nouveau résultat d’opinion, aucune mise à jour du dashboard.** Les anciennes annotations restent conversationnelles.

## Les fichiers à lire

1. [Règles de périmètre](REGLES_PERIMETRE_V1.md) : France entière, candidats, suites, comparaisons, incertains et informations contestées.
2. [Consigne du modèle](prompt_v1.md) : cible + proposition + position + arguments, contexte et prudence.
3. [Schéma JSON V1](../methodologie/pilote_v1/schema_annotation_v1.json), [dictionnaire](../methodologie/pilote_v1/dictionnaire_v1.json), [protocole](../methodologie/pilote_v1/PROTOCOLE_V1.md) et [exemples](../methodologie/pilote_v1/decisions_et_exemples.md). Ces documents sont assemblés dans les instructions ; les annotations proposées sur les 50 ne sont pas envoyées au modèle.
4. [Exécuteur](../classify_opinions.py) : point d’entrée et construction de la requête Structured Outputs. [pipeline.py](pipeline.py) : préparation, jointure du tri, contrôles, journaux et reprise.
5. [Tests](../test_classification_v1.py) : réponses factices, jamais un modèle appelé sur le réseau.

## Essayer sans payer

Depuis la racine du dépôt :

```sh
.venv/bin/python classify_opinions.py --limit 10 --output /tmp/essai_v1_sans_api
```

La simulation ne lit pas la clé API et n’utilise pas le réseau. Elle écrit :

- `protocole.json` : modèle éventuel, instructions, schéma, paramètres et empreintes ;
- `requetes_pretes.jsonl` : les requêtes qui seraient envoyées, une par commentaire ;
- `bilan.json` : nombre de requêtes, zéro appel et zéro annotation produite.

Dans chaque requête, `instructions` contient les consignes complètes, et `input[0].content` contient un JSON avec deux blocs : `commentaire` (texte complet, parent, titre, chaîne) et `contexte_documentaire` (tri séparé, motifs, signalements). Les données source sont traitées comme des données, jamais comme des instructions. Aucun texte n’est volontairement tronqué. Le modèle reste à choisir : `MODELE_A_CHOISIR` est un repère de simulation, pas un modèle réel.

Une simulation de 10 requêtes est disponible dans [preparation_10_sans_api](preparation_10_sans_api/). Elle sert à examiner les entrées, pas les performances. Aucun score de qualité ni coût réel d’un modèle n’en est déduit.

## Autres commentaires

```sh
.venv/bin/python classify_opinions.py --input /chemin/nouveaux.jsonl --output /tmp/nouveau_test_v1
```

Chaque ligne doit contenir `comment_id`, `video_id`, `texte`, `parent_id`, `texte_parent` ; titre, chaîne et statut du parent sont recommandés. `parent_id` et `texte_parent` peuvent être null. Un texte parent indisponible ne doit pas être remplacé par une invention.

Le tri archivé du pilote n’est joint automatiquement qu’à son fichier source exact par défaut. Pour un autre corpus, on peut fournir `--tri /chemin/tri.json` au format de `tri_50.json` (objet avec tableau `commentaires`, mêmes identifiants et statuts documentaires). Sans tri, le rattachement reste non vérifié et aucune position n’est candidate aux statistiques principales. Une vidéo incohérente à la jointure ou des identifiants dupliqués provoquent un arrêt.

## Exécution réelle : étape ultérieure

Un modèle compatible avec les Structured Outputs doit être choisi, sa tarification vérifiée et le budget convenu avant toute exécution. Le code exige `--execute`, `--model IDENTIFIANT_VERIFIE` et le secret `CLASSIFICATION_API_KEY` pour effectuer des appels facturables. L’option `--reasoning-effort` n’est à utiliser que si le modèle la prend en charge. Aucun modèle précis n’est annoncé comme validé pour cette grille. ChatGPT Plus ne finance pas ces appels API.

Le résultat conserve les identifiants, le modèle retourné, l’usage API, les versions, l’annotation et le tri séparé. Les citations du commentaire et du parent sont vérifiées à leur emplacement. Le JSON conserve `lien_evenement.statut = non_verifie` : l’interprétation d’une opinion ne certifie pas les scènes. Un marqueur technique identifie les positions candidates aux statistiques, avec `validation_humaine_independante = false`. Il ne vaut pas validation de qualité.

Avant l’envoi, une tentative est inscrite et synchronisée sur disque. La réponse brute est enregistrée avant validation. Refus, sortie incomplète, erreur réseau ou JSON invalide arrêtent le traitement sans répétition automatique. Une tentative sans résultat validé bloque la reprise : examiner les journaux et résoudre le cas avant tout nouvel envoi. Les résultats déjà validés sont sautés. Ne pas supprimer les journaux pour forcer une reprise aveugle.

Le même dossier ne peut pas recevoir un modèle, des données, des consignes, une sélection ou un mode différents. Changer de configuration exige un autre dossier. Les journaux réels restent ignorés par Git ; les simulations contiennent des textes publics et restent à manipuler comme les données du corpus.

## Validation avant extension

Les contrôles techniques ne prouvent pas une interprétation correcte. Le prochain essai réel doit vérifier les erreurs de cible, de position, les arguments inventés ou manqués et les effets du parent. Les exemples des passes précédentes ont développé la grille ; un contrôle humain indépendant reste nécessaire avant les statistiques ou le passage à des milliers de commentaires.

## Mise à jour : contrôle documentaire par vidéo

Voir [la méthode de vérification](../verification_evenement/README.md). Le script accepte maintenant `--verification REGISTRE.json`. Le précontrôle des 50 vidéos est chargé pour le pilote ; pour une autre source sans registre, le contrôle reste à faire. Un rattachement vidéo documenté et étayé est désormais requis pour marquer des positions candidates aux statistiques principales. Les simulations archivées dans ce dossier précèdent cette évolution : relancer dans un nouveau dossier pour intégrer le contrôle. Aucun rattachement n’a été confirmé automatiquement.

# Vérifier le rattachement des vidéos — méthode simple

**Objectif : déterminer si une vidéo traite de la mobilisation du 17 octobre 2026 en France. Cela n’authentifie pas chaque scène et ne confirme pas les accusations des commentaires.**

## Ce qui a réellement été fait

1. Le précédent tri a été effectué par lecture des titres, descriptions, commentaires et parents par l’assistant. Ses décisions sont conservées dans [le bilan du tri](../methodologie/pilote_v1/tri_evenement_france/BILAN_TRI.md).
2. Le nouveau script [controle.py](controle.py), fonction `precontrole()`, a parcouru hors réseau les métadonnées YouTube archivées des 50 vidéos : repères de date, année et lieu, mentions de 1961, dates ultérieures, description absente et contradiction 7/17 octobre. Il conserve des extraits exacts et la publication à part.
3. Le résultat est dans [precontrole_50.json](precontrole_50.json), une entrée par vidéo. Tous les contrôles restent « à vérifier ». Les 17 commentaires au lien plausible précédemment repérés ne deviennent pas pour autant des faits vérifiés.

Aucune transcription, aucun visionnage et aucun recoupement indépendant n’ont été effectués dans cette étape. Le précontrôle est un repérage de mots, non un détecteur fiable de pertinence : il peut manquer des formulations ou relever une autre date seulement citée en contexte. Il ne déduit pas le pays du nom de chaîne. Les indices de lieu sont une liste indicative, pas un inventaire de toutes les villes françaises. La nationalité et la langue de l’éditeur ne décident pas du pays des scènes.

## Ce qui doit suivre pour étayer le rattachement

Examiner le reportage, une transcription disponible ou une source concordante, puis enregistrer :

- `statut` : `rattachement_etaye`, `lien_plausible`, `autre_evenement`, `suites` ou `a_verifier` ;
- `motif`, `responsable_controle` et `date_controle` au format ISO ;
- `preuves_examinees` : pour chaque preuve, `type` (`reportage_examine`, `transcription_examinee` ou `source_concordante`), `url`, `passage` exact ou description d’observation clairement identifiée, `etaye_date_evenement` et `etaye_lieu_france` (booléens).

Pour `rattachement_etaye`, au moins une preuve examinée doit étayer la date de l’événement et le lieu français, au-delà du seul titre. La recherche, la lecture et le jugement restent une étape humaine ou documentaire ; le programme ne sait pas garantir la sincérité d’une déclaration enregistrée. Les sources concordantes doivent réellement être examinées, et leur indépendance appréciée, pas présumée parce que deux sites reprennent la même information. Conserver les cas incertains. Ne pas déclarer toutes les images authentiques : `images_authentifiees` reste faux dans ce registre.

## Intégration au code de classification

[pipeline.py](../classification_v1/pipeline.py) lit le registre avec `--verification` et joint le contrôle par identifiant de vidéo. Le pilote utilise son précontrôle par défaut. Pour de nouvelles données sans registre, le contrôle reste manquant.

`attach()` et `validate_review()` contrôlent les preuves déclarées et les champs. Le rattachement vidéo étayé est désormais nécessaire, en plus du tri du commentaire et de sa position exploitable, pour marquer une position candidate aux statistiques principales. Ce marqueur technique ne vaut toujours pas validation scientifique. Il reste possible de préparer ou classifier les textes à titre exploratoire avec des vidéos encore incertaines.

Le JSON d’opinion continue à dire « non vérifié » au niveau des faits : le contrôle documentaire externe ne devient pas une certitude fabriquée par le LLM. Les versions et empreintes du registre sont archivées avec chaque préparation. Les anciennes simulations restent des archives de l’étape précédente.

```sh
# Nouveau précontrôle sans réseau, sans écraser les décisions existantes
.venv/bin/python verification_evenement/controle.py --output /tmp/nouveau_precontrole.json
# Préparer les requêtes avec le contrôle, sans appel payant
.venv/bin/python classify_opinions.py --limit 10 --output /tmp/simulation_avec_controle
```

## Pour avancer

Commencer par les contradictions et références à d’autres dates, puis vérifier quelques vidéos candidates et documenter les décisions. L’utilisatrice peut consulter ou visionner les vidéos signalées et partager un lien ou un passage utile ; aucune nouvelle passe complète de commentaires n’est demandée. Ensuite : choisir un modèle, chiffrer un petit essai réel, comparer les annotations à un contrôle humain indépendant et élargir seulement après examen des erreurs. Aucun appel LLM payant n’a été effectué ici.

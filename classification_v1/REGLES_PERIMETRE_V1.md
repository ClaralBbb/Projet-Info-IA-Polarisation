# Règles provisoires de périmètre — France entière, version 1

Question : positions et arguments sur les violences et dégâts autour de la mobilisation recherchée du 17 octobre 2026. La police n’est pas la seule cible. La recherche initiale centrée sur Paris ne rend pas le corpus national exhaustif.

| Cas documentaire | Traitement |
| --- | --- |
| Lien plausible, non confirmé | Candidat à l’analyse principale ; statut non vérifié conservé. |
| Rattachement incertain ou date contradictoire | À vérifier ; hors statistiques principales. |
| Nouveau rassemblement des 18, 22 ou 24 | Suites, séparées du 17. |
| Autre événement, comparaison étrangère ou historique | Hors corpus principal ; conserver pour analyser les comparaisons. |
| Opinion générale ou contexte | Contexte séparé ; ne pas transformer en jugement sur un acte précis. |
| Information contestée ou allégation non corroborée signalée | Candidat avec signalement ; à revoir, hors statistiques principales provisoires. Cela ne signifie pas que l’opinion est sans intérêt. |
| Métadonnées ou tri absents | Rattachement non vérifié ; hors statistiques principales. |

La vidéo et le commentaire ont des statuts séparés. La date de publication n’établit pas celle des images. Un titre, une description ou un nom de chaîne ne confirme pas les faits. Le parent éclaire le texte sans lui transférer son opinion.

## Application dans le programme

Le tri documentaire est joint séparément aux données envoyées au modèle. Le modèle interprète la pertinence thématique et les opinions, mais ne peut pas certifier les faits : le JSON V1 conserve `lien_evenement.statut = non_verifie`. La décision de périmètre reste enregistrée à côté de sa sortie.

L’admissibilité documentaire est calculée par Python : candidat seulement si vidéo et commentaire ont un lien plausible, sans signalement. Une position n’est qu’une **candidate aux statistiques** si, en plus, elle est thématiquement directe, favorable/critique/mitigée, avec exploitabilité « exploitable » et sans forte incertitude de cible ou de position. Ce marqueur ne remplace pas la validation de qualité du modèle. Aucune statistique publique ni mise à jour du dashboard n’est produite ici.

Ces règles sont provisoires et versionnées. Les modifier nécessite un nouveau dossier d’exécution et une réévaluation des comparaisons. Les annotations historiques restent intactes.

## Contrôle vidéo ajouté le 22 novembre 2026

Le précontrôle et les preuves examinées sont désormais joints par vidéo via le registre de `verification_evenement/controle.py`. Pour marquer une position candidate aux statistiques principales, le rattachement de la vidéo doit être `rattachement_etaye`, en plus de toutes les conditions précédentes. Un lien seulement plausible reste utilisable pour l’exploration, pas pour ce marqueur statistique. Les métadonnées seules ne produisent jamais ce statut. Le registre des 50 est à vérifier : aucun visionnage ou recoupement indépendant n’a été effectué.

# Protocole pilote1.0 — version provisoire pour essai

## Question et périmètre

Décrire les positions et arguments exprimés sur les violences et dégâts autour de
la mobilisation recherchée du17octobre2026. Distinguer force policière, violences
attribuées aux participants et dégradations/pillages. Ne pas recentrer silencieusement
sur la seule police. Politique, revendications et médias sont conservés comme
sujets associés lorsqu'ils expliquent ou cadrent les violences. Les passages
purement politiques et autres événements restent séparés du noyau statistique.

La pertinence thématique et le lien factuel avec l'événement sont deux variables
différentes. Ni un titre, ni la date de publication ne prouvent la date et le lieu
des scènes. Les50 textes ne sont pas un corpus validé de Paris le17octobre.

## Unités et contexte

Une unité de contexte est un commentaire complet avec son parent référencé,
le titre et la chaîne déclarée. Un parent principal YouTube n'est pas nécessairement
le message exact visé. Lire le commentaire seul puis consulter le parent pour
résoudre les pronoms, la proposition contestée ou la fonction d'une réponse.
Distinguer sans_parent, non_necessaire, utile, indispensable et insuffisant.
Ne jamais transférer l'opinion du parent à la réponse. Une réponse autonome peut
être pertinente; une réponse à un parent pertinent peut être hors sujet.

Une unité d'annotation est une position envers une cible et une proposition
précises. Plusieurs positions dans un texte ne sont pas plusieurs commentaires.
La défense des manifestants, la critique d'un acte policier et celle des médias
peuvent coexister dans la même réponse. Conserver l'axe de réponse au parent
sans supprimer les positions secondaires effectivement présentes.

## Positions, arguments et incertitude

Positions : favorable, critique, mitigee, descriptive, indeterminable.
Favorable/critique concerne la proposition évaluée, pas un camp universel.
Mitigée suppose des réserves envers une même proposition; ne pas l'utiliser comme
raccourci pour deux cibles différentes. Décrire une cause de violence ne signifie
pas approuver cette violence. Une position citée ou hypothétique n'est pas
nécessairement celle de l'auteur; ne pas la compter comme adhésion personnelle.

Extraire la raison, pas seulement le thème. « Police incapable de prévenir les
dégâts » contient un raisonnement identifiable; ne pas le perdre dans le champ
responsabilité. À l'inverse, « je n'aime pas la police » ne contient pas forcément
un argument. Ne pas inventer un mécanisme économique pour Amazon/Zalando ni un
payeur précis dans un texte mal ponctué.

Argument explicite : lien formulé ou étayé par l'enchaînement du texte, pas
nécessairement par le mot parce que. Implicite étayé : reconstruction minimale,
avec preuve et limite explicitées. Ambigu : plusieurs raisonnements plausibles,
aucun sélectionné arbitrairement. Absent : raison non trouvée après lecture.
Non annoté et absent sont distincts. Argument identifiable hors dictionnaire :
ARG_AUTRE, avec résumé précis et preuve; ne pas forcer une famille.

Évaluer séparément l'incertitude sur cible, position et argument. L'ironie peut
être interprétable ou non : pas de règle universelle « ironie=indéterminable ».
Toutes les accusations restent attribuées aux internautes, sans validation
factuelle, juridique ou diagnostic sur les personnes.

## Dictionnaire et exemples

Réutiliser le dictionnaire A01–A12/M01 version arguments-provisoire-0.1.
Ne pas activer de nouvelle famille lors de cet essai. Les motivations opportunistes
et l'utilité préventive de l'intervention restent des candidats à discuter.
Pour L063, garder le résumé et suspendre A07 si aucune revendication précise
n'est confrontée aux actes. Pour L005, le non-travail allégué ne suffit pas à
imposer un coût aux classes moyennes. Voir decisions_et_exemples.md.

Une position peut contenir plusieurs arguments. ARG_ABSENT/ARG_AMBIGU sont des
diagnostics, pas des arguments à compter. La présence de l'argument et son code
ne garantissent pas que la position est exploitable. Un argument causal peut
être analysé même si la position sur la légitimité de la violence reste descriptive.

## Sortie et contrôles

Schéma : schema_annotation_v1.json. Tous les objets interdisent les champs
supplémentaires et tous les champs sont requis; null explicite où prévu.
Les positions et arguments peuvent être des tableaux vides selon le diagnostic.
Valider types/catégories et retrouver chaque citation dans le commentaire.
Les citations du parent sont stockées séparément et vérifiées dans le parent.
Une position indéterminable ne peut être exploitable comme position signée.
Une argumentation absente ou ambiguë ne reçoit pas de résumé affirmatif inventé.

Ce schéma est conçu pour une future requête Structured Outputs, mais le pilote
conversationnel n'est pas une exécution API. Aucun modèle/API/version n'est figé
pour l'instant. Les identifiants de modèle, paramètres, prompts et usages devront
être enregistrés avant une exécution reproductible. Ne pas annoncer une fiabilité
à partir de contrôles de format ou de citations seulement.

## Exploitation et évolution

Les commentaires ayant servi à construire la grille ne mesurent pas sa qualité
indépendante. Le lot50 est un essai exploratoire de protocole sur des vidéos
distinctes, pas une évaluation humaine aveugle ni un entraînement de modèle.
Conserver non_exploitable/a_revoir au lieu de remplir une catégorie forcée.
Pas de score de clivage1–10 ni d'indice de polarisation avant définition du construit,
contrôle du corpus et validation de la classification sur un lot indépendant.

Une famille candidate doit avoir définition, critères, exemples et contre-exemples.
La rareté seule ne l'invalide pas, mais ne pas créer une famille par commentaire.
Geler la version par lot; après changement, journaliser et reprendre les anciens
rattachements avant de comparer les fréquences entre versions.

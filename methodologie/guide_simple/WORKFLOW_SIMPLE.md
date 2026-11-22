# Mon projet, étape par étape

Guide simple et modifiable • État au 22 novembre 2026 • Version de travail à relire ensemble

Objectif : comprendre les opinions et les arguments sur les violences et dégâts autour de la mobilisation recherchée du 17 octobre 2026, en France entière. La police est une cible parmi d’autres : manifestants, casseurs et autorités peuvent aussi être évalués.

Le parcours : collecter → explorer → sélectionner → proposer des annotations → corriger la grille → tester sur 50 textes → vérifier leur rattachement → automatiser et évaluer → étudier les convergences et divergences.

## 1. Récupérer les vidéos et commentaires — FAIT

Le script interroge YouTube Data API v3 avec quatre recherches : « manifestation Paris 17 octobre 2026 », « manifestations Paris 17/10/2026 », « Paris protest October 17 2026 » et « rassemblement Paris 17 octobre 2026 ». Il cherche les publications après le début du 17 octobre, heure de Paris, sans date de fin fixée dans le code. Il n’utilise pas de liste de médias imposée : médias connus, petites chaînes et contenus étrangers peuvent apparaître.

La fonction collect() parcourt les pages de résultats, retire les doublons de vidéos par identifiant, puis récupère les commentaires publics et les réponses. API.pages() parcourt les pages suivantes. Les réponses manquantes dans le premier résultat sont recherchées séparément. Les commentaires sont dédoublonnés par identifiant. Les indisponibilités sont enregistrées.

Résultat archivé : 1 222 vidéos candidates et 234 328 commentaires, dont 86 824 réponses ; 22 vidéos avaient les commentaires désactivés. Le fichier contient des liens vers les vidéos, pas les fichiers vidéo. Cela ne garantit ni tous les résultats YouTube ni que chaque vidéo montre bien cet événement.

À consulter : [Collecte : collect.py — QUERIES, API.pages(), collect(), export()](https://github.com/ClaralBbb/Projet-Info-IA-Polarisation/blob/main/collect.py)

À consulter : [Bilan et accès au jeu de données](https://github.com/ClaralBbb/Projet-Info-IA-Polarisation/blob/main/data/README.md)

## 2. Regarder ce qui revient souvent — FAIT

analyze.py normalise le texte pour les comptages : minuscules, accents et mots très courants. Il compte les mots et expressions et repère des thèmes avec des listes de mots. Les textes originaux restent conservés. Cette exploration ne comprend pas à elle seule les positions : « police » peut apparaître dans une critique comme dans un soutien.

À consulter : [Exploration : normalize(), tokens(), analyze()](https://github.com/ClaralBbb/Projet-Info-IA-Polarisation/blob/main/analyze.py)


---

## 3. Choisir des commentaires à lire — FAIT

prepare_annotation.py utilise select() pour présélectionner des textes contenant des mots liés à la police, la répression, la violence ou les dégâts. Il écarte les doublons de texte selon une clé normalisée, mélange les candidats avec une graine fixe et limite le nombre par vidéo. Les mots-clés servent à trouver des candidats, pas à décider leur opinion.

Le lot de 500 comprend 250 commentaires principaux et 250 réponses, avec au maximum deux commentaires par vidéo. prepare_large_sample.py exclut les identifiants et vidéos des pilotes précédents et joint le titre, la chaîne et le parent disponible. Ce choix diversifie les exemples ; il ne représente pas les proportions réelles des opinions et peut manquer des textes pertinents sans mots-clés.

À consulter : [Règles de sélection : LEXICON et select()](https://github.com/ClaralBbb/Projet-Info-IA-Polarisation/blob/main/prepare_annotation.py)

À consulter : [Préparation du lot de 500 et association du parent](https://github.com/ClaralBbb/Projet-Info-IA-Polarisation/blob/main/prepare_large_sample.py)

## 4. Proposer les premières annotations — FAIT, dans la conversation

J’ai interprété les commentaires pendant nos échanges, puis enregistré mes propositions en JSON. Aucun script n’a appelé o1, o3 ou un autre modèle via API pour produire ces annotations. Les exemples de consignes et de few-shot prompting préparés servent de démonstration ; ils ne prouvent pas une exécution automatique.

Passe 1 : 20 commentaires ont donné 22 positions proposées. Tu as relu le fichier ; 14 lignes comportaient un retour, 8 n’en avaient pas. Nous avons notamment revu les acteurs, les arguments de causalité et la façon de comprendre une réponse au parent. Une case vide n’a pas été considérée comme un accord.

À consulter : [Premières propositions enregistrées](https://github.com/ClaralBbb/Projet-Info-IA-Polarisation/blob/main/annotation/exemples_ia_20.json)

À consulter : [Révision après ta première relecture : main()](https://github.com/ClaralBbb/Projet-Info-IA-Polarisation/blob/main/revise_pilot.py)

Ensuite, 90 commentaires du lot de 500 ont été interprétés, donnant 118 positions. Ces 90 commentaires ne sont pas les mêmes que le premier pilote de 20. Plusieurs positions peuvent venir d’un seul texte : il faut donc distinguer le nombre de commentaires et le nombre de positions.

À consulter : [Propositions du lot de 60](https://github.com/ClaralBbb/Projet-Info-IA-Polarisation/blob/main/plateforme/annotations_60.json)

À consulter : [Propositions du second lot de 30](https://github.com/ClaralBbb/Projet-Info-IA-Polarisation/blob/main/plateforme/annotations_lot02.json)

## 5. Afficher les propositions dans le dashboard — FAIT, exploratoire

build_platform.py assemble les données et l’interface. actor_scope.py regroupe les positions connues par acteurs, actions et familles d’arguments au moyen de correspondances écrites manuellement. Ces règles ne savent pas classifier un nouveau commentaire. Le dashboard historique reflète ces anciennes propositions ; il n’intègre pas automatiquement toutes les révisions méthodologiques récentes.

À consulter : [Construction de l’interface : build()](https://github.com/ClaralBbb/Projet-Info-IA-Polarisation/blob/main/build_platform.py)

À consulter : [Regroupements manuels : project(), aggregate(), argument_families()](https://github.com/ClaralBbb/Projet-Info-IA-Polarisation/blob/main/actor_scope.py)


---

## 6. Améliorer la grille avec tes retours — PASSE 2 FAITE

Tu as signalé qu’un thème ou une action ne suffisait pas à comprendre le raisonnement. Nous avons remplacé le champ générique « action » dans la nouvelle méthode par un argument standardisé pour regrouper les idées et un argument précis qui résume fidèlement le texte. Exemple : reprocher à la police de ne pas empêcher les dégâts relève d’une défaillance supposée du maintien de l’ordre, même si le commentaire n’utilise pas « parce que ».

Nous avons aussi séparé : sujet pertinent, cible, proposition évaluée, position, argument et incertitude. Une ironie n’est pas automatiquement incompréhensible ; mais une position ou une cause incertaine ne doit pas être inventée. Pour « Amazon vous remercie », aucun mécanisme économique précis ne doit être affirmé sans preuve.

La passe 2 a porté sur 20 commentaires représentatifs des 90, soit 29 lignes de positions. Ton fichier retourné contenait 16 lignes avec retour et 13 sans verdict. La révision a conservé tes remarques et les décisions avant/après : certains codes d’argument ont été retirés, des allusions trop générales ont été sorties du noyau, et la fonction de réponse au parent a été mieux distinguée des positions secondaires.

À consulter : [Fichier des propositions et dictionnaire de la passe 2](https://github.com/ClaralBbb/Projet-Info-IA-Polarisation/blob/main/annotation/validation_arguments_20/propositions_et_dictionnaire.json)

À consulter : [Tes retours et les ajustements expliqués](https://github.com/ClaralBbb/Projet-Info-IA-Polarisation/blob/main/annotation/validation_arguments_20/revision_01/README.md)

À consulter : [Export des ajustements, sans classification API](https://github.com/ClaralBbb/Projet-Info-IA-Polarisation/blob/main/annotation/validation_arguments_20/revision_01/reviser_validation.py)

## Les décisions à retenir

• Sujet central : violences et dégâts, y compris violences policières, actes attribués aux manifestants et aux casseurs, dégradations et pillages. Les catégories ne prouvent pas l’identité réelle des personnes.
• Géographie : France entière, comme tu l’as confirmé. La recherche initiale était centrée sur Paris ; son extension à la France ne rend pas la collecte nationale exhaustive.
• Parent : le lire s’il aide à comprendre « ils », une contestation ou une ironie. Ne jamais attribuer automatiquement son opinion à la réponse. Le parent disponible est souvent le commentaire principal du fil, pas forcément le message exact visé.
• Une position = une cible + une proposition évaluée. Plusieurs cibles peuvent donner plusieurs lignes.
• Arguments : explicite, implicite étayé, ambigu ou absent. Un argument identifiable hors dictionnaire reçoit ARG_AUTRE, pas « absent ».

## Dictionnaire provisoire et JSON V1 — PRÉPARÉS

Les familles A01–A12 et M01 ont été proposées à partir de la lecture exploratoire ; elles n’ont pas été apprises automatiquement. Elles sont gelées provisoirement pour le test. Les nouvelles idées restent dans ARG_AUTRE avec résumé et citation, puis seront examinées avant de modifier la version du dictionnaire.

Le JSON V1 fixe la forme attendue : pertinence, positions, cibles, propositions, arguments, preuves et incertitudes. Les tableaux permettent plusieurs positions par commentaire. Les contrôles vérifient la structure et la présence des citations ; ils ne garantissent pas la justesse de l’interprétation.

À consulter : [Dictionnaire V1](https://github.com/ClaralBbb/Projet-Info-IA-Polarisation/blob/main/methodologie/pilote_v1/dictionnaire_v1.json)

À consulter : [Schéma JSON V1](https://github.com/ClaralBbb/Projet-Info-IA-Polarisation/blob/main/methodologie/pilote_v1/schema_annotation_v1.json)


---

## 7. Tester la nouvelle méthode sur 50 textes — FAIT, propositions

50 nouveaux commentaires ont été tirés parmi les textes non utilisés du lot de 500 : 25 principaux, 25 réponses, une vidéo différente par commentaire. Les identifiants et vidéos des 90 précédents ont été exclus. La graine 20261116 permet de refaire la sélection. Les textes difficiles n’ont pas été remplacés pour faciliter le résultat.

J’ai proposé les annotations de ces 50 textes dans la conversation selon la grille V1, puis les ai enregistrées séparément. Le script d’export ne réalise pas cette interprétation. Ce lot teste la méthode ; il n’a pas encore de validation humaine indépendante. Le dashboard n’a pas été remplacé.

À consulter : [Sélection des 50 : main()](https://github.com/ClaralBbb/Projet-Info-IA-Polarisation/blob/main/methodologie/pilote_v1/preparer_lot50.py)

À consulter : [Propositions enregistrées sur les 50 textes](https://github.com/ClaralBbb/Projet-Info-IA-Polarisation/blob/main/methodologie/pilote_v1/annotations_50_proposees.json)

À consulter : [Contrôles de structure et de citations](https://github.com/ClaralBbb/Projet-Info-IA-Polarisation/blob/main/methodologie/pilote_v1/valider_annotations.py)

À consulter : [Export Excel de l’essai](https://github.com/ClaralBbb/Projet-Info-IA-Polarisation/blob/main/methodologie/pilote_v1/exporter_essai.py)

## 8. Vérifier le lien avec la mobilisation — TRI DOCUMENTAIRE FAIT

Avec ton accord pour la France entière, les titres, dates de publication et descriptions des 50 vidéos ont été récupérés via YouTube. J’ai lu ces éléments avec les commentaires et parents et consigné des décisions séparées pour la vidéo et le commentaire. Aucun visionnage ni confirmation indépendante des faits n’a été effectué. Une date de publication ne date pas forcément les images.

Résultat pour les commentaires : 17 liens plausibles avec la mobilisation, 23 contextes généraux ou comparaisons, 4 références explicites à d’autres événements et 6 rattachements incertains. Les suites du 18, 22 ou 24 sont distinguées du 17. Une référence à 1961 est séparée malgré sa publication en 2026. Une contradiction « 7 »/« 17 octobre » reste ouverte. La description d’un décryptage conteste aussi une prétendue agression : le commentaire reste un discours à analyser, pas une preuve de l’agression.

À consulter : [Décisions et preuves du tri documentaire](https://github.com/ClaralBbb/Projet-Info-IA-Polarisation/blob/main/methodologie/pilote_v1/tri_evenement_france/decisions_documentaires_50.json)

À consulter : [Métadonnées publiques archivées](https://github.com/ClaralBbb/Projet-Info-IA-Polarisation/blob/main/methodologie/pilote_v1/tri_evenement_france/metadata_api_snapshot.json)

À consulter : [Export du tri : build(), sans nouveau classificateur](https://github.com/ClaralBbb/Projet-Info-IA-Polarisation/blob/main/methodologie/pilote_v1/tri_evenement_france/construire_tri.py)

## 9. Ce qui vient ensuite — PAS ENCORE EXÉCUTÉ

D’abord : stabiliser le traitement des cas incertains, des suites et du contexte. Puis adapter classify_opinions.py, qui utilise encore l’ancienne grille 0.2, au JSON V1. Choisir et enregistrer le modèle, le prompt, les exemples, les paramètres, les coûts et les sorties. Le script dispose déjà d’une fonction make_request() pour les Structured Outputs, mais n’a pas produit les annotations actuelles.

À consulter : [Futur exécuteur API : make_request(), main()](https://github.com/ClaralBbb/Projet-Info-IA-Polarisation/blob/main/classify_opinions.py)

Ensuite : comparer les sorties automatiques à un échantillon humain indépendant, si possible sans montrer les réponses IA avant la relecture. Les passes précédentes ont servi à construire la grille, pas à mesurer une précision indépendante. Si la qualité et le budget conviennent, étendre à 500–1 000 textes avant davantage. Aucun appel LLM payant n’a été lancé ici.

Enfin : alimenter le dashboard avec les résultats contrôlés, comparer les arguments sur une même proposition, puis définir un indicateur de polarisation. Aucun indice n’est encore validé ; le nombre de critiques ou un score arbitraire de 1 à 10 ne suffit pas. L’étude d’autres sujets et de leurs liens viendra après cette première étape.

À modifier par toi : tu peux corriger directement ce document, activer le suivi des modifications dans Word ou ajouter des commentaires. Cette relecture porte sur l’explication du workflow ; elle ne te demande pas une nouvelle passe de 50 annotations.

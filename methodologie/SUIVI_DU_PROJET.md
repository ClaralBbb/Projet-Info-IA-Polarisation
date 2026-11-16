# Suivi du projet — état au16novembre2026

## Lire ce document

Ce journal distingue ce qui est réalisé, proposé, non validé et restant à faire.
Il ne transforme pas des annotations conversationnelles en résultats d'un modèle
API. « Protocole pilote version1 » signifie une première version écrite et testable
des règles; pas un modèle entraîné, un dictionnaire définitif ou une validation
scientifique déjà acquise.

Le dossier `pilote_v1` est séparé. Aucun ancien résultat, relecture humaine ou
fichier du dashboard n'est remplacé. Aucun appel LLM payant n'est effectué.

## Historique des étapes réalisées

### 1. Collecte exploratoire

Dépôt initialement vide; préparation du collecteur YouTube Data API v3. Recherches
françaises/anglaises autour de manifestations à Paris le17octobre2026. Résultat
archivé :1222 vidéos candidates,234328 commentaires/réponses dont86824 réponses;
22 vidéos avec commentaires désactivés. Source : `data/README.md`.

Les titres, chaînes, dates de publication, liens et commentaires publics
accessibles ont été collectés. Pas de fichiers vidéo téléchargés, pas de comptes
auteurs ajoutés. Les textes peuvent malgré cela contenir des informations
personnelles. Les recherches ne garantissent pas l'exhaustivité de YouTube.
La date de publication ne prouve pas la date des images. Des résultats concernent
d'autres lieux, dates ou sujets. Les comptes de chaînes ne sont pas authentifiés.

**Manque majeur : validation du lien réel des vidéos ET des commentaires avec
l'événement recherché.** Ce contrôle n'a pas encore été effectué. La collecte
n'est donc pas un corpus validé de Paris le17octobre.

### 2. Exploration lexicale et premier dashboard

Normalisation pour comptages, textes originaux conservés, mots/expressions et
thèmes lexicaux, tableaux HTML. `analyze.py`, `reports/`.
Les fréquences ne déterminent ni une opinion, ni un argument, ni une polarisation.

### 3. Passe1 — démonstration d'annotation et relecture humaine

20 commentaires du premier pilote,22 positions proposées directement par
l'assistant conversationnel. Grille acteur/objet/position et exemples fictifs.
`annotation/exemples_ia_20.json`, classeurs de relecture V2.
Relecture humaine reçue :14 lignes renseignées et8 sans verdict. Révisions sur
génération Z, parti de Mélenchon, argument causal, comportements non précisés,
position supplémentaire sur Sarkozy et désaccord ciblé au parent. Un désaccord
sur le commentaire des pavés reste ouvert. `revise_pilot.py`, `pilote_revise.json`.
Les blancs ne sont pas des accords; cette passe sert à développer la grille.

### 4. Extension exploratoire à90 commentaires

Sélection d'un lot500 par mots-clés :250 principaux,250 réponses, maximum2 par
vidéo,188 chaînes déclarées. Le lot est distinct des pilotes initiaux grâce à des
exclusions enregistrées.90 commentaires ont ensuite été lus directement par
l'assistant :118 positions enregistrées dans `plateforme/annotations_60.json`
et `annotations_lot02.json`.

Ce n'est pas l'exécution d'un classificateur entraîné ni d'un script appelant un
LLM. Les regroupements du dashboard par acteurs/actions/familles ont été codés
manuellement pour les positions connues (`actor_scope.py`). Ils ne généralisent
pas aux nouveaux textes. La présence d'une citation dans un texte a été contrôlée;
cela ne prouve pas la justesse de l'interprétation.

### 5. Passe2 — revoir les arguments et les incertitudes

Relecture méthodologique des90 textes, propositions pour20 commentaires
représentatifs,29 lignes de positions. Identifiants Lxxx = ordre du lot500,
à distinguer des Cxxx du premier pilote. Remplacement du regroupement générique
d'action par argument standardisé ET résumé précis; conservation d'une proposition
évaluée pour ne pas mélanger les objets. Séparation pertinence, position,
argument explicite/implicite/ambigu/absent et exploitabilité.

Dictionnaire A01–A12 et M01 proposé manuellement, avec définitions, critères et
exemples, non considéré comme vérité de référence. Diagnostics ARG_ABSENT,
ARG_AUTRE et ARG_AMBIGU. Source : `annotation/validation_arguments_20/`.

Relecture humaine reçue :16 lignes renseignées,13 sans verdict. Révision séparée :
L033 replacé dans sa défense du mouvement face au parent sans effacer ses
positions secondaires; A05 retiré pour L005; L059 conservé comme argument
identifiable non couvert; famille de L063 suspendue; jugements généraux et
allusions sans acte précis exclus du noyau. `revision_01/` préserve le fichier
humain et un journal avant/après. Ces corrections ne mesurent pas une performance
indépendante, puisque les annotations IA étaient visibles.

### 6. Choix actuel du périmètre

**Violences et dégâts autour de la mobilisation**, pas seulement violences
policières : force policière, violences attribuées aux participants, dégradations
et pillages. Police, manifestants, casseurs/pillards/émeutiers et autorités sont
séparés, sans transformer leurs désignations en identités réelles vérifiées.

Politique, Macron, Mélenchon, revendications et médias sont conservés lorsqu'ils
expliquent, justifient ou cadrent ces violences. Les relations doivent être
exprimées, pas déduites d'une simple cooccurrence de mots. L'extension à une
étude exhaustive des autres sujets est différée.

### 7. Protocole pilote1.0 et essai sur50 nouveaux commentaires

Le document `pilote_v1/PROTOCOLE_V1.md` rassemble les consignes dispersées dans la
conversation. Dictionnaire gelé provisoirement `arguments-provisoire-0.1`, JSON
strict et contrôles Python. Ce gel sert à l'essai; pas validation définitive.

50 nouveaux commentaires sélectionnés dans les entrées non utilisées du lot500,
avec exclusion des identifiants ET vidéos des90 précédents :50 vidéos,
25 principaux,25 réponses. Les exclusions initiales du lot500 restent valables.
La graine et les empreintes sont enregistrées. Le lot teste aussi les cas hors
périmètre; il n'a pas été remplacé après découverte de textes difficiles.

Les50 ont été interprétés par l'assistant dans la conversation selon ce protocole
et enregistrés séparément. Aucun appel API, aucune version de modèle API figée,
aucun réentraînement. `execution_conversationnelle.json` précise le mode et les
empreintes. Ce sont de NOUVELLES PROPOSITIONS, sans validation humaine de ce lot.
Le dashboard historique n'est pas mis à jour par cette étape.

### Discussion des modèles et du budget — non exécutée

Les options API LLM, Batch, modèle ouvert local et classificateur spécialisé
(TF-IDF, CamemBERT/XLM-R) ont été discutées. Aucun modèle n'a été entraîné ni
comparé sur un test humain indépendant. Les budgets évoqués étaient indicatifs,
pas des tarifs actuels vérifiés ni une autorisation de dépense. Le souhait d'un
budget limité doit être traduit en estimation mesurée avant exécution. Un prompt
few-shot préparé et un schéma strict ne prouvent pas qu'un appel a été effectué.

## Ce qu'il faut définir ou vérifier ensuite

| Étape | Ce qui manque / décision | Condition avant de généraliser |
| --- | --- | --- |
| Périmètre géographique et temporel | Paris seul ou mobilisation nationale ? Images du17, suites du18/22/24, commémoration1961 et analogies étrangères à séparer. | Règle écrite; indicateur d'événement distinct de la pertinence thématique. |
| Validation des vidéos | Examiner titre, description, dates, éléments de lieu, transcription ou visionnage lorsque disponibles. | Journal avec preuve, statut vérifié/exclu/incertain; ne pas promettre des transcriptions automatiquement accessibles. |
| Lien du commentaire | Un commentaire peut parler d'un autre événement sous une vidéo pertinente, ou inversement. | Décision au niveau vidéo ET commentaire; parent relié mais pas substitué au texte. |
| Unité et comparaisons | Cible, proposition, plusieurs positions, citations de tiers, relation au parent et modalité doivent rester distinctes. | Pas de pour/contre global fabriqué par fusion d'objets différents. |
| Échantillonnage | Définir ce que l'on veut représenter : commentaires, vidéos, sources, langues; mesurer les textes manqués par le lexique. | Lot aléatoire complémentaire sans filtre de mots-clés; pas d'estimation représentative sur le seul lot équilibré. |
| Dictionnaire | Définir activation/retrait/fusion de catégories; examiner ARG_AUTRE et cas ambigus. | Versionner et garder anciens codes/résumés/preuves; réexaminer les anciens rattachements avant comparaison. |
| Exploitabilité | Séparer pertinence, position signée et argument interprétable. | Dénominateurs explicites; descriptions/indéterminables ne deviennent pas favorable/critique. |
| Évaluation humaine | Les passes actuelles ont développé la grille, pas mesuré une précision indépendante. | Prévoir un échantillon indépendant annoté sans voir l'IA, si possible double annotation; comparer erreurs et positions oubliées. |
| Modèle et budget | Choisir modèle local ou API; vérifier langues, matériel, coût et qualité. | Aucun appel payant sans accord; ChatGPT Plus n'inclut pas l'API. |
| Pipeline automatisé | `classify_opinions.py` utilise encore le contrat0.2 et n'alimente pas automatiquement le dashboard. | Adapter l'exécuteur au contratV1, fixer modèle/paramètres/prompt, tester refus/troncatures/coûts/reprise. |
| Passage à des milliers de textes | Évaluer erreurs, couverture et sensibilité aux vidéos/chaînes dominantes. | Ne pas présenter10000 comme garantie de qualité. Les nouvelles sorties doivent être traçables. |
| Polarisation | Définir si l'on mesure désaccords de positions, distance argumentative, délégitimation ou hostilité. | Pas de score1–10 arbitraire ni de polarisation déduite de la seule négativité. |
| Convergences/divergences | Comparer sur une même proposition; distinguer cooccurrence, causalité attribuée, justification et contradiction. | Exemples justificatifs et contrôle de comparabilité des objets. |
| Extension aux autres thèmes | Revendications, médias, institutions et relations inter-thèmes. | Étendre le codebook et valider avant de mélanger les nouvelles catégories aux anciennes statistiques. |

## Ce que l'utilisatrice doit faire maintenant

Pas de nouvelle passe exhaustive demandée. Consulter d'abord le bilan et les
cas signalés du lot50 pour comprendre ce que le protocole résout ou laisse ouvert.
Les décisions de périmètre et de méthode devront être confirmées avant une
exécution massive. Une évaluation humaine indépendante restera nécessaire si
l'objectif est de publier des chiffres fiables sur les positions.

## Ce que ces documents ne prouvent pas

Un JSON conforme ne prouve pas une interprétation juste. Une preuve textuelle
exacte ne prouve pas la vérité d'une accusation. Un lot distinct ne remplace pas
une référence humaine. Les résultats exploratoires ne définissent ni l'opinion
publique ni des groupes stables de personnes. Aucun entraînement de BERT ou
appel automatique o1/o3/autre modèle n'a eu lieu dans ces étapes conversationnelles.

# Bilan du premier essai — propositions, non résultats validés

## Ce qui a été fait

50 nouveaux textes lus par l'assistant conversationnel :48 positions proposées
sur39 commentaires.11 commentaires n'ont pas de position extraite dans le cadre
retenu, sans être effacés.32 commentaires directement pertinents,11 contextuels,
5 incertains et2 hors sujet selon cette lecture provisoire.

22 positions sont proposées comme exploitables,14 à revoir et12 non exploitables
pour une analyse de positions signées. **Ce sont des décisions de l'assistant,
pas des performances mesurées ou22 validations humaines.** Aucun événement n'est
validé. Aucune précision, F1 ou mesure de polarisation n'est calculée.

Les catégories et citations ont été contrôlées automatiquement. Ce contrôle peut
repérer une citation inexacte, pas dire si le modèle comprend correctement l'ironie.
Aucun appel API; il n'existe pas de modèle API figé ni de journal d'appels prouvant
une exécution automatique de ce protocole. Les fichiers JSON sont les sorties
conversationnelles conservées, pas les sorties d'un script classificateur.

## Ce que l'essai met en évidence

1. **Le périmètre doit être vérifié** : N001/N009/N030 parlent d'autres pays,
   N011 de1961; N023 évoque un appel au24 et un titre au22; N026 a un titre mentionnant
   le7. Ces indices ne remplacent pas une vérification vidéo/commentaire. Tous
   gardent statut événement non_verifie, avec leur référence signalée.
2. **Le parent n'est pas toujours suffisant** : N010 mentionne les CRS sans acte
   interprétable dans le parent disponible. N035 ne reprend pas nécessairement
   le scénario de violence du parent. N041 exige de distinguer la réfutation
   d'une causalité gaz/pillage d'un soutien global à la police.
3. **L'ironie peut être interprétable** : N018 est une critique ironique de la
   violence et de la doctrine; certaines positions restent à revoir. N003 etN020
   n'ont pas été forcés dans une lecture univoque.
4. **Description et critique restent délicates** : N025 rapporte une accusation
   très grave sans jugement explicitement formulé. La sortie reste descriptive,
   sans transformer l'assertion en condamnation signée ni en fait vérifié.
5. **Le dictionnaire doit évoluer** :38 arguments interprétables sont proposés,
   dont32 en ARG_AUTRE. Ne pas les transformer en32 familles ni accepter leurs
   résumés sans contrôle. Ce taux important signale une couverture insuffisante
   du dictionnaire ou des décisions de codage à revoir, pas la nécessité de forcer
   les cas dans A01–A12.
6. **Les liens inter-thèmes peuvent être conservés** : certaines sorties relient
   causalement ou par attribution politique la gestion, l'action policière et
   les dégâts. Ces relations sont celles des auteurs, pas des causalités établies.

## Décisions encore nécessaires

- Confirmer Paris seul versus mobilisation française plus large et séparer les
  suites des18/22/24, l'histoire1961 et les comparaisons étrangères.
- Dire si une accusation rapportée sans appréciation évaluative doit rester
  descriptive (N025) ou peut être codée critique implicite sous conditions.
- Clarifier la frontière entre simple thèse et argument normatif : N039 « vive
  la police contre les violences illégitimes »; proposition à revoir, pas exemple
  d'entraînement réputé correct.
- Valider les positions mitigées de gravité ou de responsabilité (N026,N032,N047)
  sans y voir automatiquement un soutien à des violences.
- Examiner les candidats de dictionnaire : utilité protectrice/préventive (N013,
  N039 à interpréter avec prudence); hiérarchisation des préjudices (N032,N048);
  efficacité des modes d'action (N029). Ne pas activer de nouveau code ici.
- Examiner les relations inter-thèmes sur les citations fournies; ne pas compter
  comme relation une simple liste de noms politiques.

## Suite concrète

Le dossier de suivi expose les étapes suivantes et leurs conditions. La priorité
n'est pas de demander une nouvelle annotation exhaustive : il faut confirmer le
périmètre, contrôler quelques cas discutables et préparer la validation vidéo.
Avant une exécution payante, adapter l'exécuteur au nouveau contrat, choisir et
figer le modèle, estimer le coût réel, puis obtenir l'accord de dépense.

Pour une évaluation de qualité, prévoir un autre lot humain indépendant et aveugle
aux sorties IA. Si les50 servent à modifier la grille, ils deviennent un lot de
développement et ne doivent pas être réutilisés comme test indépendant.

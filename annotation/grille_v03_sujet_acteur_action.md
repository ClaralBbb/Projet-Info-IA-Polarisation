# Grille 0.3 — sujet, acteur, action et position

Sujet principal unique : **Violences et dégâts**.

Une ligne analytique représente une position, pas le commentaire complet. Les
textes et annotations antérieurs restent conservés. La version0.3 est pour le
moment une revue explicite de périmètre appliquée aux 118 positions déjà lues;
ce n'est pas une nouvelle exécution LLM automatique.

## Ordre de lecture

1. Le texte porte-t-il sur le sujet ? Les médias, rôles politiques généraux,
   revendications ou autres événements ne deviennent pas des violences de2026.
2. Quel acteur est **évalué par cette position** ? Garder la désignation précise.
3. Quelle action ou quel jugement est évalué ? Ne pas confondre l'acteur qui
   utilise la force et la personne qui la subit.
4. Quelle attitude l'auteur exprime-t-il envers cette action ?
5. Quelle citation prouve cette lecture ? Quel argument est réellement donné ?
6. Le parent est-il nécessaire et suffisant ? L'acteur est-il explicite ou implicite ?

## Catégories

Acteurs : police; manifestants; casseurs/pillards/émeutiers; autres autorités;
autres acteurs; acteur non établi. « Casseurs » et « manifestants » sont les
qualifications présentes dans les discours, pas des identités vérifiées ou des
groupes nécessairement exclusifs dans les faits. Une insulte de l'auteur ou une
attribution de responsabilité n'établit pas les faits ni le profil d'une personne.

Actions : coups/gaz/force; violences attribuées aux participants; dégradations/
incendies/pillages; intervention/prévention/sanctions; jugements généraux sur les
acteurs dans le contexte de la violence. Ces derniers sont affichables séparément
pour ne pas les prendre pour une position sur une intervention précise.

Positions : critique/condamne; justifie/soutient; nuance; décrit sans position;
indéterminée. Un soutien est local à l'acte jugé, pas un pro/anti-acteur universel.

Si le responsable de l'action n'est pas identifiable, conserver « acteur non
établi »; ne pas déduire police ou manifestants à partir du seul titre. Les
références historiques ou étrangères ne sont pas comptées comme des observations
sur les violences françaises de2026. Les positions hors sujet restent dans l'Excel.

## Pourcentages

Une unité = commentaire × acteur, pour les filtres sélectionnés. Si un même texte
contient deux attitudes différentes envers le même acteur, le ranger dans mixte,
plutôt que compter deux fois le texte. Un commentaire peut évaluer plusieurs
acteurs : il contribue alors à plusieurs lignes d'acteurs, chacune avec son propre
dénominateur. Les pourcentages des différents acteurs ne s'additionnent pas.

La catégorie mixte doit être lue avant interprétation : soutien aux interpellations
et refus des coups peuvent coexister sans contradiction. Ce n'est pas un score
de polarisation. Les pourcentages affichent aussi les effectifs, y compris les
petits volumes. Par défaut, lectures et attributions d'acteurs explicites seulement.

## Ce qui est fait dans le code

`actor_scope.py` contient les acteurs, actions et décisions de revue indexées par
numéro de commentaire et position. Les règles ne cherchent pas des mots dans les
textes pour inventer une position; elles référencent les lectures déjà enregistrées.
Le module est volontairement limité au lot analysé; une nouvelle position sans
règle est exclue de la comparaison tant qu'elle n'a pas fait l'objet d'une revue.

`build_platform.py` ajoute les familles d'arguments, uniquement quand un argument
est enregistré. Il assemble les données du site, pas un classificateur automatique.
Le code d'appel API dans `classify_opinions.py` et son schéma0.2 restent historiques
et n'ont pas été exécutés; ils doivent être adaptés à cette grille avant une
future exécution payante. Aucun nouveau score de clivage n'est ajouté.

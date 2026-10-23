# Rapport exploratoire des commentaires

Télécharger **rapport.html**, puis l'ouvrir dans un navigateur. Le rapport est
interactif et autonome : aucun serveur, aucune connexion et aucune clé API requis.
GitHub affiche le code HTML; son aperçu ne lance pas l'interface.

Le rapport présente :

- Les effectifs du corpus et les indicateurs de qualité.
- Les mots et expressions les plus présents par commentaire.
- La comparaison tous / textes uniques / commentaires principaux / réponses.
- Des catégories thématiques définies par mots-clés explicites.
- La concentration des commentaires par vidéo.
- 400 extraits filtrables pour préparer une annotation manuelle.

**Ce rapport ne mesure pas la polarisation.** Les fréquences ne déterminent pas
une opinion ni le soutien à une cause. Les vidéos candidates doivent être
validées. Les formes fléchies ne sont pas regroupées et la langue n'est pas
détectée automatiquement; les mots vides français et anglais sont filtrés.
Les tokens sont limités aux lettres latines normalisées a–z : les écritures
non latines ne sont pas analysées.
Les catégories peuvent se chevaucher et les mots-clés être ambigus.

Le masquage des extraits est partiel et ne garantit pas l'anonymat. Les extraits
sont limités à 1 200 caractères; le corpus original n'est jamais modifié.

## Reproduire

Depuis la racine du dépôt, avec les dépendances installées :

```bash
.venv/bin/python analyze.py
.venv/bin/python -m unittest -v
```

Le script utilise le JSON brut local s'il est présent; sinon il lit l'Excel suivi
dans Git. Pour forcer la source :

```bash
.venv/bin/python analyze.py --input data/paris_2026-10-17.xlsx
```

La synthèse conserve le nom et l'empreinte SHA-256 du fichier source et l'heure
de génération. La sélection de lecture utilise la graine 42 : un commentaire
analysable tiré au sort par vidéo, puis au maximum 400 vidéos tirées au sort.
Cet échantillon privilégie la diversité des vidéos, pas la représentativité
statistique des commentaires. Les textes uniques gardent la première occurrence
rencontrée, après normalisation de casse, d'espaces et d'entités HTML.

## Fichiers

- `rapport.html` : interface interactive autonome.
- `frequences.csv` : 50 premiers mots et 40 premières expressions par vue.
- `themes.csv` : effectifs et dénominateurs des thèmes par vue.
- `annotation_400.csv` : extraits et champs d'annotation laissés vides.
- `synthese.json` : données agrégées et extraits utilisés par le rapport.

Le HTML affiche les 30 premiers mots et les 30 premières expressions.
L'annotation proposée demande d'abord la pertinence de la vidéo, puis la cible,
la position, l'incertitude et une note. Définir un protocole commun avant de
remplir ces champs; un vocabulaire de thèmes n'est pas un classificateur d'opinion.

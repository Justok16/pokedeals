# 05 — Tableau de bord central

## Pourquoi un tableau de bord avant le premier contenu

Sans mesure, la décision d'arrêter un projet se prend à l'humeur — et l'humeur
dit toujours de continuer, parce qu'on a déjà investi du temps. Le tableau de
bord existe pour rendre l'arrêt **mécanique**.

## Schéma des données

Deux tables. Rien de plus tant qu'il n'y a pas de revenu.

### Table `contenus` — une ligne par contenu publié

| Champ | Type | Note |
|---|---|---|
| `projet` | texte | ID du concept (A1, A2, D3…) |
| `niche` | texte | la profession / verticale ciblée |
| `plateforme` | texte | TikTok, Shorts, beehiiv, site |
| `contenu_id` | texte | URL ou identifiant |
| `date` | date | |
| `format` | texte | numéro de veille / fiche comparateur / vidéo courte / page |
| `hook` | texte | les 3 premières secondes ou le titre — **c'est la variable la plus prédictive** |
| `duree` | entier | secondes |
| `vues` | entier | |
| `impressions` | entier | |
| `retention_3s` | décimal | % |
| `ctr` | décimal | % |
| `abonnements` | entier | gagnés grâce à ce contenu |
| `commentaires` | entier | |
| `clics_sortants` | entier | **le prédicteur de revenu le plus fiable** |
| `conversions` | entier | inscriptions, ventes |
| `revenu` | décimal | € attribués |
| `cout` | décimal | € dépensés |
| `temps_production` | entier | minutes réelles |
| `revenu_estime_par_contenu` | décimal | calculé |
| `statut` | énum | cf. ci-dessous |
| `decision` | texte | la décision prise et **sa date** |

### Table `projets` — une ligne par concept, mise à jour chaque semaine

`projet`, `semaine`, `statut`, `inscrits_cumules`, `revenu_semaine`,
`cout_semaine`, `marge`, `heures_investies`, `revenu_par_heure`,
`hypothese_en_cours`, `seuil`, `echeance`, `decision`.

Le champ qui décide de tout à moyen terme est **`revenu_par_heure`** : un
projet qui rapporte 300 €/mois en 2 h/semaine bat un projet à 800 €/mois en
20 h/semaine (cf. critère de richesse, `08`).

Modèle CSV prêt à l'emploi : [`modeles/tableau_de_bord.csv`](modeles/tableau_de_bord.csv).

## Statuts

| Statut | Définition | Sortie possible |
|---|---|---|
| **TEST** | Hypothèse en cours, échéance fixée | PROMETTEUR ou STOP |
| **PROMETTEUR** | Seuil atteint, mais pas encore de revenu | SCALE ou STOP |
| **SCALE** | On augmente délibérément la production | MONÉTISATION ou STOP |
| **MONÉTISATION** | Revenu mesuré, on optimise la marge | BUSINESS ou STOP |
| **BUSINESS** | Revenu récurrent, actif autonome et automatisé | reste, ou revente |
| **STOP** | Arrêté. La date et la raison sont écrites. | archivé, jamais supprimé |

Un projet ne saute pas d'étape. Passer de TEST à SCALE sans revenu mesuré est
l'erreur la plus coûteuse possible : on industrialise une chose qui ne marche
pas.

## Règle de KILL

Avant tout test, quatre lignes sont écrites (sinon le test ne commence pas) :

```
HYPOTHÈSE : ...
MÉTRIQUE  : ... (une seule, chiffrée)
ÉCHÉANCE  : JJ/MM (date ferme)
SEUIL     : ... (le nombre en dessous duquel on arrête)
```

À l'échéance, une seule des quatre décisions est prise, le jour même :

- **CONTINUER** — seuil atteint, on poursuit à l'identique ;
- **MODIFIER** — signal partiel : on change **une seule variable** (le format,
  le hook ou le canal), et on relance un test daté ;
- **AMPLIFIER** — seuil largement dépassé → règle de SCALE ;
- **ARRÊTER** — seuil non atteint. On arrête **le jour même**.

**Le temps déjà investi n'est jamais un argument.** Il est dépensé, il ne
reviendra pas, et il ne dit rien sur la suite. C'est la règle la plus difficile
à appliquer et la plus rentable.

**Exception unique** : un test dont la mesure a été cassée (suivi absent,
données perdues) est **rejoué**, pas prolongé.

## Règle de SCALE

Quand un concept dépasse son seuil, **ne pas produire simplement plus de la même
chose**. Ordre d'amplification, du moins cher au plus cher :

1. **Comprendre pourquoi** — identifier les 3 contenus gagnants et ce qu'ils ont
   en commun (hook ? donnée ? format ?). Sans cette étape, l'amplification
   duplique du hasard.
2. **Refaire le gagnant** sous d'autres angles (même promesse, autre entrée).
3. **Augmenter la fréquence** seulement si la qualité tient.
4. **Récupérer l'audience** : tout pousser vers la newsletter (actif possédé).
5. **Brancher l'affiliation** sur les contenus les plus cliqués.
6. **Ajouter un format long** (page SEO, vidéo longue) sur le sujet gagnant.
7. **Dupliquer sur une 2ᵉ profession** avec la même méthode de veille.
8. **Passer à l'anglais** (cf. `08`) une fois le concept FR stabilisé.
9. **Créer le produit** seulement quand l'audience a exprimé le problème.
10. **Automatiser** ce qui est devenu répétitif — et pas avant.

## Revue hebdomadaire (dimanche, 30 min)

1. Lire le tableau (5 min).
2. Pour chaque projet : le signal progresse-t-il ? (10 min)
3. Appliquer KILL/SCALE sur les échéances arrivées (10 min).
4. Écrire la décision et sa raison dans `decision` (5 min).

Si la revue dépasse 30 minutes, le problème est le tableau, pas la revue.

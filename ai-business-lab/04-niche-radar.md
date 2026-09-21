# 04 — Niche Radar

## Rôle

Empêcher que cette étude, datée du 21/09/2026, devienne la vérité permanente du
projet. Le Radar cherche en continu des opportunités **meilleures que celles du
portefeuille actuel**, et doit pouvoir dire : « ce que tu fais aujourd'hui n'est
plus le meilleur usage de ton temps ».

C'est aussi la réponse à une contrainte du cahier des charges : ne jamais
considérer une niche comme définitivement gagnante.

## Principe de conception

Le Radar ne doit **rien coûter** et prendre **moins de 30 minutes par semaine**.
Au démarrage il est manuel et assisté ; il ne s'automatise qu'une fois la
routine faite cinq fois à la main.

```
lundi (20 min)   ->  collecte des sources publiques
                 ->  extraction des signaux (nouveautés, croissance, douleurs)
                 ->  filtrage (déjà vu ? hors critères ? trop petit ?)
dimanche (10 min)->  1 à 3 fiches d'opportunité + arbitrage
```

## Sources, par ordre de fiabilité

| Source | Ce qu'elle détecte | Gratuit | Fiabilité |
|---|---|---|---|
| **Sources officielles** (Légifrance, service-public, URSSAF, DGFiP, fédérations) | **Changements réglementaires datés** = demande contrainte | Oui | **La plus haute** : c'est ainsi qu'on repère une fenêtre comme la facturation électronique |
| **Pages officielles de monétisation** (YouTube, TikTok, plateformes) | Changement de règles = risque ou opportunité | Oui | **La plus haute** (source primaire) |
| **Communautés professionnelles** (groupes, forums, commentaires) | Problèmes récurrents exprimés spontanément | Oui | Moyenne, mais irremplaçable pour détecter une douleur |
| **Catalogues de programmes d'affiliation** | Nouveaux programmes, taux récurrents | Oui | Bonne |
| **Pages tarifaires et nouveautés des éditeurs** | Marchés qui se créent, budgets qui existent | Oui | Bonne |
| **data.gouv.fr et portails open data** | Jeux de données exploitables (concept B1) | Oui | Bonne |
| Google Trends | Croissance/déclin de requêtes FR | Oui | Moyenne (indice relatif, pas un volume) |
| **Vos propres métriques** | Ce que votre audience cherche et clique | Oui | **La plus haute une fois qu'elle existe** |

**Règle de source** : un signal n'est retenu que s'il est confirmé par **deux
sources indépendantes**, ou s'il vient d'une **source primaire**. Un article de
blog annonçant une tendance n'est pas une donnée.

## Priorités de surveillance

1. **Échéances réglementaires françaises** — la meilleure source d'opportunités
   pour un média B2B francophone : demande contrainte, datée, non concurrencée
   par les plateformes internationales. (C'est ce qui a produit le concept A1.)
2. **Changements de règles de monétisation** — peut détruire un actif du jour
   au lendemain.
3. **Nouveaux programmes d'affiliation récurrents** — gain immédiat, coût nul.
4. **Douleurs récurrentes exprimées par l'audience existante** — la seule source
   légitime d'un produit (règle : problème → demande → validation → solution).
5. **Marchés où des éditeurs dépensent déjà** — là où il y a des annonceurs, il
   y a un modèle économique.
6. **Nouveaux outils IA** qui réduisent un coût de production réel.

## Fiche d'opportunité

Modèle complet : [`modeles/fiche-opportunite.md`](modeles/fiche-opportunite.md).
Elle reprend les 15 rubriques demandées, **plus trois ajouts** qui tranchent
réellement :

- **Avantage défendable** : qu'est-ce qu'un concurrent équipé des mêmes IA ne
  peut pas copier en une semaine ? (Si la réponse est « rien », la fiche est
  archivée, quel que soit le potentiel.)
- **Vitesse de validation** : en combien de temps saura-t-on qu'on se trompe ?
- **Coût d'opportunité** : qu'arrête-t-on pour la prendre ? Le temps est la
  seule ressource vraiment rare — 4 h/jour, pas 4 h/jour par projet.

## Règle d'arbitrage (dimanche, 10 min)

Une fiche ne devient un test que si elle remplit les **trois** conditions :

1. score ≥ au **plus faible concept actuellement actif** (ajouter la fiche à
   `outils/concepts.yaml` et relancer `scorer.py`) ;
2. testable en **moins de 15 jours** avec ≤ 10 h de travail ;
3. un **seuil d'échec** est écrit avant de commencer.

Sinon la fiche est **archivée, pas supprimée**. Une opportunité écartée en
septembre peut devenir évidente en mars : ce qui change, c'est le contexte.

## Trois règles ajoutées le 21/09/2026

Les deux premiers passages et la comparaison avec une exécution externe du même
prompt (cf. [`10-comparaison-chatgpt.md`](10-comparaison-chatgpt.md)) ont mis en
évidence trois manques. Ils sont corrigés ici.

### R-A — Balayer les échéances **UE avant** les échéances FR

Le premier passage ne regardait que les échéances françaises. Le second, en
élargissant à l'Europe, a sorti en une requête la directive EmpCo — applicable
**six jours plus tard**, et absente des cinq numéros déjà rédigés.

Une obligation européenne précède **toujours** le texte français qui la
transpose. La regarder en second, c'est la découvrir en retard. Six jours de
marge cette fois ; il n'y en aura pas toujours.

### R-B — Séparer **annonce datée** et **offre simplement revérifiée**

Emprunté à la veille de ChatGPT, qui le fait mieux que ce Radar ne le faisait.
Chaque élément d'une fiche est désormais étiqueté :

| Étiquette | Sens |
|---|---|
| **Annonce datée** | Un fait nouveau, avec sa date de publication |
| **Offre revérifiée** | Une offre qui existait déjà, simplement recontrôlée ce jour |
| **Non mesuré** | Ce que la veille n'a **pas** regardé — à écrire explicitement |

La troisième ligne est la plus importante : une veille qui ne dit pas ce qu'elle
n'a pas mesuré laisse croire qu'elle a tout mesuré.

### R-C — Le test du **concurrent gratuit**

Avant qu'une fiche ne devienne un test, une question supplémentaire :
**qui le fait déjà gratuitement, et depuis combien de temps ?**

Origine du signal : une exécution externe du prompt a bâti un calculateur de
marge payant pour revendeurs, avant de constater qu'un acteur du marché offrait
déjà la fonction **gratuitement** — et publiait en plus les guides pédagogiques
censés attirer l'audience.

Un concurrent gratuit et installé ne tue pas seulement le prix : il tue aussi
l'angle éditorial, parce qu'il produit le même contenu pour vendre son outil.

**Cette question vient avant les trois conditions d'arbitrage**, pas après.

## Ce que le Radar ne fera pas

- Il ne donnera **pas** de liste de « niches rentables ». Une niche n'est pas
  rentable en soi : elle l'est pour quelqu'un qui a un avantage dedans.
- Il ne remplacera **pas** la décision. Il produit des candidats argumentés ;
  l'arbitrage reste humain, parce qu'il engage du temps de vie.

## Automatisation (plus tard, pas maintenant)

Quand la routine aura été faite cinq fois à la main : script hebdomadaire de
collecte, sortie dans `ai-business-lab/opportunites/AAAA-MM-JJ-<slug>.md`,
notification. Coupe-circuit par source : une source qui échoue trois fois de
suite est abandonnée pour le cycle, les autres continuent.

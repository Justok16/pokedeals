# 04 — Niche Radar

## Rôle

Empêcher que cette étude, datée du 21/09/2026, devienne la vérité permanente du
projet. Le Radar cherche en continu des opportunités **meilleures que celles du
portefeuille actuel**, et doit pouvoir dire : « ce que tu fais aujourd'hui n'est
plus le meilleur usage de ton temps ».

## Principe de conception

Le Radar ne doit **rien coûter** et **rien demander manuellement**. Il reprend
exactement le modèle déjà en production dans ce dépôt : un cron GitHub Actions
hebdomadaire, des sources publiques, un fichier d'état versionné, une
notification. Aucune infrastructure nouvelle.

```
lundi 08:00  ->  collecte sources publiques
             ->  extraction de signaux (nouveautés, croissance, douleurs)
             ->  filtrage (déjà vu ? hors critères ? trop petit ?)
             ->  rédaction de 1 à 3 fiches d'opportunité
             ->  notification Telegram + commit dans strategie/opportunites/
             ->  arbitrage humain le dimanche (30 min)
```

## Sources, par ordre de fiabilité

| Source | Ce qu'elle détecte | Accès gratuit | Fiabilité |
|---|---|---|---|
| **Données internes PokéDeals** | Ce que les gens cherchent, quelles cartes bougent, quelles boutiques cassent les prix | Oui, déjà là | **La plus haute** : ce sont des faits observés, pas des déclarations |
| Google Trends | Croissance/déclin de requêtes FR | Oui (interface ; extraction non officielle fragile) | Moyenne (indice relatif, pas un volume) |
| Reddit / forums FR | Problèmes récurrents exprimés spontanément | Oui (flux JSON publics) | Moyenne, mais excellente pour repérer une douleur |
| Pages nouveautés des plateformes SaaS | Nouveaux outils, nouveaux marchés | Oui | Bonne |
| Pages officielles de monétisation (YouTube, TikTok) | **Changement de règles** = risque ou opportunité | Oui | **La plus haute** (source primaire) |
| Annuaires de programmes d'affiliation | Nouveaux programmes, meilleurs taux | Oui | Bonne |
| Registres/dépôts de noms de domaine | Nouveaux entrants sur une niche | Oui (déjà exploité par `decouverte_boutiques.py`) | Bonne |

**Règle de source** : un signal n'est retenu que si **deux sources
indépendantes** le confirment, ou si la source est primaire (la plateforme
elle-même). Un article de blog qui annonce une tendance n'est pas une donnée.

## Ce que le Radar surveille en priorité (par ordre de valeur)

1. **Changements de règles de monétisation** — c'est ce qui peut détruire un
   actif du jour au lendemain (cf. YouTube 2026). Priorité absolue.
2. **Nouveaux programmes d'affiliation mieux rémunérés** dans les niches déjà
   couvertes — gain immédiat, coût nul.
3. **Douleurs récurrentes exprimées** par l'audience existante — la seule source
   légitime d'un nouveau produit (cf. règle « problème → demande → validation →
   solution »).
4. **Nouveaux TCG / marchés de collection en croissance** — coût marginal quasi
   nul grâce au moteur existant.
5. **Nouveaux outils IA** qui réduisent un coût de production réel.
6. **Changements réglementaires** (influence commerciale, RGPD, fiscalité).

## Fiche d'opportunité

Modèle complet : [`modeles/fiche-opportunite.md`](modeles/fiche-opportunite.md).

Elle reprend les 15 rubriques demandées (problème, audience, demande, tendance,
concurrence, monétisation, affiliation, produit, SaaS, international, risques,
coût, difficulté d'automatisation, hypothèses) **plus deux ajouts** qui
tranchent réellement :

- **Levier sur l'existant** : qu'est-ce que cette opportunité réutilise de ce
  qui tourne déjà ? (Si la réponse est « rien », la barre d'acceptation monte
  fortement.)
- **Coût d'opportunité** : qu'est-ce qu'on arrête pour la prendre ? Le temps est
  la seule ressource vraiment rare ici — 4 h/jour, pas 4 h/jour par projet.

## Règle d'arbitrage (le dimanche, 30 min)

Une fiche ne devient un test que si elle remplit les **trois** conditions :

1. score ≥ au **plus faible concept actuellement actif** (calculé avec
   `outils/scorer.py`, en ajoutant la fiche à `concepts.yaml`) ;
2. testable en **moins de 15 jours** avec ≤ 10 h de travail ;
3. un **seuil d'échec** est écrit avant de commencer.

Sinon la fiche est archivée — pas supprimée. Une opportunité écartée en
septembre peut devenir évidente en mars ; ce qui change, c'est le contexte, pas
la fiche.

## Ce que le Radar ne fera pas

- Il ne donnera **pas** de liste de « niches rentables ». Une niche n'est pas
  rentable en soi : elle l'est pour quelqu'un qui a un avantage dedans.
- Il ne remplacera **pas** la décision. Il produit des candidats argumentés ;
  l'arbitrage reste humain, parce qu'il engage du temps de vie.

## Implémentation (à écrire en phase 4)

Fichier `strategie/outils/niche_radar.py`, cron hebdomadaire, sortie dans
`strategie/opportunites/AAAA-MM-JJ-<slug>.md`, notification Telegram réutilisant
`telegram_utils.py` déjà présent dans le scraper. Anti-spam et coupe-circuit sur
le modèle des connecteurs existants : une source qui échoue 3 fois de suite est
abandonnée pour le cycle, les autres continuent.

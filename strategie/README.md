# AI Business Lab — dossier stratégique

> Étude réalisée le 21/09/2026. Tout ce qui est écrit ici est daté et révisable.
> Les sources externes sont citées dans [`01-etude-marche.md`](01-etude-marche.md).
> Distinction systématique : **[DONNÉE]** = observé et sourcé · **[ESTIMATION]** =
> calcul à partir de données · **[HYPOTHÈSE]** = à vérifier par un test ·
> **[OPINION]** = position stratégique assumée.

## Sommaire

| Document | Contenu |
|---|---|
| [01 — Étude de marché](01-etude-marche.md) | Données 2026 : marché TCG, règles de monétisation, affiliation, plateformes, cadre légal FR |
| [02 — Portefeuille de concepts](02-portefeuille-concepts.md) | 15 concepts notés sur 18 critères, classés par un score reproductible |
| [03 — Plan d'exécution](03-plan-execution.md) | Phases 1 à 10 + plan jour par jour des 90 premiers jours |
| [04 — Niche Radar](04-niche-radar.md) | Système de veille permanente d'opportunités (spécification + sources gratuites) |
| [05 — Tableau de bord](05-tableau-de-bord.md) | Schéma de base, statuts, règle de KILL, règle de SCALE |
| [06 — Monétisation et risques](06-monetisation-risques.md) | 8 sources de revenus chiffrées + registre des risques |
| [07 — Automatisation et agents](07-automatisation-agents.md) | Les 15 agents, et ce qui doit rester humain |
| [08 — Trajectoire 12 mois / 3-5 ans](08-roadmap.md) | Direction stratégique, pas une promesse |
| [09 — Outils et budget](09-outils-et-budget.md) | Stack 0 € puis règles de réinvestissement |
| [`outils/`](outils/) | Le moteur de scoring (code + données + tests) |
| [`modeles/`](modeles/) | Modèles réutilisables : fiche opportunité, fiche de test, prompts d'agents |

---

## DÉCISION

**Ne pas démarrer un portefeuille de médias à partir de zéro. Construire d'abord
le portefeuille autour de l'actif qui tourne déjà : PokéDeals.**

Le brief initial décrit un profil "débutant, 0 €, aucune compétence forte". Ce
n'est **pas** la situation réelle observée dans ce dépôt, et c'est le point le
plus important de toute cette étude.

Ce qui existe déjà, en production, aujourd'hui :

- un moteur de veille de prix sur **83+ boutiques** FR/JP + eBay + Vinted +
  Leboncoin, avec coupe-circuits, watchdog et tests automatisés ;
- une **base de cotes propriétaire** (`data/cotes.json`, avec le nombre
  d'annonces ayant alimenté chaque cote) et un historique de prix ;
- une **infrastructure d'automatisation à 0 €/mois** : ~20 workflows GitHub
  Actions en cron, sans serveur ni base à payer ;
- un **SaaS** déjà branché (watchlists utilisateurs, alertes push/email,
  Supabase) dans un dépôt séparé ;
- un projet dérivé déjà cadré (**PokéPrécoms**) ;
- et une compétence de programmation/automatisation très au-dessus de "2/5".

**[OPINION]** Repartir de zéro sur "quelle niche choisir" serait la pire
décision disponible : cela jetterait 100 % d'un avantage que personne d'autre
n'a, pour entrer sur des marchés (outils IA, finance perso) où des centaines de
concurrents mieux armés sont déjà installés.

## POURQUOI

1. **La donnée propriétaire est la seule barrière à l'entrée réelle dans un
   monde où l'IA rend le contenu gratuit.** N'importe qui peut générer 50
   vidéos par jour. Personne d'autre ne peut dire *« cette carte est à 32 € chez
   X alors que sa cote FR réelle est à 58 €, et voici l'historique »*.
2. **YouTube a fermé la porte à la stratégie "volume IA" en 2026.** La politique
   de contenu non authentique s'évalue désormais **au niveau de la chaîne** et
   non plus vidéo par vidéo, avec un système à trois paliers allant jusqu'au
   retrait définitif du programme partenaire ([DONNÉE], cf. 01). Une stratégie
   de "faceless à haut volume" est donc un actif à risque de destruction totale.
   Un contenu adossé à une base de données est, lui, structurellement original.
3. **Le marché est porteur et français.** Pokémon = 61 % du marché français des
   jeux de cartes, ~4 millions de collectionneurs français, marché des jeux de
   cartes FR +12 % sur un an ([DONNÉE], cf. 01).
4. **Le coût marginal d'un nouveau concept est proche de zéro** quand il
   réutilise un moteur déjà écrit : ajouter Lorcana ou One Piece, c'est changer
   une watchlist, pas écrire un produit.
5. **L'objectif déclaré est le patrimoine, pas les vues.** Une newsletter, un
   comparateur et une API se revendent ; une chaîne TikTok faceless générique,
   beaucoup plus difficilement.

## DONNÉES

Les 6 chiffres qui pilotent cette décision (détail et sources dans `01`) :

| Donnée | Valeur | Source |
|---|---|---|
| Part de Pokémon sur le marché FR des jeux de cartes | 61 % | SRTCG |
| Collectionneurs français estimés | ~4 millions | SRTCG |
| Croissance marché FR jeux de cartes | +12 % sur un an (Pokémon +18 % en 2024) | SRTCG |
| RPM TikTok France (Creator Rewards) | ~0,40 à 1,20 € / 1000 vues qualifiées | TikTrends/Quasa |
| Affiliation Amazon, catégorie jeux | ~1 à 3 % | Amazon Partenaires |
| Abonnement d'un concurrent direct (Collectr PRO) | 4,99–7,99 $/mois ou 59,99 $/an | Collectr |

**Lecture critique de ces chiffres** : à 1,20 € de RPM maximum, il faut
**830 000 vues pour gagner 1 000 €** sur TikTok. À l'inverse, **200 abonnés à
5 €/mois font 1 000 €/mois récurrents**. C'est tout l'argument de cette étude :
le revenu ne vient pas de l'audience, il vient de ce qu'on vend à l'audience.

## HYPOTHÈSES

Ce qui n'est **pas** démontré et doit être testé :

- **H1** — Les collectionneurs FR veulent recevoir une synthèse hebdomadaire des
  prix par email (et pas seulement des alertes temps réel).
- **H2** — Une partie de cette audience paie pour de l'information/des outils.
- **H3** — Les boutiques TCG FR acceptent des liens d'affiliation ou une mise en
  avant payante dans un comparateur.
- **H4** — Le contenu court alimenté par des données réelles surperforme le
  contenu Pokémon générique sur TikTok/Shorts FR.
- **H5** — La cote FR propriétaire a une valeur commerciale pour des vendeurs
  professionnels.

Chacune a un test, un seuil et une date dans [`03-plan-execution.md`](03-plan-execution.md).

## ACTIONS (les 7 prochaines, dans l'ordre)

1. **Lire ce dossier en entier une fois**, puis contester au moins un choix :
   la grille de poids est dans `outils/criteres.yaml` et se rejoue en une
   commande.
2. **Lancer la newsletter (A2)** : compte beehiiv gratuit, page d'inscription,
   premier numéro généré automatiquement depuis `data/cotes.json`.
3. **Brancher la capture d'emails** sur ce qui existe déjà (bot Telegram, SaaS).
4. **Publier le comparateur boutiques (D3)** en version statique, à partir des
   83 boutiques déjà scannées.
5. **Ouvrir 2 comptes courts (A1)** — TikTok + YouTube Shorts — avec un format
   unique : « la donnée du jour », 1 publication/jour, 30 jours.
6. **Dupliquer le moteur sur un 2ᵉ TCG (B1)** : Lorcana ou One Piece, watchlist
   uniquement.
7. **Activer le Niche Radar** (`04`) en cron hebdomadaire, pour ne jamais
   dépendre de cette seule étude.

## AUTOMATISATION

Ce qui est automatisable **immédiatement** avec l'existant : génération du
numéro de newsletter, production des scripts vidéo à partir des deals réels,
mise à jour du comparateur, collecte des métriques, exécution du Niche Radar.
Détail et limites dans [`07-automatisation-agents.md`](07-automatisation-agents.md).

## COÛT

**0 €/mois** pour l'intégralité de la phase 1 (détail dans `09`). Le premier
euro dépensé n'arrive qu'après un revenu démontré, et jamais sur un outil dont
la version gratuite suffit.

## KPI

La règle : **aucun KPI de vanité**. Les seuls chiffres suivis sont dans
[`05-tableau-de-bord.md`](05-tableau-de-bord.md) — abonnés email, clics
sortants, conversions, revenu par contenu, coût, temps de production.

## PROCHAINE ÉTAPE

Décider, avant toute production, quels concepts entrent dans le premier lot de
test (recommandation : **A2 + D3 + A1**, et **B1** en tâche de fond). Le
calendrier exact est dans [`03-plan-execution.md`](03-plan-execution.md).

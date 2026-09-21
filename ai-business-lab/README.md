# AI Business Lab — dossier stratégique

> Étude réalisée le 21/09/2026, pour un **démarrage à zéro** : aucun actif,
> aucune audience, aucun revenu en ligne, 0 € de budget, 4 h/jour, travail
> faceless sous pseudonyme, marché francophone.
> Sources externes citées dans [`01-etude-marche.md`](01-etude-marche.md).
> Distinction systématique : **[DONNÉE]** = observé et sourcé · **[ESTIMATION]**
> = calcul à partir de données · **[HYPOTHÈSE]** = à vérifier par un test ·
> **[OPINION]** = position stratégique assumée.

## Sommaire

| Document | Contenu |
|---|---|
| [01 — Étude de marché](01-etude-marche.md) | Données 2026 : RPM/CPM par niche, règles de monétisation, affiliation récurrente, SEO programmatique, cadre légal FR |
| [02 — Portefeuille de concepts](02-portefeuille-concepts.md) | 15 concepts notés sur 18 critères, classés par un score reproductible |
| [03 — Plan d'exécution](03-plan-execution.md) | Phases 1 à 10 + plan jour par jour des 90 premiers jours |
| [04 — Niche Radar](04-niche-radar.md) | Veille permanente d'opportunités (sources gratuites, cadence hebdo) |
| [05 — Tableau de bord](05-tableau-de-bord.md) | Schéma de mesure, statuts, règle de KILL, règle de SCALE |
| [06 — Monétisation et risques](06-monetisation-risques.md) | 8 sources de revenus chiffrées + registre des risques |
| [07 — Automatisation et agents](07-automatisation-agents.md) | Les 15 agents, et ce qui doit rester humain |
| [08 — Trajectoire 12 mois / 3-5 ans](08-roadmap.md) | Direction stratégique, pas une promesse |
| [09 — Outils et budget](09-outils-et-budget.md) | Stack 0 € puis règles de réinvestissement |
| [`outils/`](outils/) | Le moteur de scoring (code + données + tests) |
| [`modeles/`](modeles/) | Fiche opportunité, fiche de test, prompts d'agents, modèle de tableau de bord |
| [`lancement/`](lancement/) | **Kit de lancement de la verticale choisie (e-commerçants français)** : démonstration du choix, sources de veille, 4 premiers numéros, plan du comparateur, affiliation récurrente, 30 contenus courts |

---

## DÉCISION

**Construire un actif B2B francophone de niche — pas une chaîne de
divertissement faceless.** Concrètement, le premier lot est :

1. **A4 — une newsletter de veille pour une profession précise** (score 81.4) ;
2. **A1 — un média d'accompagnement sur la facturation électronique** (78.3),
   dont l'échéance légale crée une demande contrainte pendant 12 mois ;
3. **B2 — un comparateur de logiciels** sur la même verticale (73.2), qui
   monétise l'intention d'achat générée par les deux premiers.

Ces trois concepts partagent **la même audience et le même travail de veille**.
Ce n'est pas trois projets : c'est un projet avec trois sorties, donc trois
façons de gagner, pour un seul effort de recherche.

## POURQUOI

**1. Parce que l'IA a détruit la valeur du contenu générique, et cette étude en
tire la conséquence jusqu'au bout.**
N'importe qui peut produire 50 vidéos par jour. Le critère qui décide de tout en
2026 n'est donc plus « la niche est-elle porteuse ? » mais **« qu'est-ce qu'un
concurrent équipé des mêmes IA ne peut pas copier en une semaine ? »**. C'est le
critère `avantage_defendable`, l'un des trois plus lourds de la grille.

**2. Parce que les chiffres de monétisation ne laissent aucune ambiguïté.**
[DONNÉE] RPM YouTube France : **8-15 €** en finance, **5-12 €** en
business/entrepreneuriat, **5-10 €** en tech — contre **2-5 €** en gaming et
**0,50-2,50 $** sur les formats faceless saturés (musique, sommeil, histoires).
[DONNÉE] Un sponsoring de newsletter B2B en France se facture **150 à 800 €**
l'insertion, avec un CPM de **20 à 80 €**. Un même effort rapporte donc entre
10 et 100 fois plus selon l'audience choisie. **Le choix de l'audience pèse plus
lourd que la qualité de l'exécution.**

**3. Parce qu'il existe une fenêtre datée, rare et vérifiable.**
[DONNÉE] La facturation électronique est **obligatoire en France depuis le
1ᵉʳ septembre 2026** (réception, pour toutes les entreprises assujetties à la
TVA) et l'obligation d'émission frappe **PME, TPE et micro-entreprises au
1ᵉʳ septembre 2027**. Des millions d'entreprises doivent s'équiper dans les
douze mois. Une demande *contrainte par la loi* ne dépend ni d'une mode, ni d'un
algorithme.

**4. Parce que l'affiliation récurrente change la nature du revenu.**
[DONNÉE] Le programme francophone le mieux doté verse **60 % de commission
récurrente à vie** avec cookie illimité. Une seule vente rapporte tous les mois,
aussi longtemps que le client reste abonné. C'est la différence entre gagner de
l'argent et construire un revenu.

**5. Parce que le débutant a un avantage, et un seul : la vitesse de
validation.** Sans salariés, sans marque à protéger, sans investisseurs, on peut
tuer une idée en 30 jours. Toute la stratégie est construite pour exploiter ça
— d'où le critère `vitesse_validation`, et d'où le rejet des concepts dont on ne
sait qu'au bout de 6 mois s'ils marchent (B1, 9ᵉ, pénalisé pour cette seule
raison malgré ses qualités).

## DONNÉES

Les 6 chiffres qui pilotent la décision (détail et sources dans `01`) :

| Donnée | Valeur | Source |
|---|---|---|
| RPM YouTube France, finance / business / tech | 8-15 € / 5-12 € / 5-10 € | fluxnote, outilsy |
| RPM des niches faceless saturées (musique, sommeil, histoires) | 0,50-2,50 $ | shortsfast |
| Sponsoring newsletter B2B France | 150-800 € l'insertion, CPM 20-80 € | entreprisma, nenuphar-studio |
| Affiliation SaaS francophone la mieux dotée | **60 % récurrent à vie** | systeme.io |
| Facturation électronique : réception obligatoire | **01/09/2026** (émission TPE/PME : 01/09/2027) | Urssaf, economie.gouv.fr |
| Micro-SaaS B2B : prix d'entrée standard | 19-49 €/mois | saasmania, Knack |

**Lecture croisée, qui contredit l'intuition générale** : à 1 € de RPM, il faut
**un million de vues** pour gagner 1 000 €. À 300 € de sponsoring, il faut
**trois insertions** dans une newsletter lue par 1 500 professionnels. Le second
chemin est incomparablement plus court, et il ne dépend d'aucun algorithme.

## HYPOTHÈSES

Ce qui n'est **pas** démontré et doit être testé :

- **H1** — Une profession précise s'abonne à une veille hebdomadaire par email.
- **H2** — Cette audience professionnelle paie (produit ou abonnement).
- **H3** — Des annonceurs (éditeurs de logiciels) achètent une insertion dans
  une newsletter de 1 000 à 2 000 abonnés qualifiés.
- **H4** — Le contenu court en français sur un sujet B2B aride attire malgré
  tout une audience (ou bien l'acquisition doit passer par le SEO et LinkedIn).
- **H5** — L'affiliation logiciel convertit sur ce trafic (clic → essai → abonné).

Chacune a un test, un seuil chiffré et une date dans
[`03-plan-execution.md`](03-plan-execution.md).

## ACTIONS (les 7 prochaines, dans l'ordre)

1. **Choisir la profession cible** avant toute autre chose — c'est la seule
   décision de cette étude que je ne peux pas prendre à votre place, et elle
   détermine tout le reste. Méthode de choix en 3 questions : `03`, phase 0.
2. **Vérifier la demande en 48 h** : recherches existantes, groupes
   professionnels actifs, logiciels qui s'adressent déjà à cette profession
   (leur existence prouve qu'un budget existe).
3. **Ouvrir la newsletter** (beehiiv, gratuit jusqu'à 2 500 abonnés) et publier
   la page d'inscription **avant** d'avoir écrit un seul numéro.
4. **Publier 8 numéros en 8 semaines**, sans exception, même à 12 abonnés.
5. **Publier en parallèle 20 pages de comparatif/annuaire** sur la même
   verticale, avec liens d'affiliation et mention légale obligatoire.
6. **Tester 30 contenus courts** (H4) pour mesurer si l'acquisition sociale
   fonctionne sur un sujet B2B, ou s'il faut basculer sur SEO + LinkedIn.
7. **Activer le Niche Radar** (`04`) dès la première semaine, pour ne jamais
   dépendre de cette seule étude, datée du 21/09/2026.

## AUTOMATISATION

Automatisable dès maintenant : la collecte de la veille, la rédaction d'un
premier jet, la génération des pages de comparatif, la collecte des métriques,
l'exécution du Niche Radar. **Non automatisable, et c'est délibéré** : la
vérification des faits, la publication, et la décision d'arrêter un projet.
Détail dans [`07-automatisation-agents.md`](07-automatisation-agents.md).

## COÛT

**0 €/mois** pour toute la phase 1. Première dépense envisagée : un nom de
domaine (~10 €/an), et seulement une fois le trafic amorcé. Détail et seuils de
bascule dans [`09-outils-et-budget.md`](09-outils-et-budget.md).

## KPI

Aucun indicateur de vanité. Les seuls chiffres suivis : inscrits, taux
d'ouverture, **clics sortants**, conversions, revenu par contenu, coût, temps de
production. Schéma complet dans [`05-tableau-de-bord.md`](05-tableau-de-bord.md).

## PROCHAINE ÉTAPE

**La verticale est choisie : les e-commerçants français** (décision du
21/09/2026, sur le critère posé par le propriétaire — revenu maximal, marché
stable ou porteur). Les artisans du bâtiment ont été écartés parce que leur
marché est en recul (13 trimestres de baisse), ce qui ne passe pas ce critère.
La démonstration, les signaux négatifs et le plan de 30 jours sont dans
[`lancement/`](lancement/).

Il n'y a donc plus de décision bloquante. La prochaine action concrète est
l'ouverture du compte beehiiv et la mise en ligne de la page d'inscription,
avant tout contenu.

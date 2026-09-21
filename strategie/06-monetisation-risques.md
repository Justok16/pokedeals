# 06 — Monétisation et risques

## Les 8 sources de revenus, chiffrées

Ordre = ordre d'activation recommandé. Les montants sont des **[ESTIMATION]**
calculées à partir des données de [`01`](01-etude-marche.md), pas des promesses.

### 1. Affiliation
- **Taux réels** : Amazon jeux ~1-3 % ; eBay 1-4 % (3 % sur les cartes) ;
  Cardmarket inexploitable (plafond 10 €/mois).
- **[ESTIMATION]** panier 40 € × 3 % = 1,20 €/vente. À 3 % de conversion sur les
  clics sortants : **~28 000 clics pour 1 000 €/mois**.
- **Verdict** : revenu d'appoint, jamais un pilier. Utile surtout comme
  **preuve d'intention d'achat** (le clic vaut plus comme signal que comme euro).

### 2. Accords directs avec les boutiques TCG FR (**la piste la plus sous-estimée**)
- Les 83+ boutiques déjà scannées sont des commerçants qui achètent du trafic
  qualifié. Un acheteur envoyé au moment exact de sa recherche vaut plus pour
  eux qu'une publicité au CPM.
- Formes possibles : commission négociée, code promo tracké, mise en avant
  payante dans le comparateur, encart dans la newsletter.
- **[ESTIMATION]** 5 boutiques × 80 €/mois de mise en avant = **400 €/mois**
  récurrents, sans audience massive.
- **Risque** : c'est du B2B. Mais c'est du B2B **entrant et non prospecté** dès
  que le comparateur existe — conforme à la contrainte « pas de prospection
  manuelle intensive ».

### 3. Sponsoring de newsletter
- Activable vers ~1 000 abonnés qualifiés.
- **[ESTIMATION]** 150-400 €/envoi sur une audience acheteuse de niche.
- beehiiv fournit en plus un réseau publicitaire rémunéré à l'impression.

### 4. Publicité de plateforme
- TikTok Creator Rewards : **0,40-1,20 €/1000 vues** en France ; YPP YouTube
  soumis à la politique de contenu non authentique (2026).
- **[ESTIMATION]** 1 000 €/mois ≈ **830 000 à 2 500 000 vues qualifiées**.
- **Verdict** : à activer parce que c'est gratuit, jamais à viser comme objectif.

### 5. Produit numérique
- Guide/tableur à 19-29 €.
- **[ESTIMATION]** 1 000 abonnés × 2 % × 19 € = **380 €** une fois, puis décroît.
- **Rôle réel** : tester la solvabilité (H2), pas financer le projet.

### 6. Abonnement (premium newsletter / alertes anticipées)
- **[ESTIMATION]** 3 000 abonnés × 3 % × 5 €/mois = **450 €/mois récurrents**.
- Comparaison qui remet tout en perspective : **c'est l'équivalent de ~400 000
  vues TikTok par mois, pour un travail très inférieur.**

### 7. Micro-SaaS B2B (A3)
- **[DONNÉE]** un concurrent grand public facture 4,99-7,99 $/mois ; un pro paie
  plus.
- **[ESTIMATION]** 30 clients × 39 €/mois = **1 170 €/mois**, marge très élevée,
  mais support humain non automatisable.

### 8. B2B automatisé (mise en avant, données, marque blanche)
- Seulement en self-serve. Toute forme qui exige de la prospection manuelle
  intensive est exclue par le cahier des charges — et à raison : elle ne
  s'automatise pas et elle repose sur une compétence de vente absente.

## Ce que ces chiffres disent ensemble

| Source | Effort pour 1 000 €/mois | Récurrent ? | Automatisable ? |
|---|---|---|---|
| Publicité plateforme | ~1 M de vues/mois | Non | Partiellement |
| Affiliation | ~28 000 clics/mois | Non | Oui |
| Sponsoring | 3-6 envois/mois à ~1 000 abonnés | Semi | Partiellement |
| Abonnement | ~200 abonnés payants à 5 € | **Oui** | Oui |
| Micro-SaaS B2B | ~26 clients à 39 € | **Oui** | En partie (hors support) |

**[OPINION]** La conclusion est nette et elle contredit l'intuition de la plupart
des créateurs : **le chemin le plus court vers 1 000 €/mois passe par 200
personnes qui paient 5 €, pas par un million de vues.** Tout le plan est
construit là-dessus.

---

## Registre des risques

| # | Risque | Probabilité | Impact | Mesure de réduction |
|---|---|---|---|---|
| R1 | **Dépendance plateforme** (compte fermé, algorithme modifié) | Élevée | Élevé | Tout contenu pousse vers la newsletter ; l'actif de référence est la liste email + le site |
| R2 | **Démonétisation pour contenu non authentique** (YouTube 2026, évaluation **au niveau de la chaîne**) | Moyenne | Élevé | Contenu adossé à une donnée propriétaire, variation réelle des formats, jamais de volume sans valeur |
| R3 | **Droits d'auteur sur les visuels de cartes** (Nintendo/TPC) | Moyenne | Élevé | Photos propres, données chiffrées, visuels fournis par les boutiques ; ne jamais bâtir la valeur sur la rediffusion d'illustrations officielles |
| R4 | **Droits musicaux/images** en vidéo | Moyenne | Moyen | Bibliothèques libres de droits des plateformes uniquement |
| R5 | **Non-respect de la loi influence commerciale** (mention « Publicité » obligatoire ; jusqu'à 2 ans et 300 000 €) | Faible si procédure suivie | **Très élevé** | Mention automatique insérée par le générateur de contenu dès qu'un lien d'affiliation est présent — jamais à la main |
| R6 | **RGPD** (newsletter, SaaS) | Moyenne | Moyen | Consentement explicite, désinscription 1 clic, politique de confidentialité, minimisation |
| R7 | **Discours de promesse de gain** (« investir », « rendement ») | Moyenne | Élevé | Lexique interdit dans les modèles de contenu ; on publie des prix observés, pas des conseils de placement |
| R8 | **Blocage/refus des boutiques scannées** | Moyenne | Moyen | Scan respectueux (cadence, identification), retrait immédiat sur demande, relation commerciale plutôt qu'adversariale |
| R9 | **Cote erronée publiée** (bug, faible nombre d'annonces) | Moyenne | Élevé | Ne publier une cote que si `nb_annonces` dépasse un seuil ; afficher l'incertitude ; garde-fous déjà présents dans le moteur |
| R10 | **Retournement du marché des cartes** | Moyenne | Moyen | Monétisation qui fonctionne à la hausse comme à la baisse (comparaison de prix, information) ; diversification vers d'autres TCG (B1) |
| R11 | **Sur-dispersion** (trop de concepts en parallèle) | **Élevée** | Élevé | 3 concepts actifs maximum ; règle de KILL appliquée sans exception |
| R12 | **Fiscal/statut** (revenus non déclarés) | Faible | Élevé | Micro-entreprise dès le premier revenu régulier ; pseudonymat ≠ anonymat juridique |
| R13 | **Dépendance à un fournisseur d'IA** (prix, disponibilité) | Moyenne | Moyen | Aucune brique critique ne doit dépendre d'un seul fournisseur ; les workflows actuels tournent déjà sans IA |
| R14 | **Point de défaillance unique : une seule personne** | Élevée | Moyen | Tout documenté dans le dépôt, tout automatisé, rien qui repose sur un savoir non écrit |

**R2, R5 et R9 sont les trois risques qui peuvent détruire un actif en une
fois.** Ils justifient à eux seuls la validation humaine avant publication
décrite dans [`07`](07-automatisation-agents.md).

# 02 — Portefeuille de concepts

15 concepts, notés sur 16 critères pondérés, classés par un **score calculé,
pas choisi**. Le calcul est dans [`outils/`](outils/) et se rejoue par :

```bash
cd strategie/outils && python scorer.py          # classement
python scorer.py --detail A2                     # le détail d'un concept
```

Si vous n'êtes pas d'accord avec la hiérarchie, **changez les poids dans
`outils/criteres.yaml`** et relancez : c'est fait pour ça. Les poids actuels
privilégient volontairement le revenu récurrent, l'actif revendable, le levier
sur l'existant et l'automatisation.

## Classement (21/09/2026)

| # | ID | Concept | Score global /100 | Potentiel éco /100 | Faisabilité /100 |
|---|----|---------|------------------:|-------------------:|-----------------:|
| 1 | A2 | Newsletter « La Cote » (indice hebdo Pokémon FR) | **83.1** | 76.9 | 92.4 |
| 2 | D3 | Annuaire/comparateur des boutiques TCG FR | **81.5** | 83.1 | 90.5 |
| 3 | B1 | Extension du moteur à One Piece / Lorcana / Magic FR | **79.7** | 73.8 | 96.2 |
| 4 | A4 | PokéPrécoms (radar de précommandes générique) | **78.8** | 69.2 | 92.4 |
| 5 | A3 | API/Cote PokéDeals Pro (micro-SaaS B2B self-serve) | **76.6** | 75.4 | 81.9 |
| 6 | A5 | Site SEO « cote-pokemon » (pages carte/set générées) | **76.3** | 76.9 | 82.9 |
| 7 | A1 | PokéDeals Média FR | **70.2** | 63.1 | 80.0 |
| 8 | D2 | Micro-SaaS vendeurs TCG (fiches d'annonces automatiques) | **70.2** | 72.3 | 65.7 |
| 9 | C1 | Média FR « Outils IA pour indépendants » | **68.9** | **89.2** | **44.8** |
| 10 | B3 | Deal Radar as a Service (marque blanche) | **65.2** | 66.2 | 61.9 |
| 11 | B2 | Deal radar hors TCG (rétrogaming, LEGO, sneakers) | **64.0** | 67.7 | 62.9 |
| 12 | D1 | Produit numérique « Investir dans les cartes Pokémon » | **62.5** | 52.3 | 76.2 |
| 13 | C2 | Média FR finance perso / pouvoir d'achat | **59.4** | **81.5** | **36.2** |
| 14 | C4 | YouTube long format documentaire collection/gaming | **55.7** | 63.1 | 45.7 |
| 15 | C3 | Média FR droits, aides et démarches | **47.7** | 46.2 | 43.8 |

**Ce que ce tableau dit et qu'une liste d'idées ne dirait pas** : les concepts
les plus *rentables en théorie* (C1 à 89/100 de potentiel économique, C2 à 81)
sont ceux que ce profil a le moins de chances de gagner (faisabilité 45 et 36).
Les concepts gagnants ne sont pas les plus séduisants — ce sont ceux où un
avantage réel existe déjà.

**Incertitude assumée** : je ne sais pas lequel deviendra le plus rentable.
Le classement ordonne des **hypothèses**, pas des résultats. Il sera faux en
partie — le rôle des tests de [`03`](03-plan-execution.md) est de dire où.

---

## Lot de test recommandé (ne pas tout lancer)

| Lot | Concepts | Pourquoi ceux-là |
|---|---|---|
| **Lot 1 — maintenant** | **A2**, **D3**, **A1** | Un actif possédé (email), un actif de trafic (comparateur), un canal d'acquisition (court). Trois natures différentes, donc trois apprentissages différents. |
| **Lot 1 bis — tâche de fond** | **B1** | Coût marginal quasi nul (changer une watchlist), donne une 2ᵉ audience sans 2ᵉ travail. |
| **Lot 2 — après validation de H2** | **A3**, **A5**, **A4** | Ne se justifient que si l'audience et la valeur de la donnée sont démontrées. |
| **Jamais sans signal fort** | **C2**, **C3**, **C4** | Risque juridique, monétisation faible ou production trop lourde. |

Trois concepts actifs simultanément : assez pour apprendre, pas assez pour
diluer 4 h/jour. Ouvrir 15 comptes serait une erreur de débutant coûteuse en
attention.

---

## Fiches détaillées

Chaque fiche suit les 18 points demandés.

### A2 — Newsletter « La Cote » · score 83.1 · **rang 1**

1. **Concept** — Newsletter hebdomadaire générée automatiquement depuis la base
   de cotes : top hausses/baisses de la semaine, meilleures affaires repérées,
   précommandes ouvertes, boutique la moins chère du moment.
2. **Audience** — Collectionneurs/revendeurs FR de 18 à 45 ans qui suivent les
   prix, déjà acheteurs.
3. **Pourquoi maintenant** — Le seul actif que l'IA ne dévalue pas est une liste
   d'emails adossée à une donnée exclusive. Les outils équivalents (Collectr…)
   sont anglophones et ignorent le marché FR.
4. **Tendances observées** — [DONNÉE] marché FR +12 %/an ; [DONNÉE] beehiiv
   gratuit jusqu'à 2 500 abonnés, 0 % de commission sur l'abonnement.
5. **Potentiel d'audience** — [ESTIMATION] 2 000 à 10 000 abonnés atteignables
   en 12-18 mois sur une niche FR active ; plafond réaliste bien inférieur aux
   4 M de collectionneurs.
6. **Potentiel économique** — 76.9/100. [ESTIMATION] à 3 000 abonnés :
   sponsoring boutique 150-400 €/envoi, affiliation 100-300 €/mois, offre
   premium 5 €/mois × 3 % des abonnés ≈ 450 €/mois.
7. **Affiliation** — Boutiques TCG FR (accords directs), eBay Partner Network,
   Amazon (faible). Cardmarket exclu (plafond 10 €/mois).
8. **Produit potentiel** — Édition premium (cotes complètes, alertes anticipées,
   export CSV).
9. **SaaS potentiel** — Oui, c'est le tunnel naturel vers A3 et vers le SaaS
   existant.
10. **Difficulté** — Faible : la donnée existe, le formatage est du code.
11. **Coût initial** — 0 €.
12. **Automatisation possible** — Très élevée : génération complète par cron,
    relecture humaine 10 min avant envoi.
13. **Risques** — Faible volume d'inscriptions au départ ; dépendance à la
    qualité de la cote ; RGPD ; lassitude si le contenu n'apporte rien de neuf.
14. **Contenu possible** — Indice hebdo, « la carte de la semaine », écart de
    prix entre boutiques, calendrier des sorties.
15. **Plateformes** — beehiiv (hébergement + page d'inscription), relais
    Telegram/TikTok/SaaS pour l'acquisition.
16. **Hypothèse à tester** — **H1** : ≥ 300 inscrits en 60 jours sans
    publicité, et ≥ 35 % de taux d'ouverture moyen sur 4 numéros.
17. **Ce qui pourrait faire échouer l'idée** — Les collectionneurs vivent sur
    Telegram/Discord et n'ouvrent pas d'emails ; ou la cote n'est pas assez
    fiable pour être publiée nominativement.
18. **Métriques à surveiller** — Inscrits/semaine, taux d'ouverture, taux de
    clic, clics sortants par numéro, désinscriptions, revenu par envoi.

---

### D3 — Annuaire/comparateur des boutiques TCG FR · score 81.5 · **rang 2**

1. **Concept** — Comparateur public : pour une carte ou un produit scellé, le
   prix chez les 83+ boutiques FR/JP déjà scannées, avec disponibilité.
2. **Audience** — Acheteur en intention immédiate (le moment où la valeur
   commerciale est maximale).
3. **Pourquoi maintenant** — La base de boutiques et le scan existent déjà et
   tournent toutes les 30 minutes. Le produit est à 90 % construit sans le savoir.
4. **Tendances observées** — [DONNÉE] aucun comparateur FR multi-boutiques TCG
   identifié ; les acteurs existants sont US/EN et orientés collection.
5. **Potentiel d'audience** — [ESTIMATION] trafic SEO longue traîne :
   « prix carte X », « où acheter ETB Y ». Fort mais lent (6-12 mois).
6. **Potentiel économique** — 83.1/100, le meilleur du portefeuille parmi les
   concepts faisables.
7. **Affiliation** — Cœur du modèle : commission ou mise en avant payante
   négociée directement avec les boutiques (**H3**).
8. **Produit potentiel** — Alerte de baisse de prix (freemium).
9. **SaaS potentiel** — Oui : côté boutique (tableau de bord de positionnement
   prix face aux concurrents) — c'est A3 sous un autre angle.
10. **Difficulté** — Moyenne : le scan existe, la mise en page/SEO est neuve.
11. **Coût initial** — 0 € (pages statiques générées + hébergement gratuit) ;
    un nom de domaine (~10 €/an) devient utile une fois le trafic amorcé.
12. **Automatisation possible** — Totale (regénération par cron).
13. **Risques** — Refus/opposition de boutiques ; conditions d'utilisation des
    sites scannés ; dépendance SEO à Google et aux réponses IA.
14. **Contenu possible** — Fiches produit, pages « meilleures offres du jour »,
    classement des boutiques par prix moyen.
15. **Plateformes** — Site (GitHub Pages ou équivalent gratuit), SEO, relais
    newsletter.
16. **Hypothèse à tester** — **H3** : au moins **3 boutiques sur 20 contactées**
    acceptent un accord (affiliation, code promo ou mise en avant).
17. **Ce qui pourrait faire échouer l'idée** — Les boutiques FR ne font pas
    d'affiliation et refusent la comparaison de prix ; ou le SEO ne décolle pas
    faute d'autorité de domaine.
18. **Métriques à surveiller** — Pages indexées, impressions/clics Search
    Console, clics sortants par boutique, accords signés, revenu par boutique.

---

### B1 — Extension du moteur à un 2ᵉ TCG · score 79.7 · **rang 3** (meilleure faisabilité : 96.2)

1. **Concept** — Réutiliser le moteur existant (connecteurs, cote, alertes) sur
   Lorcana, One Piece ou Magic en français.
2. **Audience** — Collectionneurs FR de ces jeux, moins bien outillés que ceux
   de Pokémon.
3. **Pourquoi maintenant** — Le coût marginal est une watchlist. Aucun autre
   concept du portefeuille n'a ce rapport effort/portée.
4. **Tendances observées** — [DONNÉE] Pokémon = 61 % du marché FR : les 39 %
   restants sont un marché réel et bien moins couvert par des outils.
5. **Potentiel d'audience** — [ESTIMATION] 20 à 40 % de l'audience Pokémon FR.
6. **Potentiel économique** — 73.8/100 ; surtout un **multiplicateur** des
   concepts A2/D3 plutôt qu'un revenu autonome.
7. **Affiliation** — Identique à Pokémon (mêmes boutiques).
8. **Produit potentiel** — Édition newsletter dédiée par jeu.
9. **SaaS potentiel** — Mutualisé avec A3.
10. **Difficulté** — Très faible (configuration).
11. **Coût initial** — 0 €.
12. **Automatisation possible** — Totale, infrastructure identique.
13. **Risques** — IP plus jeunes, donc demande moins prouvée dans la durée ;
    dilution de la marque si tout est mélangé.
14. **Contenu possible** — Mêmes formats, autre public.
15. **Plateformes** — Identiques.
16. **Hypothèse à tester** — À volume de contenu égal, l'audience acquise par
    carte publiée est-elle ≥ 50 % de celle de Pokémon ?
17. **Ce qui pourrait faire échouer l'idée** — Fonds de catalogue trop petit, ou
    cotes trop peu liquides pour être fiables (peu d'annonces par carte).
18. **Métriques à surveiller** — Nombre de cartes avec cote fiable (`nb_annonces`),
    alertes émises, engagement comparé à Pokémon.

---

### A4 — PokéPrécoms (radar de précommandes) · score 78.8 · **rang 4**

1. **Concept** — Détecter et annoncer en premier l'ouverture des précommandes de
   produits scellés, toutes boutiques confondues.
2. **Audience** — Acheteurs pressés, revendeurs ; intention d'achat maximale.
3. **Pourquoi maintenant** — Le radar générique est **déjà écrit** dans ce dépôt
   et un dépôt dédié est déjà prévu.
4. **Tendances observées** — [DONNÉE] produits scellés en tension, ruptures
   fréquentes ; [HYPOTHÈSE] l'urgence crée le meilleur taux de clic sortant.
5. **Potentiel d'audience** — Plus étroite que A2 mais plus réactive.
6. **Potentiel économique** — 69.2/100, mais **le meilleur taux de conversion
   attendu** de tout le portefeuille (panier 50-200 €).
7. **Affiliation** — Le cas d'usage idéal : le lien arrive à la seconde où
   l'achat est décidé.
8. **Produit potentiel** — Accès anticipé payant aux alertes (2-5 min d'avance).
9. **SaaS potentiel** — Oui, adossé au SaaS existant.
10. **Difficulté** — Faible (code existant).
11. **Coût initial** — 0 €.
12. **Automatisation possible** — Totale.
13. **Risques** — Fausse alerte = perte de confiance immédiate ; boutiques qui
    bloquent le scan ; accusations de favoriser les revendeurs.
14. **Contenu possible** — Alertes, calendrier des sorties, historique des
    ruptures.
15. **Plateformes** — Telegram, email, X, site.
16. **Hypothèse à tester** — ≥ 10 % de clics sortants par alerte envoyée.
17. **Ce qui pourrait faire échouer l'idée** — Concurrence des groupes Discord
    de revendeurs, plus rapides et communautaires.
18. **Métriques à surveiller** — Délai de détection vs. concurrents, clics par
    alerte, taux de faux positifs.

---

### A3 — API/Cote PokéDeals Pro · score 76.6 · **rang 5**

1. **Concept** — Accès payant à la cote FR calculée et à son historique (API +
   export), pour vendeurs pros, boutiques et gros revendeurs. Self-serve.
2. **Audience** — B2B étroit : quelques centaines d'acteurs FR.
3. **Pourquoi maintenant** — La donnée est déjà produite quotidiennement ; le
   coût marginal de la vendre est proche de zéro.
4. **Tendances observées** — [DONNÉE] des particuliers paient déjà 4,99-7,99 $/
   mois pour de l'historique de prix (Collectr) : un pro paie davantage.
5. **Potentiel d'audience** — Faible en volume, élevé en valeur unitaire.
6. **Potentiel économique** — 75.4/100. [ESTIMATION] 30 clients × 39 €/mois ≈
   1 170 €/mois récurrents, sans production de contenu.
7. **Affiliation** — Sans objet.
8. **Produit potentiel** — Rapport mensuel de marché FR vendu à l'unité.
9. **SaaS potentiel** — C'est le SaaS.
10. **Difficulté** — Moyenne : facturation, quotas, support client.
11. **Coût initial** — 0 € jusqu'aux premiers encaissements (puis commissions
    Stripe et statut micro-entreprise).
12. **Automatisation possible** — Élevée, sauf le support.
13. **Risques** — Revente de données agrégées à cadrer juridiquement (sources,
    CGU des sites scannés) ; dépendance à un petit nombre de clients ; support
    = travail humain non automatisable.
14. **Contenu possible** — Documentation, études de marché publiques comme
    produit d'appel.
15. **Plateformes** — Site + Stripe.
16. **Hypothèse à tester** — **H5** : ≥ 3 acteurs pros acceptent un pilote
    payant (même à 19 €/mois) après démonstration.
17. **Ce qui pourrait faire échouer l'idée** — Les pros se fient à Cardmarket et
    n'ont pas besoin d'une cote FR ; ou ils veulent un outil complet, pas une API.
18. **Métriques à surveiller** — Essais → payants, rétention à 3 mois, revenu
    moyen par client, tickets de support par client (indicateur d'automatisation).

---
### A5 — Site SEO « cote-pokemon » · score 76.3 · **rang 6**

1. **Concept** — Milliers de pages longue traîne générées depuis la base
   (« prix carte X 123/456 »), avec historique et liens boutiques.
2. **Audience** — Trafic de recherche : quelqu'un qui tape le nom d'une carte.
3. **Pourquoi maintenant** — La base existe ; générer des pages est du code.
4. **Tendances observées** — [DONNÉE] le SEO subit la pression des réponses
   générées par IA ; [OPINION] les pages à **donnée chiffrée fraîche** résistent
   mieux que les pages d'avis rédigées.
5. **Potentiel d'audience** — Élevé mais différé (6-12 mois d'indexation).
6. **Potentiel économique** — 76.9/100 ; s'additionne à D3 plutôt qu'il ne le
   concurrence (même socle, deux intentions de recherche).
7. **Affiliation** — Forte (intention d'achat sur la page).
8. **Produit potentiel** — Alertes prix par carte.
9. **SaaS potentiel** — Bascule vers le SaaS existant.
10. **Difficulté** — Faible techniquement, élevée en SEO (autorité à construire).
11. **Coût initial** — 0 € + nom de domaine ~10 €/an.
12. **Automatisation possible** — Totale.
13. **Risques** — **Risque majeur** : des milliers de pages quasi identiques
    peuvent être vues comme du contenu de faible valeur et déclasser tout le
    site. Règle : ne générer une page que si elle contient une donnée réelle et
    différenciante (cote, historique, offres) — jamais du texte de remplissage.
14. **Contenu possible** — Fiches carte, pages set, classements.
15. **Plateformes** — Site statique, Search Console.
16. **Hypothèse à tester** — ≥ 1 000 impressions/jour en Search Console à 90
    jours sur 500 pages publiées.
17. **Ce qui pourrait faire échouer l'idée** — Pénalité de qualité, ou SERP
    occupée par les gros acteurs du secteur.
18. **Métriques à surveiller** — Pages indexées/publiées, impressions, position
    moyenne, clics sortants, revenu par 1 000 visites.

---

### A1 — PokéDeals Média FR · score 70.2 · **rang 7**

1. **Concept** — Compte faceless (TikTok + Shorts) alimenté par les données du
   scraper : l'affaire du jour, l'écart entre boutiques, la carte qui monte.
2. **Audience** — 18-34 ans (57 % du marché TCG sous licence), très présents en
   format court.
3. **Pourquoi maintenant** — C'est le canal d'acquisition le moins cher pour
   remplir A2 et D3. Et un contenu **basé sur une donnée exclusive** est
   défendable face à la politique YouTube 2026.
4. **Tendances observées** — [DONNÉE] RPM FR 0,40-1,20 € ; [DONNÉE] YouTube
   sanctionne désormais au niveau de la chaîne le contenu répétitif/IA générique.
5. **Potentiel d'audience** — Le plus élevé du portefeuille en volume brut.
6. **Potentiel économique** — 63.1/100, **le plus faible des concepts
   faisables** : c'est de l'acquisition, pas du revenu.
7. **Affiliation** — Indirecte (lien en bio → comparateur/newsletter).
8. **Produit potentiel** — Aucun en direct.
9. **SaaS potentiel** — Via redirection.
10. **Difficulté** — Moyenne (production + rythme).
11. **Coût initial** — 0 €.
12. **Automatisation possible** — Élevée pour le script et les données,
    **semi-automatique pour la publication** (une relecture humaine avant mise
    en ligne, cf. `07`).
13. **Risques** — Dépendance plateforme, démonétisation, droits sur les visuels
    de cartes, lassitude du format.
14. **Contenu possible** — « Cette carte a pris +40 % en 3 semaines », « 32 €
    ici, 58 € ailleurs », « précommande ouverte depuis 4 minutes ».
15. **Plateformes** — TikTok et YouTube Shorts d'abord ; Instagram en recyclage.
16. **Hypothèse à tester** — **H4** : ≥ 3 vidéos sur 30 dépassant 10 000 vues,
    et ≥ 100 inscrits newsletter venus du canal, en 30 jours.
17. **Ce qui pourrait faire échouer l'idée** — Format trop informatif pour
    l'algorithme de divertissement ; ou audience non transférable hors plateforme.
18. **Métriques à surveiller** — Vues, rétention à 3 s, clics en bio,
    **inscrits newsletter attribués**, coût en temps par vidéo.

---

### D2 — Micro-SaaS vendeurs TCG · score 70.2 · **rang 8**

1. **Concept** — Photo d'une carte → annonce complète (titre normalisé, état,
   prix conseillé depuis la cote) pour Vinted/eBay.
2. **Audience** — Particuliers et semi-pros qui vendent en volume.
3. **Pourquoi maintenant** — Le problème est réel et chronophage ; la cote et la
   normalisation des noms sont déjà résolues dans le moteur existant.
4. **Tendances observées** — [HYPOTHÈSE] pas de donnée de demande collectée ; à
   valider avant toute ligne de code.
5. **Potentiel d'audience** — Moyenne, mais fortement solvable au temps gagné.
6. **Potentiel économique** — 72.3/100, revenu récurrent noté 5/5.
7. **Affiliation** — Sans objet.
8. **Produit potentiel** — C'est le produit.
9. **SaaS potentiel** — Oui, par nature.
10. **Difficulté** — **Élevée** : la reconnaissance visuelle fiable est un vrai
    travail produit, pas un prompt.
11. **Coût initial** — Non nul (coût d'inférence à l'usage) → contrevient à la
    contrainte 0 €.
12. **Automatisation possible** — Moyenne (le support et la qualité restent
    humains).
13. **Risques** — Qualité insuffisante = produit inutilisable ; coût variable
    non maîtrisé ; CGU des plateformes de vente.
14. **Contenu possible** — Démonstrations vidéo (excellent contenu viral).
15. **Plateformes** — Web + mobile.
16. **Hypothèse à tester** — **Avant de coder** : 20 vendeurs interrogés, ≥ 8
    déclarent perdre > 1 h/semaine sur la rédaction d'annonces.
17. **Ce qui pourrait faire échouer l'idée** — Les outils natifs des plateformes
    suffisent déjà ; ou les vendeurs ne paient pas pour gagner 20 minutes.
18. **Métriques à surveiller** — Inscriptions, annonces générées/utilisateur,
    taux d'usage à J+7, coût d'inférence par utilisateur.

---

### C1 — Média FR « Outils IA pour indépendants » · score 68.9 · **rang 9**

1. **Concept** — Contenu court + newsletter sur les outils IA pour TPE et
   indépendants, monétisé par affiliation SaaS.
2. **Audience** — Indépendants, TPE, curieux de l'IA. Grande et solvable.
3. **Pourquoi maintenant** — [DONNÉE] marché IA ~+29 %/an ; affiliation SaaS
   souvent récurrente (20-30 %).
4. **Tendances observées** — Croissance forte **mais** saturation éditoriale
   massive, y compris en français.
5. **Potentiel d'audience** — Le plus élevé du portefeuille (5/5).
6. **Potentiel économique** — **89.2/100 — le meilleur score économique de tout
   le portefeuille.**
7. **Affiliation** — Excellente (récurrente).
8. **Produit potentiel** — Formations, modèles, annuaire.
9. **SaaS potentiel** — Oui, mais sans avantage particulier.
10. **Difficulté** — Élevée : fact-checking permanent, obsolescence en semaines.
11. **Coût initial** — 0 €.
12. **Automatisation possible** — **Moyenne, et c'est le piège** : publier des
    informations fausses sur des outils payants détruit la crédibilité et
    expose juridiquement.
13. **Risques** — Concurrence, durabilité faible (2/5), aucun levier sur
    l'existant (1/5).
14. **Contenu possible** — Comparatifs, tutoriels, veille.
15. **Plateformes** — YouTube, LinkedIn, newsletter.
16. **Hypothèse à tester** — Ne pas tester maintenant. **[OPINION] Décision :
    écarté du lot 1** — meilleur potentiel théorique, mais aucune raison
    objective de gagner contre des concurrents installés, et une pire faisabilité
    (44.8/100). À reconsidérer seulement si les tests A2/D3/A1 échouent tous.
17. **Ce qui pourrait faire échouer l'idée** — Absence d'angle différenciant.
18. **Métriques à surveiller** — Sans objet tant que non lancé.

---

### B3 — Deal Radar as a Service (marque blanche) · score 65.2 · **rang 10**

1. **Concept** — Vendre le moteur de veille de prix configurable à d'autres
   niches de collection, en self-serve.
2. **Audience** — Éditeurs de sites de niche, communautés, revendeurs.
3. **Pourquoi maintenant** — Aucune urgence. Suppose un moteur industrialisé,
   documenté et générique.
4. **Tendances observées** — Aucune donnée de demande. [HYPOTHÈSE] pure.
5. **Potentiel d'audience** — Faible (2/5).
6. **Potentiel économique** — 66.2/100, récurrent noté 5/5.
7. **Affiliation** — Sans objet.
8. **Produit potentiel** — Le produit lui-même.
9. **SaaS potentiel** — Oui.
10. **Difficulté** — Élevée : généraliser un moteur est plus coûteux que
    l'écrire pour un cas.
11. **Coût initial** — Non nul (infrastructure d'exécution pour des tiers).
12. **Automatisation possible** — Moyenne.
13. **Risques** — Support B2B lourd ; responsabilité en cas de scan fautif chez
    un client ; contrevient à la règle « pas de produit sans problème validé ».
14. **Contenu possible** — Études de cas.
15. **Plateformes** — Web.
16. **Hypothèse à tester** — Reporté. À ne rouvrir que si ≥ 5 demandes entrantes
    spontanées arrivent.
17. **Ce qui pourrait faire échouer l'idée** — Chaque niche a ses connecteurs :
    la promesse « configurable » est probablement fausse techniquement.
18. **Métriques à surveiller** — Demandes entrantes (seul signal à observer
    pour l'instant).

---
### B2 — Deal radar hors TCG · score 64.0 · **rang 11**

1. **Concept** — Appliquer le moteur d'écart prix/cote au rétrogaming, aux LEGO
   retirés, aux sneakers.
2. **Audience** — Large, mais déjà servie par des acteurs installés.
3. **Pourquoi maintenant** — Aucun déclencheur particulier.
4. **Tendances observées** — Marché des bons plans FR très occupé (Dealabs et
   assimilés), avec effet de communauté difficile à concurrencer.
5. **Potentiel d'audience** — Élevé (4/5).
6. **Potentiel économique** — 67.7/100.
7. **Affiliation** — Bonne.
8. **Produit potentiel** — Faible.
9. **SaaS potentiel** — Faible.
10. **Difficulté** — La « cote » est bien plus dure à calculer hors TCG
    (références non normalisées, états hétérogènes).
11. **Coût initial** — 0 €.
12. **Automatisation possible** — Bonne.
13. **Risques** — Concurrence frontale ; dilution de l'attention.
14. **Contenu possible** — Alertes bons plans.
15. **Plateformes** — Telegram, site.
16. **Hypothèse à tester** — Reporté (lot 3 au plus tôt).
17. **Ce qui pourrait faire échouer l'idée** — Impossible d'établir une cote
    fiable sans normalisation des références.
18. **Métriques à surveiller** — Sans objet tant que non lancé.

---

### D1 — Produit numérique « Investir dans les cartes Pokémon » · score 62.5 · **rang 12**

1. **Concept** — Guide + tableur de suivi vendu une fois (15-29 €).
2. **Audience** — Collectionneurs qui veulent acheter mieux.
3. **Pourquoi maintenant** — Sert surtout de **test de solvabilité** rapide
   (H2), pas de pilier.
4. **Tendances observées** — [DONNÉE] des outils payants existent déjà sur le
   suivi de collection.
5. **Potentiel d'audience** — Moyen.
6. **Potentiel économique** — 52.3/100 — **le plus faible des concepts du
   cluster A/D** parce que le revenu est non récurrent (1/5).
7. **Affiliation** — Faible.
8. **Produit potentiel** — C'est le produit.
9. **SaaS potentiel** — Non.
10. **Difficulté** — Faible.
11. **Coût initial** — 0 €.
12. **Automatisation possible** — Bonne (vente et livraison automatiques).
13. **Risques** — **Risque de discours** : le mot « investir » fait entrer dans
    la zone de la promesse de gain. Reformuler en « acheter et revendre sans se
    tromper », sans projection de rendement.
14. **Contenu possible** — Extraits offerts comme aimant à inscriptions.
15. **Plateformes** — Newsletter, Kit/Gumroad.
16. **Hypothèse à tester** — Après 300 abonnés newsletter : ≥ 2 % d'achat sur
    une offre à 19 €.
17. **Ce qui pourrait faire échouer l'idée** — Information disponible
    gratuitement partout ; faible valeur perçue.
18. **Métriques à surveiller** — Taux de conversion, remboursements, revenu par
    abonné.

---

### C2 — Média FR finance perso / pouvoir d'achat · score 59.4 · **rang 13**

1. **Concept** — Média court sur l'argent du quotidien.
2. **Audience** — Très large, CPM parmi les plus élevés du marché FR.
3. **Pourquoi maintenant** — Aucune raison propre à ce profil.
4. **Tendances observées** — Demande durable, concurrence extrême.
5. **Potentiel d'audience** — 5/5.
6. **Potentiel économique** — **81.5/100** — très élevé.
7. **Affiliation** — Bonne (banques, courtiers).
8. **Produit potentiel** — Oui.
9. **SaaS potentiel** — Faible.
10. **Difficulté** — Élevée.
11. **Coût initial** — 0 €.
12. **Automatisation possible** — **Faible (2/5)** : chaque affirmation engage.
13. **Risques** — **Risque juridique noté 1/5** : conseil en investissement,
    démarchage, responsabilité. C'est le concept le plus dangereux du
    portefeuille pour un débutant sous pseudonyme.
14. **Contenu possible** — Sans objet.
15. **Plateformes** — Sans objet.
16. **Hypothèse à tester** — **[OPINION] Écarté.** Le potentiel économique ne
    compense pas le couple risque juridique / faisabilité (36.2/100).
17. **Ce qui pourrait faire échouer l'idée** — Une seule erreur de conseil.
18. **Métriques à surveiller** — Sans objet.

---

### C4 — YouTube long format documentaire · score 55.7 · **rang 14**

1. **Concept** — Vidéos longues documentaires sur la collection/le gaming.
2. **Audience** — Fidèle, forte valeur de marque, sponsoring possible.
3. **Pourquoi maintenant** — Pas maintenant : production trop lourde pour 4 h/jour
   avec trois autres concepts en test.
4. **Tendances observées** — [DONNÉE] YouTube valorise désormais explicitement
   l'originalité et sanctionne le volume sans variation.
5. **Potentiel d'audience** — 4/5.
6. **Potentiel économique** — 63.1/100.
7. **Affiliation** — Moyenne.
8. **Produit potentiel** — Moyen.
9. **SaaS potentiel** — Non.
10. **Difficulté** — **La plus élevée du portefeuille (1/5 en facilité)**.
11. **Coût initial** — Faible en argent, très élevé en temps.
12. **Automatisation possible** — Faible.
13. **Risques** — Droits sur archives, images et musique ; dépendance
    plateforme (2/5).
14. **Contenu possible** — Enquêtes sur le marché, histoires de cartes rares.
15. **Plateformes** — YouTube.
16. **Hypothèse à tester** — Reporté à la phase « SCALE » d'un concept gagnant :
    le format long est un **amplificateur de marque**, pas un point de départ.
17. **Ce qui pourrait faire échouer l'idée** — Une vidéo tous les 15 jours ne
    construit pas d'audience assez vite pour justifier le coût.
18. **Métriques à surveiller** — Sans objet tant que non lancé.

---

### C3 — Média FR droits, aides et démarches · score 47.7 · **rang 15**

1. **Concept** — Vulgarisation des aides, droits et démarches administratives.
2. **Audience** — Immense.
3. **Pourquoi maintenant** — Ne pas le faire. Présent dans l'étude pour montrer
   **pourquoi une grosse audience ne fait pas un bon business**.
4. **Tendances observées** — Demande stable et forte.
5. **Potentiel d'audience** — 5/5.
6. **Potentiel économique** — **46.2/100 — le plus faible du portefeuille.**
7. **Affiliation** — Quasi inexistante (1/5).
8. **Produit potentiel** — Faible.
9. **SaaS potentiel** — Faible.
10. **Difficulté** — Moyenne.
11. **Coût initial** — 0 €.
12. **Automatisation possible** — Faible : une information périmée ou fausse sur
    des droits sociaux cause un préjudice réel.
13. **Risques** — Réputationnels et juridiques.
14. **Contenu possible** — Sans objet.
15. **Plateformes** — Sans objet.
16. **Hypothèse à tester** — **Écarté.**
17. **Ce qui pourrait faire échouer l'idée** — Une audience pauvre en intention
    d'achat ne se monétise pas, quel que soit son volume.
18. **Métriques à surveiller** — Sans objet.

---

## Ce que ce portefeuille démontre

1. **Audience ≠ argent.** C3 a l'audience potentielle maximale et le pire
   potentiel économique. A3 a l'audience la plus étroite et l'un des meilleurs.
2. **Le meilleur marché n'est pas le meilleur marché *pour vous*.** C1 gagne sur
   l'économie (89/100) et perd sur la faisabilité (45/100).
3. **Le levier sur l'existant décide presque tout.** Les 8 premiers du classement
   réutilisent le moteur, la donnée ou l'infrastructure déjà en production.
4. **Le classement est révisable par construction** : changez les poids, il
   change. Ce qui n'est pas négociable, c'est de le confronter aux tests.

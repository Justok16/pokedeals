# 02 — Portefeuille de concepts

15 concepts, notés sur 18 critères pondérés, classés par un **score calculé,
pas choisi**. Le calcul est dans [`outils/`](outils/) et se rejoue par :

```bash
cd ai-business-lab/outils && python scorer.py   # classement
python scorer.py --detail A4                    # le détail d'un concept
```

Si vous n'êtes pas d'accord avec la hiérarchie, **changez les poids dans
`outils/criteres.yaml`** et relancez : c'est fait pour ça. Les poids actuels
privilégient le revenu récurrent, **l'avantage défendable** et la **vitesse de
validation** — les trois choses qui manquent le plus à un débutant en 2026.

## Classement (21/09/2026)

| # | ID | Concept | Score global /100 | Potentiel éco /100 | Faisabilité /100 |
|---|----|---------|------------------:|-------------------:|-----------------:|
| 1 | A4 | Newsletter de veille pour une profession | **81.4** | 83.8 | 87.6 |
| 2 | A2 | IA appliquée à UN métier précis | **78.9** | 87.5 | 70.5 |
| 3 | A1 | Facture électronique 2026-2027 (média + annuaire + affiliation) | **78.3** | **90.0** | 70.5 |
| 4 | A3 | Micro-entreprise / création d'entreprise en France | **75.5** | 88.8 | 61.9 |
| 5 | B2 | Annuaire/comparateur de logiciels d'une niche | **73.2** | 80.0 | 62.9 |
| 6 | B3 | Outils gratuits en ligne (calculateurs) → freemium | **72.1** | 77.5 | 63.8 |
| 7 | E1 | Micro-SaaS no-code B2B (19-49 €/mois) | **71.5** | 76.2 | 60.0 |
| 8 | E2 | Automatisations prêtes à l'emploi en self-serve | **68.7** | 66.2 | 76.2 |
| 9 | B1 | Site programmatique sur données publiques ouvertes | **67.3** | 67.5 | 67.6 |
| 10 | D1 | Chaîne faceless éducation IA/tech en français | **67.0** | 71.2 | 66.7 |
| 11 | C1 | Produits numériques pour une profession | **65.1** | 53.8 | 81.0 |
| 12 | C2 | Mini-formation sur une obligation réglementaire | **63.4** | 67.5 | 67.6 |
| 13 | D2 | Chaîne faceless finance / business en français | **61.4** | 72.5 | 54.3 |
| 14 | C3 | Print on demand faceless | **48.5** | 36.2 | 68.6 |
| 15 | D3 | Chaîne faceless divertissement (histoires, motivation, musique) | **45.9** | **30.0** | 76.2 |

**Ce que ce tableau dit, et qu'une liste d'idées ne dirait pas :**

1. **Les 8 premiers concepts visent tous une audience professionnelle.** Ce
   n'est pas une préférence esthétique : c'est la conséquence arithmétique des
   RPM, des tarifs de sponsoring et des taux d'affiliation mesurés dans `01`.
2. **Le concept le plus populaire chez les débutants arrive dernier** (D3, 45.9,
   avec un potentiel économique de 30/100). Il est facile, gratuit, rapide — et
   c'est précisément pour ça qu'il ne vaut rien : ce qui est accessible à tous
   n'a aucune valeur défendable.
3. **Le meilleur potentiel économique (A1, 90/100) n'est pas premier**, parce
   que sa demande est datée et que le sujet engage juridiquement. Un score
   global existe justement pour empêcher de ne regarder que l'argent.

**Incertitude assumée** : je ne sais pas lequel deviendra le plus rentable. Le
classement ordonne des **hypothèses**, pas des résultats. Il sera faux en
partie — le rôle des tests de [`03`](03-plan-execution.md) est de dire où.

---

## Lot de test recommandé (ne pas tout lancer)

| Lot | Concepts | Pourquoi ceux-là |
|---|---|---|
| **Lot 1 — maintenant** | **A4** + **A1 ou A2** + **B2** | Une seule audience, un seul travail de veille, trois façons de gagner : abonnés (actif possédé), trafic d'intention (comparateur), revenu récurrent (affiliation). |
| **Lot 1 bis — canal de test** | **D1** en format court | 30 vidéos pour savoir si l'acquisition sociale fonctionne sur un sujet B2B. Jetable sans regret. |
| **Lot 2 — après validation de H2** | **C1**, **B3** | Ne se justifient que si l'audience a exprimé un problème précis. |
| **Lot 3 — 6 à 12 mois** | **E1** | Le micro-SaaS est la destination, pas le départ (6-18 mois avant rentabilité). |
| **Jamais sans signal fort** | **D2**, **C3**, **D3** | Risque juridique majeur, ou aucun avantage défendable. |

Trois concepts actifs simultanément : assez pour apprendre, pas assez pour
diluer 4 h/jour. Ouvrir dix comptes est l'erreur de débutant la plus coûteuse
en attention.

**Le choix qui reste à faire** : la **profession cible**. A4, A2, B2 et E1 en
dépendent tous. Méthode de sélection en phase 0 de [`03`](03-plan-execution.md).

---

## Fiches détaillées

Chaque fiche suit les 18 points demandés.

### A4 — Newsletter de veille pour une profession · score 81.4 · **rang 1**

1. **Concept** — Une synthèse hebdomadaire de ce qui change dans un métier :
   réglementaire, outils, marché, aides. Pour des professionnels qui n'ont pas
   le temps de suivre, et qui savent ce que coûte de rater une information.
2. **Audience** — Une profession précise (artisans du bâtiment, experts-
   comptables, infirmiers libéraux, agents immobiliers, restaurateurs…), pas
   « les entrepreneurs ».
3. **Pourquoi maintenant** — [DONNÉE] la plupart des métiers n'ont **aucune
   veille indépendante en français** ; les sources professionnelles existantes
   sont chères et institutionnelles. [DONNÉE] une newsletter B2B se sponsorise
   150-800 € l'insertion.
4. **Tendances observées** — [DONNÉE] CPM newsletter B2B FR 20-80 € ; [DONNÉE]
   beehiiv gratuit jusqu'à 2 500 abonnés, 0 % sur les abonnements payants.
5. **Potentiel d'audience** — [ESTIMATION] 1 000 à 5 000 abonnés sur une
   profession de taille moyenne en 12-18 mois. Petit en volume, dense en valeur.
6. **Potentiel économique** — 83.8/100. [ESTIMATION] à 1 500 abonnés :
   2 insertions/mois × 300 € = **600 €/mois**, plus affiliation logicielle.
7. **Affiliation** — Les logiciels du métier (gestion, facturation, planning),
   souvent en abonnement, donc commissionnables de façon **récurrente**.
8. **Produit potentiel** — Modèles et documents métier (C1), formation courte.
9. **SaaS potentiel** — Oui, en phase 3 : la newsletter fait remonter le
   problème récurrent que l'outil résoudra (E1).
10. **Difficulté** — Faible techniquement, moyenne éditorialement : la
    difficulté est la **régularité**, pas la production.
11. **Coût initial** — 0 €.
12. **Automatisation possible** — Élevée sur la collecte et le premier jet ;
    **la vérification et l'envoi restent humains**.
13. **Risques** — Choisir une profession trop étroite (pas d'annonceurs) ou trop
    large (pas d'avantage) ; information erronée ; lassitude.
14. **Contenu possible** — Échéances légales, nouveaux outils testés, chiffres
    du secteur, aides disponibles, revue de décisions marquantes.
15. **Plateformes** — beehiiv, plus LinkedIn et SEO pour l'acquisition (canaux
    naturels d'une audience professionnelle).
16. **Hypothèse à tester** — **H1** : ≥ 300 inscrits en 60 jours sans publicité,
    et ≥ 40 % de taux d'ouverture moyen sur 8 numéros (un B2B de niche doit
    ouvrir davantage qu'une liste grand public).
17. **Ce qui pourrait faire échouer l'idée** — La profession s'informe déjà via
    sa fédération ou ses groupes ; ou l'email n'est pas son canal.
18. **Métriques à surveiller** — Inscrits/semaine, taux d'ouverture, clics
    sortants, réponses reçues (**le meilleur signal qualitatif gratuit**),
    désinscriptions, marques ayant répondu à une sollicitation de sponsoring.

---

### A2 — IA appliquée à UN métier précis · score 78.9 · **rang 2**

1. **Concept** — Non pas « les 10 meilleurs outils IA », mais « comment un
   expert-comptable (ou un artisan, ou un RH) utilise concrètement l'IA cette
   semaine », avec des cas testés.
2. **Audience** — Les professionnels de ce métier, plus leurs fournisseurs.
3. **Pourquoi maintenant** — [DONNÉE] l'éducation IA/tech est la catégorie
   faceless en plus forte croissance en 2026, la demande y dépasse l'offre ;
   mais [DONNÉE] les **listes génériques d'outils IA sont explicitement
   saturées**. L'angle métier est la porte encore ouverte.
4. **Tendances observées** — [DONNÉE] RPM FR tech/SaaS B2B 5-12 € ; [DONNÉE]
   affiliation SaaS francophone jusqu'à 60 % récurrent à vie.
5. **Potentiel d'audience** — Moyen en volume, élevé en valeur.
6. **Potentiel économique** — **87.5/100**, deuxième meilleur du portefeuille.
7. **Affiliation** — Excellente et récurrente. [ESTIMATION] 40 clients actifs à
   24 €/mois de commission = **~960 €/mois** sans publier davantage.
8. **Produit potentiel** — Bibliothèque de prompts et de procédures métier.
9. **SaaS potentiel** — Fort : les usages répétés révèlent l'outil à construire.
10. **Difficulté** — Moyenne : il faut **réellement tester** les outils.
11. **Coût initial** — 0 € (versions gratuites des outils testés).
12. **Automatisation possible** — Moyenne, et c'est une limite saine : tester un
    outil ne s'automatise pas, et c'est exactement ce qui rend le contenu
    défendable.
13. **Risques** — Obsolescence rapide des outils ; affirmation fausse sur un
    logiciel payant ; dérive vers le générique (le piège principal).
14. **Contenu possible** — Cas d'usage chronométrés, comparatifs, tutoriels
    métier, « ce que l'IA ne sait pas faire dans ce métier ».
15. **Plateformes** — YouTube (long et court), LinkedIn, newsletter.
16. **Hypothèse à tester** — **H5** : ≥ 20 clics d'affiliation et ≥ 1 essai
    déclenché sur les 30 premiers contenus.
17. **Ce qui pourrait faire échouer l'idée** — L'audience métier n'est pas
    encore mûre sur l'IA ; ou elle veut un prestataire, pas de l'information.
18. **Métriques à surveiller** — Clics d'affiliation, essais déclenchés,
    abonnés récurrents générés, revenu récurrent cumulé (**le seul chiffre qui
    compte à 6 mois**).

---

### A1 — Facture électronique 2026-2027 · score 78.3 · **rang 3** (meilleur potentiel économique : 90/100)

1. **Concept** — Média d'accompagnement d'une obligation légale : pédagogie,
   échéances, annuaire comparatif des plateformes agréées et des logiciels de
   facturation, monétisé par affiliation récurrente.
2. **Audience** — Toute entreprise française assujettie à la TVA, et en premier
   lieu les TPE/PME/micro visées par l'échéance du 01/09/2027.
3. **Pourquoi maintenant** — [DONNÉE] obligation de **réception** effective
   depuis le **01/09/2026** ; obligation d'**émission** pour les PME/TPE/micro au
   **01/09/2027**. Passage obligatoire par une **plateforme agréée** et un
   **format structuré**. C'est une demande contrainte, datée, et adressant des
   millions d'entreprises.
4. **Tendances observées** — [DONNÉE] sources officielles (Urssaf,
   economie.gouv.fr, service-public.gouv.fr) convergentes sur le calendrier.
5. **Potentiel d'audience** — Très élevé sur 12 mois, en forte décroissance
   ensuite.
6. **Potentiel économique** — **90.0/100, le meilleur du portefeuille.**
7. **Affiliation** — Les logiciels de facturation/comptabilité sont vendus par
   abonnement : commissions **récurrentes** sur une décision d'achat contrainte
   par la loi. C'est la meilleure configuration d'affiliation du portefeuille.
8. **Produit potentiel** — Checklist de conformité, modèles, mini-formation (C2).
9. **SaaS potentiel** — Indirect (outil de vérification, de suivi d'échéances).
10. **Difficulté** — Moyenne : sujet aride, exigeant en rigueur.
11. **Coût initial** — 0 €.
12. **Automatisation possible** — Moyenne : la veille s'automatise, **la
    vérification non**. Une erreur sur une obligation légale n'est pas une
    erreur ordinaire.
13. **Risques** — **Durabilité 2/5 : la fenêtre se referme après 2027.**
    Risque juridique 2/5 : information réglementaire engageante. Le calendrier
    de cette réforme a déjà été modifié par le passé : toute page doit être
    datée et sourcée pour rester corrigeable.
14. **Contenu possible** — « Ce qui change pour vous au 1ᵉʳ septembre 2027 »,
    comparatif des plateformes agréées, erreurs fréquentes, calendrier par
    taille d'entreprise.
15. **Plateformes** — SEO en priorité (recherche d'information contrainte),
    newsletter, LinkedIn. Le format court est secondaire ici.
16. **Hypothèse à tester** — ≥ 1 000 impressions/jour en Search Console à 90
    jours sur 40 pages, et ≥ 5 clics d'affiliation par semaine.
17. **Ce qui pourrait faire échouer l'idée** — Les éditeurs de logiciels et les
    cabinets comptables occupent déjà le terrain avec des moyens supérieurs ; ou
    un nouveau report du calendrier vide le sujet de son urgence.
18. **Métriques à surveiller** — Impressions et positions, clics sortants par
    éditeur, essais déclenchés, **et la date : ce concept a une horloge**, et
    son plan de reconversion (vers la gestion d'entreprise) doit être écrit
    avant le milieu de 2027.

---

### A3 — Micro-entreprise / création d'entreprise · score 75.5 · **rang 4**

1. **Concept** — Média sur les statuts, charges, obligations et outils du
   créateur d'entreprise français.
2. **Audience** — [DONNÉE indicative] environ un million de créations
   d'entreprises par an en France : une audience qui se **renouvelle en
   permanence**.
3. **Pourquoi maintenant** — Pas de fenêtre particulière : c'est un flux
   continu, ce qui explique la meilleure note de durabilité du portefeuille (5/5).
4. **Tendances observées** — [DONNÉE] affiliation très riche : banques pro,
   comptabilité en ligne, outils de vente (jusqu'à 60 % récurrent).
5. **Potentiel d'audience** — Le plus élevé des concepts B2B (5/5).
6. **Potentiel économique** — 88.8/100.
7. **Affiliation** — Excellente, récurrente, avec un panier élevé.
8. **Produit potentiel** — Modèles de documents, parcours de démarrage.
9. **SaaS potentiel** — Moyen (marché déjà servi par des legaltech).
10. **Difficulté** — Élevée en concurrence (2/5) : blogs, cabinets et legaltech
    occupent le terrain avec des équipes entières.
11. **Coût initial** — 0 €.
12. **Automatisation possible** — **Faible (2/5)** : le droit et la fiscalité
    changent, l'exactitude est critique, la maintenance des pages est un travail
    permanent.
13. **Risques** — Responsabilité sur l'information juridique et fiscale ;
    concurrence établie ; international impossible (1/5).
14. **Contenu possible** — Guides par statut, simulateurs de charges,
    comparatifs d'outils.
15. **Plateformes** — SEO avant tout, newsletter, YouTube.
16. **Hypothèse à tester** — À ne lancer **que** si l'on identifie un angle
    différenciant précis (une profession, une situation, une étape). Sinon,
    c'est A4/A2 avec plus de concurrence.
17. **Ce qui pourrait faire échouer l'idée** — Impossible de se distinguer : le
    sujet est couvert par des acteurs mieux dotés depuis dix ans.
18. **Métriques à surveiller** — Positions sur les requêtes longues, clics
    sortants, conversions d'affiliation.

---

### B2 — Annuaire/comparateur de logiciels d'une niche · score 73.2 · **rang 5**

1. **Concept** — Comparer honnêtement les solutions d'un marché précis : prix
   réels, fonctionnalités, limites, cas d'usage.
2. **Audience** — L'acheteur au moment exact de sa décision : la valeur
   commerciale maximale de tout le parcours.
3. **Pourquoi maintenant** — C'est le **complément naturel** de A4/A1/A2 : la
   veille crée l'intention, le comparateur la monétise.
4. **Tendances observées** — [DONNÉE] affiliation SaaS récurrente ; [DONNÉE]
   Google désindexe les pages minces : un comparatif superficiel ne survivra pas.
5. **Potentiel d'audience** — Moyen, très qualifié.
6. **Potentiel économique** — 80.0/100.
7. **Affiliation** — Cœur du modèle (5/5).
8. **Produit potentiel** — Faible.
9. **SaaS potentiel** — Faible en direct ; excellent détecteur de besoin.
10. **Difficulté** — Moyenne : **tester réellement** les outils prend du temps,
    et c'est précisément ce qui crée l'avantage défendable.
11. **Coût initial** — 0 € + nom de domaine ~10 €/an.
12. **Automatisation possible** — Moyenne (3/5) : la structure se génère, le
    jugement non.
13. **Risques** — Obligation d'exactitude et de transparence (mention de
    l'affiliation) ; comparatif vieilli = perte de crédibilité immédiate ;
    pression commerciale des éditeurs sur le classement.
14. **Contenu possible** — Fiches outil, tableaux comparatifs, « le moins cher
    pour tel cas », alternatives françaises.
15. **Plateformes** — SEO, newsletter.
16. **Hypothèse à tester** — **H5** : ≥ 3 % de clics sortants sur les visiteurs,
    et au moins 1 conversion d'affiliation en 60 jours.
17. **Ce qui pourrait faire échouer l'idée** — Les éditeurs n'ont pas de
    programme d'affiliation, ou les comparateurs généralistes dominent la SERP.
18. **Métriques à surveiller** — Pages indexées, impressions, clics sortants par
    éditeur, conversions, **revenu récurrent cumulé**.

---
### B3 — Outils gratuits en ligne (calculateurs, simulateurs) · score 72.1 · **rang 6**

1. **Concept** — Un outil gratuit qui résout un calcul pénible et récurrent
   (charges, marge, devis, conversion de format), qui capte du trafic et des
   emails, puis bascule en version payante.
2. **Audience** — Celle qui fait ce calcul toutes les semaines.
3. **Pourquoi maintenant** — [DONNÉE] un outil réellement utile est exactement
   ce que Google continue d'indexer, alors que les pages de texte mince sont
   désindexées en masse.
4. **Tendances observées** — [DONNÉE] le freemium fonctionne quand l'outil a une
   **utilité quotidienne** ; sinon il ne convertit pas.
5. **Potentiel d'audience** — Élevé si le calcul est courant.
6. **Potentiel économique** — 77.5/100.
7. **Affiliation** — Moyenne (l'outil peut recommander un logiciel complet).
8. **Produit potentiel** — La version payante elle-même.
9. **SaaS potentiel** — C'est le chemin le plus naturel vers E1.
10. **Difficulté** — **Élevée (2/5 en facilité)** : construire un outil qui
    marche n'est pas écrire un article.
11. **Coût initial** — 0 € (hébergement statique), sauf si des calculs serveur
    deviennent nécessaires.
12. **Automatisation possible** — Bonne une fois construit.
13. **Risques** — Un calcul faux sur des charges sociales ou une TVA engage ;
    un outil copié en une semaine si la logique est triviale.
14. **Contenu possible** — Pages d'explication autour de l'outil (« comment se
    calcule X »), qui apportent le trafic.
15. **Plateformes** — Site + SEO.
16. **Hypothèse à tester** — ≥ 200 utilisations et ≥ 30 emails captés en 30
    jours, avant d'écrire la moindre fonctionnalité payante.
17. **Ce qui pourrait faire échouer l'idée** — Un tableur gratuit suffit déjà,
    ou l'outil est utilisé une fois par an.
18. **Métriques à surveiller** — Utilisations, **taux de retour** (l'indicateur
    décisif pour un outil), emails captés, conversion vers le payant.

---

### E1 — Micro-SaaS no-code B2B · score 71.5 · **rang 7**

1. **Concept** — Un outil qui résout **un** problème répétitif d'une profession,
   construit sans code, facturé dès le premier jour 19-49 €/mois.
2. **Audience** — La profession servie par A4/A2 — donc une audience déjà
   constituée et interrogeable, ce qui divise le risque.
3. **Pourquoi maintenant** — Pas maintenant : **en phase 3**. [DONNÉE]
   rentabilité typique atteinte en **6 à 18 mois**.
4. **Tendances observées** — [DONNÉE] pile no-code gratuite possible ; [DONNÉE]
   prix d'entrée standard 19-49 €/mois ; recommandation constante du secteur :
   **facturer dès le premier jour**, car un outil gratuit ne valide rien.
5. **Potentiel d'audience** — Faible en volume (2/5), élevé en valeur unitaire.
6. **Potentiel économique** — 76.2/100 ; revenu récurrent noté 5/5.
7. **Affiliation** — Sans objet.
8. **Produit potentiel** — C'est le produit.
9. **SaaS potentiel** — Par définition.
10. **Difficulté** — Élevée : même en no-code, un produit reste un produit
    (support, fiabilité, mises à jour).
11. **Coût initial** — Démarrage possible à 0 €, mais les plans payants des
    outils no-code arrivent vite avec les premiers utilisateurs.
12. **Automatisation possible** — Moyenne : **le support client n'est pas
    automatisable**, et c'est ce qui limite la croissance d'un solo.
13. **Risques** — Construire avant d'avoir validé le problème (l'erreur la plus
    fréquente et la plus coûteuse) ; dépendance à l'outil no-code choisi.
14. **Contenu possible** — Le journal de construction est lui-même un contenu
    qui attire l'audience concernée.
15. **Plateformes** — Web + la newsletter comme canal d'acquisition — d'où
    l'ordre du plan : **l'audience d'abord, le logiciel ensuite**.
16. **Hypothèse à tester** — Avant toute ligne : ≥ 10 professionnels décrivent
    spontanément le même problème, et ≥ 3 acceptent de payer d'avance.
17. **Ce qui pourrait faire échouer l'idée** — Le problème est réel mais pas
    assez douloureux pour justifier un abonnement ; ou un éditeur l'intègre
    gratuitement dans son offre.
18. **Métriques à surveiller** — Essais → payants, rétention à 3 mois, revenu
    récurrent mensuel, **tickets de support par client** (l'indicateur qui dit
    si le produit peut grossir sans vous).

---

### E2 — Automatisations prêtes à l'emploi en self-serve · score 68.7 · **rang 8**

1. **Concept** — Vendre des scénarios d'automatisation prêts à installer pour
   une profession (relances de devis, publication, tri de documents).
2. **Audience** — Les mêmes professionnels, côté gain de temps immédiat.
3. **Pourquoi maintenant** — Complément à faible effort d'un média existant.
4. **Tendances observées** — [DONNÉE] les plateformes d'automatisation ont des
   offres gratuites suffisantes pour démarrer.
5. **Potentiel d'audience** — Faible en volume.
6. **Potentiel économique** — 66.2/100.
7. **Affiliation** — Moyenne (commissions des plateformes d'automatisation).
8. **Produit potentiel** — C'est le produit (5/5).
9. **SaaS potentiel** — Chemin possible vers E1.
10. **Difficulté** — Moyenne.
11. **Coût initial** — 0 €.
12. **Automatisation possible** — Bonne.
13. **Risques** — Un scénario qui casse chez le client engage votre crédibilité
    sans que vous puissiez le corriger ; support difficile à l'échelle.
14. **Contenu possible** — Démonstrations « avant/après », gains de temps
    chronométrés.
15. **Plateformes** — Newsletter, site.
16. **Hypothèse à tester** — ≥ 5 ventes sur les 30 premiers jours après
    présentation à l'audience existante.
17. **Ce qui pourrait faire échouer l'idée** — Les acheteurs veulent que ce soit
    **installé pour eux** — ce qui est du service, donc non automatisable, donc
    hors cahier des charges.
18. **Métriques à surveiller** — Ventes, demandes de support, taux de
    remboursement.

---

### B1 — Site programmatique sur données publiques · score 67.3 · **rang 9**

1. **Concept** — Des milliers de pages générées depuis des jeux de données
   publics : une page par commune, par établissement, par métier, chacune
   portant une donnée chiffrée réelle et sourcée.
2. **Audience** — Trafic de recherche très large.
3. **Pourquoi maintenant** — [DONNÉE] plus de 10 000 nouveaux jeux de données
   publiés sur data.gouv.fr en 2025 ; [DONNÉE] un site lancé début 2024 sur ce
   principe atteint ~33 000 visites/mois, dont 80 % d'organique.
4. **Tendances observées** — [DONNÉE] depuis les mises à jour anti-spam de
   2025-2026, **seules les pages réellement utiles restent indexées** ; une
   donnée factuelle et attribuable est ce que citent les moteurs génératifs.
5. **Potentiel d'audience** — Le plus élevé en volume brut (5/5).
6. **Potentiel économique** — 67.5/100 seulement : le trafic est abondant mais
   peu qualifié, et le revenu **non récurrent** (2/5).
7. **Affiliation** — Bonne si la verticale choisie a des annonceurs.
8. **Produit potentiel** — Faible.
9. **SaaS potentiel** — Faible.
10. **Difficulté** — Moyenne : génération de pages, donc un minimum technique.
11. **Coût initial** — 0 € + nom de domaine.
12. **Automatisation possible** — **Totale (5/5)**, la meilleure du portefeuille.
13. **Risques** — **Vitesse de validation 2/5 : on ne sait qu'après 3 à 6 mois
    d'indexation.** C'est la seule raison de son classement médiocre malgré de
    vraies qualités — pour un débutant qui doit apprendre vite, attendre six
    mois pour un premier signal est un coût énorme. Autres risques : licences
    des données, désindexation si les pages sont jugées minces.
14. **Contenu possible** — Pages de données locales, classements, comparaisons.
15. **Plateformes** — Site + Search Console.
16. **Hypothèse à tester** — À lancer **en tâche de fond**, jamais comme test
    principal : la mesure arrive trop tard pour piloter un apprentissage.
17. **Ce qui pourrait faire échouer l'idée** — Pages jugées de faible valeur, ou
    verticale sans annonceur.
18. **Métriques à surveiller** — Pages indexées / publiées (**le vrai
    indicateur de qualité**), impressions, position moyenne, revenu par 1 000
    visites.

---

### D1 — Chaîne faceless éducation IA/tech en français · score 67.0 · **rang 10**

1. **Concept** — Format court et long sur l'usage concret de l'IA et des outils
   numériques, en voix de synthèse, sans visage.
2. **Audience** — Large, jeune, en demande.
3. **Pourquoi maintenant** — [DONNÉE] c'est la catégorie faceless **en plus
   forte croissance en 2026**, où la demande dépasse l'offre.
4. **Tendances observées** — [DONNÉE] **mais** les listes génériques d'outils IA
   sont citées parmi les formats les plus saturés. La croissance et la
   saturation coexistent : c'est l'angle qui sépare les deux.
5. **Potentiel d'audience** — 5/5.
6. **Potentiel économique** — 71.2/100.
7. **Affiliation** — Excellente et récurrente (5/5).
8. **Produit potentiel** — Bon.
9. **SaaS potentiel** — Moyen.
10. **Difficulté** — Moyenne.
11. **Coût initial** — 0 €.
12. **Automatisation possible** — Moyenne **volontairement** : au-delà, on entre
    dans la zone visée par la politique de contenu non authentique.
13. **Risques** — **Indépendance plateforme 2/5** et **avantage défendable 2/5**
    sans angle métier : c'est le concept le plus exposé du top 10. Il ne tient
    que s'il est adossé à A2 (une profession précise).
14. **Contenu possible** — Cas d'usage chronométrés, tests réels, erreurs
    fréquentes.
15. **Plateformes** — YouTube Shorts, TikTok, format long ensuite.
16. **Hypothèse à tester** — **H4** : ≥ 3 vidéos sur 30 dépassant 10 000 vues
    **et** ≥ 100 inscrits newsletter attribués, en 30 jours. Sinon
    l'acquisition bascule sur SEO + LinkedIn.
17. **Ce qui pourrait faire échouer l'idée** — Un sujet B2B ne perce pas dans un
    flux de divertissement ; ou l'audience acquise n'est pas transférable.
18. **Métriques à surveiller** — Rétention à 3 s, clics en bio, **inscrits
    attribués** (pas les vues), temps de production par vidéo.

---
### C1 — Produits numériques pour une profession · score 65.1 · **rang 11**

1. **Concept** — Modèles, tableurs et documents qui font gagner des heures à un
   professionnel précis, vendus 19-39 €.
2. **Audience** — Celle déjà constituée par A4/A2.
3. **Pourquoi maintenant** — En phase 2 : c'est le **test de solvabilité** (H2)
   le plus rapide et le moins coûteux qui existe.
4. **Tendances observées** — [DONNÉE] les produits éducatifs et les modèles
   dominent le marché ; un modèle qui fait gagner 5 h à un indépendant facturant
   60 €/h justifie facilement 19-39 €. [DONNÉE] Gumroad prélève ~13 % en coût
   effectif mais gère la TVA européenne ; Etsy ~10-12 % avec une **hausse des
   frais pour les créateurs numériques en mai 2026**.
5. **Potentiel d'audience** — Moyen.
6. **Potentiel économique** — **53.8/100 seulement** : revenu non récurrent
   (1/5) et avantage défendable très faible (2/5).
7. **Affiliation** — Faible.
8. **Produit potentiel** — C'est le produit (5/5).
9. **SaaS potentiel** — Un modèle très utilisé désigne l'outil à construire.
10. **Difficulté** — La plus faible du portefeuille (5/5).
11. **Coût initial** — 0 € jusqu'à la première vente.
12. **Automatisation possible** — Bonne (vente et livraison automatiques).
13. **Risques** — **Se copie en une après-midi** ; frais de plateforme en
    hausse ; aucune récurrence.
14. **Contenu possible** — Une version gratuite allégée comme aimant à
    inscriptions.
15. **Plateformes** — Gumroad ou Lemon Squeezy (3,5 % + 0,50 $, nettement moins
    cher), vente depuis la newsletter.
16. **Hypothèse à tester** — **H2** : ≥ 2 % d'achat sur les inscrits, sur une
    offre à 29 €.
17. **Ce qui pourrait faire échouer l'idée** — Équivalent gratuit disponible ; ou
    le métier n'achète pas de modèles.
18. **Métriques à surveiller** — Taux de conversion, remboursements, revenu par
    abonné, **et surtout : les demandes reçues après l'achat** (elles décrivent
    le produit suivant).

---

### C2 — Mini-formation sur une obligation réglementaire · score 63.4 · **rang 12**

1. **Concept** — Un cours court et opérationnel pour se mettre en conformité
   avec une obligation datée, vendu 49-149 €.
2. **Audience** — Les entreprises contraintes par l'échéance.
3. **Pourquoi maintenant** — L'urgence légale justifie un prix élevé — c'est
   précisément ce qui le rend **rentable et risqué**.
4. **Tendances observées** — [DONNÉE] calendrier de la facturation électronique
   (01/09/2026 et 01/09/2027).
5. **Potentiel d'audience** — Moyen.
6. **Potentiel économique** — 67.5/100.
7. **Affiliation** — Moyenne (l'outil recommandé en fin de parcours).
8. **Produit potentiel** — C'est le produit.
9. **SaaS potentiel** — Faible.
10. **Difficulté** — Moyenne, mais exige une **exactitude irréprochable**.
11. **Coût initial** — 0 €.
12. **Automatisation possible** — Moyenne.
13. **Risques** — **Risque juridique noté 1/5 : le plus élevé du portefeuille
    avec D2.** Vendre de la conformité engage ; la vente de formation a en outre
    son propre cadre réglementaire, y compris pour sa promotion. Et
    **durabilité 1/5** : le produit meurt avec l'échéance.
14. **Contenu possible** — Extraits gratuits comme aimant à inscriptions.
15. **Plateformes** — Depuis la newsletter uniquement.
16. **Hypothèse à tester** — À ne lancer **qu'après** validation de H2 sur un
    produit à faible enjeu (C1). Ne pas débuter par le produit le plus engageant.
17. **Ce qui pourrait faire échouer l'idée** — L'information officielle est
    gratuite et suffisante ; l'expert-comptable fait déjà le travail.
18. **Métriques à surveiller** — Conversion, remboursements, réclamations
    (**tolérance zéro** : une seule suffit à imposer une révision du contenu).

---

### D2 — Chaîne faceless finance / business · score 61.4 · **rang 13**

1. **Concept** — Contenu sur l'argent, l'entreprise et l'investissement, sans
   visage.
2. **Audience** — Très large, très convoitée par les annonceurs.
3. **Pourquoi maintenant** — Aucune raison propre à ce profil.
4. **Tendances observées** — [DONNÉE] **le meilleur RPM mesuré du marché
   français : 8-15 €, CPM 18-25 €.**
5. **Potentiel d'audience** — 5/5.
6. **Potentiel économique** — 72.5/100.
7. **Affiliation** — Bonne (courtiers, banques, outils).
8. **Produit potentiel** — Bon.
9. **SaaS potentiel** — Faible.
10. **Difficulté** — Élevée : concurrence notée 1/5.
11. **Coût initial** — 0 €.
12. **Automatisation possible** — Faible (2/5) : chaque affirmation engage.
13. **Risques** — **Risque juridique 1/5** : conseil en investissement,
    démarchage, promesse de gain. Pour un débutant sous pseudonyme, c'est le
    concept le plus dangereux du portefeuille : le meilleur RPM du marché
    s'accompagne du cadre le plus strict, et ce n'est pas une coïncidence.
14. **Contenu possible** — Sans objet.
15. **Plateformes** — Sans objet.
16. **Hypothèse à tester** — **[OPINION] Écarté du lot 1.** Le potentiel
    économique ne compense pas le couple risque juridique / concurrence
    (faisabilité 54.3/100).
17. **Ce qui pourrait faire échouer l'idée** — Une seule affirmation mal cadrée.
18. **Métriques à surveiller** — Sans objet tant que non lancé.

---

### C3 — Print on demand faceless · score 48.5 · **rang 14**

1. **Concept** — Designs vendus sur objets imprimés à la demande.
2. **Audience** — Grand public.
3. **Pourquoi maintenant** — **Contre-exemple assumé.** Ce concept figure dans
   l'étude pour montrer, chiffres à l'appui, pourquoi « facile et gratuit » n'est
   pas un critère de sélection.
4. **Tendances observées** — L'IA générative a multiplié l'offre de designs :
   l'avantage défendable est **noté 1/5**, le plus bas possible.
5. **Potentiel d'audience** — 4/5.
6. **Potentiel économique** — **36.2/100.**
7. **Affiliation** — Nulle.
8. **Produit potentiel** — Moyen.
9. **SaaS potentiel** — Nul.
10. **Difficulté** — Faible en production, extrême en visibilité.
11. **Coût initial** — 0 €.
12. **Automatisation possible** — Bonne — ce qui est justement le problème :
    tout le monde peut l'automatiser.
13. **Risques** — Contrefaçon, droits sur les visuels générés, marges écrasées.
14. **Contenu possible** — Sans objet.
15. **Plateformes** — Sans objet.
16. **Hypothèse à tester** — **Écarté.**
17. **Ce qui pourrait faire échouer l'idée** — L'absence totale de barrière à
    l'entrée : ce qui n'a coûté aucun effort ne vaut rien sur un marché ouvert.
18. **Métriques à surveiller** — Sans objet.

---

### D3 — Chaîne faceless divertissement · score 45.9 · **rang 15 (dernier)**

1. **Concept** — Histoires, motivation, musique relaxante, faits divers : le
   format faceless le plus répandu, et **le plus recommandé sur internet**.
2. **Audience** — Immense.
3. **Pourquoi maintenant** — **Contre-exemple central de cette étude.** C'est
   probablement ce que la plupart des guides « business IA » recommanderaient en
   premier ; les données disponibles disent l'inverse.
4. **Tendances observées** — [DONNÉE] musique relaxante, ASMR et histoires sont
   des **pièges à RPM : 0,50-2,50 $** avec une concurrence brutale ; citations
   de motivation, histoires reprises de forums et faits sur les célébrités
   figurent parmi les catégories explicitement saturées ; [DONNÉE] la politique
   de contenu non authentique vise exactement ce type de production, **au niveau
   de la chaîne**.
5. **Potentiel d'audience** — 5/5 — et c'est le piège : l'audience potentielle
   est le seul critère où ce concept gagne.
6. **Potentiel économique** — **30.0/100, le plus faible du portefeuille.**
7. **Affiliation** — Nulle (1/5).
8. **Produit potentiel** — Nul.
9. **SaaS potentiel** — Nul.
10. **Difficulté** — Faible en production.
11. **Coût initial** — 0 €.
12. **Automatisation possible** — **5/5 — et c'est exactement pourquoi il ne
    faut pas le faire.** Ce qu'une machine peut produire entièrement, mille
    machines le produisent déjà.
13. **Risques** — Démonétisation, droits musicaux, dépendance plateforme notée
    1/5.
14. **Contenu possible** — Sans objet.
15. **Plateformes** — Sans objet.
16. **Hypothèse à tester** — **Écarté.**
17. **Ce qui pourrait faire échouer l'idée** — Tout : l'économie, les règles de
    plateforme, et l'absence de barrière.
18. **Métriques à surveiller** — Sans objet.

---

## Ce que ce portefeuille démontre

1. **Audience ≠ argent.** D3 a l'audience potentielle maximale et le pire
   potentiel économique du portefeuille (30/100). A4, avec une audience cent
   fois plus petite, obtient 83.8.
2. **Ce qui est facile n'a pas de valeur.** C3 et D3 sont les deux concepts les
   plus simples à lancer, et les deux derniers du classement. En 2026, la
   facilité d'exécution est devenue un **signal négatif** : ce qu'une IA fait
   seule, tout le monde le fait déjà.
3. **Le rendement le plus élevé s'accompagne du cadre le plus strict.** D2
   (finance) a le meilleur RPM mesuré du marché français et la pire note de
   risque juridique. Ce n'est pas un hasard : les annonceurs paient cher parce
   que l'accès est difficile.
4. **La vitesse de validation vaut plus qu'on ne croit.** B1 est techniquement
   excellent (automatisation 5/5, effet de stock réel) mais tombe au 9ᵉ rang
   parce qu'il ne donne son premier signal qu'après 3 à 6 mois. Pour quelqu'un
   qui doit apprendre vite, c'est rédhibitoire.
5. **Le classement est révisable par construction** : changez les poids, il
   change. Ce qui n'est pas négociable, c'est de le confronter aux tests.

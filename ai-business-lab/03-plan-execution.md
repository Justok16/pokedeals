# 03 — Plan d'exécution

Deux règles qui priment sur tout ce document :

1. **Aucune production avant que le circuit de mesure existe.** Publier sans
   mesurer, c'est fabriquer une opinion, pas une donnée.
2. **Aucune production avant que la profession cible soit choisie.** C'est la
   seule décision bloquante aujourd'hui.

---

## PHASE 0 — Choisir la profession cible (jour 1, 2 h maximum)

Quatre des cinq concepts du lot 1 en dépendent. C'est la seule décision que
cette étude ne peut pas prendre à votre place, parce qu'elle dépend de ce que
vous connaissez déjà et des communautés auxquelles vous avez accès.

**Méthode, en trois questions filtrantes :**

| Question | Pourquoi elle filtre | Élimination si… |
|---|---|---|
| **1. Ce métier achète-t-il déjà des logiciels ?** | S'il existe 5 éditeurs qui s'adressent à lui, un budget existe **et** des annonceurs existent | Aucun logiciel spécialisé n'existe → pas d'affiliation, pas de sponsors |
| **2. Ce métier a-t-il une actualité qui change ?** | Sans changement, pas de veille, donc pas de raison de s'abonner | Rien ne bouge dans ce métier → une veille n'a pas d'objet |
| **3. Puis-je lire ce que disent ces gens quelque part ?** | Groupes, forums, commentaires : c'est votre source de problèmes réels | Aucune communauté accessible → vous écrirez à l'aveugle |

**Candidats crédibles** [OPINION, à valider par la méthode ci-dessus] :
artisans du bâtiment, infirmiers et professions libérales de santé, agents
immobiliers, restaurateurs, experts-comptables et collaborateurs de cabinet,
professionnels RH de PME, e-commerçants, photographes et prestataires
indépendants.

**Critère de départage, s'il en reste plusieurs** : prendre celui pour lequel
**l'échéance de facturation électronique du 01/09/2027** est la plus anxiogène
(TPE et indépendants sans service administratif). Cela permet de servir A4 et
A1 avec le même travail.

**À ne pas faire** : choisir « les entrepreneurs » ou « les freelances ». Trop
large, aucun avantage défendable, concurrence maximale.

---

## PHASE 1 — Les comptes à créer (jour 1-2, ~2 h)

| Compte | Pour quoi | Coût | Remarque |
|---|---|---|---|
| **beehiiv** | Newsletter A4 | 0 € | Gratuit jusqu'à 2 500 abonnés, 0 % sur les abonnements payants |
| **Hébergement statique gratuit** | Comparateur B2, pages A1 | 0 € | Le site est l'actif ; le nom de domaine viendra plus tard |
| **Google Search Console** | SEO | 0 € | Dès la première page publiée |
| **LinkedIn** (pseudo) | Acquisition B2B | 0 € | Canal naturel d'une audience professionnelle, souvent sous-estimé |
| **TikTok + YouTube** (pseudo) | Test d'acquisition D1 | 0 € | Lire la politique de contenu non authentique **avant** de publier |
| **Programmes d'affiliation** des logiciels du métier | Monétisation | 0 € | Vérifier les taux **réels** et la récurrence avant de bâtir dessus |
| **Tableau de bord** (fichier CSV) | Mesure | 0 € | Modèle fourni dans `modeles/` |

**Ne pas créer** : Instagram, X, Pinterest, Discord, Facebook. 4 h/jour
réparties sur huit plateformes ne produisent aucun signal exploitable.

**Contrainte légale** dès le premier lien d'affiliation : mention
« Publicité » ou « Collaboration commerciale » claire et visible, mentions
légales identifiant l'éditeur sur le site, et micro-entreprise dès le premier
revenu régulier (cf. `06`).

---

## PHASE 2 — Les outils gratuits (jour 2)

beehiiv (newsletter), hébergement statique gratuit, Search Console, ChatGPT
(déjà souscrit), outils de montage gratuits et voix de synthèse intégrées pour
le test D1, un tableur pour le tableau de bord. **Total : 0 €/mois.**
Détail, alternatives et seuils de bascule : [`09-outils-et-budget.md`](09-outils-et-budget.md).

---

## PHASE 3 — L'architecture (un seul travail, trois sorties)

```
        [ VEILLE sur UNE profession ]   <- le seul travail de fond
        (réglementaire, outils, marché, aides)
                      |
        +-------------+-------------+
        |             |             |
        v             v             v
   A4 newsletter  B2 comparateur  D1 contenus courts
   (actif possédé)  (intention)     (acquisition, jetable)
        |             |             |
        +------ liens d'affiliation récurrents ------+
                      |
                      v
            [ Tableau de bord unique ]
                      |
                      v
    CONTINUER / MODIFIER / AMPLIFIER / ARRÊTER (hebdo)
```

Principe : **une veille, trois monétisations**. C'est ce qui rend tenable de
mener trois concepts de front à 4 h/jour — ils partagent 80 % du travail.

---

## PHASE 4 — Les premiers workflows (semaine 1)

| Routine | Fréquence | Entrée | Sortie | Automatisation |
|---|---|---|---|---|
| Collecte de veille | quotidienne (20 min) | sources officielles du métier, éditeurs, communautés | notes brutes datées | Assistée |
| Rédaction du numéro | hebdo | notes de la semaine | brouillon | Assistée, **vérification humaine obligatoire** |
| Pages comparateur | hebdo | tests d'outils | 3-5 fiches | Semi-auto |
| Scripts courts | quotidienne | sujets de la semaine | 2 scripts | Assistée, **publication humaine** |
| Collecte des métriques | quotidienne | beehiiv, Search Console, plateformes | tableau de bord | Manuelle au début, automatisée ensuite |
| Niche Radar | hebdo | sources de `04` | fiches d'opportunité | Assistée |

**Ne pas automatiser en semaine 1.** Faire chaque tâche cinq fois à la main
avant de l'automatiser : sinon on automatise une erreur.

---

## PHASE 5 — Les premiers contenus (semaine 2)

- **A4** : 8 numéros, 1/semaine, structure fixe : ce qui a changé · l'échéance à
  ne pas rater · un outil testé · un chiffre du secteur. **Publier même à 12
  abonnés** — la régularité est le produit.
- **B2/A1** : 20 pages en 4 semaines. **Règle absolue : aucune page sans un
  élément que l'on n'a pas ailleurs** (prix réel constaté, test, tableau
  comparatif, source officielle citée et datée). Google désindexe le reste.
- **D1** : 30 vidéos en 30 jours, 3 formats × 10, pour trancher H4.

---

## PHASE 6 — Les tests

| # | Hypothèse | Test | Durée | Seuil de succès | Si échec |
|---|---|---|---|---|---|
| **H1** | Une profession s'abonne à une veille hebdo | 8 numéros + page d'inscription | 60 j | ≥ 300 inscrits **et** ≥ 40 % d'ouverture | Changer de profession (pas de format) avant d'abandonner le concept |
| **H2** | Cette audience paie | Offre à 29 € aux inscrits | à J+75 | ≥ 2 % d'achat | Renoncer au produit, miser sur sponsoring + affiliation |
| **H3** | Des annonceurs achètent une insertion | Proposer une insertion à 5 éditeurs du métier | 30 j | ≥ 1 accord, même à tarif réduit | Le sponsoring attendra 1 000 abonnés ; l'affiliation porte le revenu |
| **H4** | L'acquisition sociale fonctionne sur un sujet B2B | 30 vidéos, 3 formats | 30 j | ≥ 3 vidéos > 10 000 vues **et** ≥ 100 inscrits attribués | Arrêter le format court, basculer sur SEO + LinkedIn |
| **H5** | L'affiliation logicielle convertit | Liens sur comparateur + newsletter | 60 j | ≥ 1 conversion payante **et** ≥ 3 % de clics sortants | Revoir le choix des programmes avant de conclure quoi que ce soit |

**Chaque test a une date de fin écrite à l'avance.** Un test sans date se
transforme en projet qu'on n'ose plus arrêter.

---

## PHASE 7 — Les métriques

Suivies quotidiennement : inscrits/jour, taux d'ouverture, **clics sortants**
(le meilleur prédicteur de revenu), conversions d'affiliation, revenu par
contenu, coût, temps de production. Schéma complet dans
[`05-tableau-de-bord.md`](05-tableau-de-bord.md).

**Interdits** : nombre d'abonnés sur les réseaux, likes, impressions seules.
Ce sont des indicateurs de vanité qui font continuer des projets morts.

---

## PHASE 8 — Les critères de décision (dimanche, 30 min)

Une seule question par concept : **le signal progresse-t-il par rapport à la
semaine précédente ?**

- 3 semaines sans progression → **MODIFIER** (une seule variable) ;
- 3 semaines de plus → **ARRÊTER**, le jour même, sans discussion ;
- seuil dépassé → **AMPLIFIER** (règle de SCALE dans `05`).

---

## PHASE 9 — La monétisation (à partir de J+45)

Ordre d'activation, du moins engageant au plus engageant (chiffres dans
[`06`](06-monetisation-risques.md)) :

1. **affiliation logicielle récurrente** — le pilier, car un client acquis
   rapporte tous les mois ;
2. sponsoring de newsletter (H3) ;
3. produit numérique à 29 € (H2) ;
4. offre premium ou abonnement ;
5. micro-SaaS (E1), en phase 3 seulement ;
6. revenus publicitaires des plateformes — **en dernier**, parce que c'est le
   revenu le plus faible et le plus fragile.

---

## PHASE 10 — L'automatisation (continue)

Ce qui s'automatise, ce qui reste humain, et pourquoi :
[`07-automatisation-agents.md`](07-automatisation-agents.md).

---

## Plan des 90 premiers jours

### Jours 1-7 — Fondations (ne rien publier)
- Phase 0 : **choisir la profession** (2 h, pas 2 semaines).
- Vérifier en 48 h : éditeurs existants, communautés actives, sujets qui bougent.
- Créer les comptes, lire les politiques de monétisation et d'affiliation.
- Préparer 4 numéros et 10 scripts d'avance.
- **Livrable** : tout est prêt, rien n'est public, la page d'inscription est en
  ligne.

### Jours 8-37 — Premier cycle
- A4 : 1 numéro/semaine, sans exception.
- B2/A1 : 5 pages/semaine.
- D1 : 1 vidéo/jour (30 au total).
- Contacter 5 éditeurs du métier (H3), par email, sans relance agressive.
- **Livrable J+37** : H4 et H3 tranchées.

### Jours 38-60 — Concentration
- Arrêter ce qui n'a pas atteint son seuil, **sans exception**.
- Doubler l'effort sur le canal d'acquisition qui a fonctionné.
- Activer l'affiliation sur les pages et numéros les plus cliqués.
- **Livrable J+60** : H1 et H5 tranchées ; premiers euros ou preuve documentée
  que la monétisation ne vient pas de là.

### Jours 61-90 — Première monétisation
- Tester l'offre à 29 € (H2).
- Écrire la fiche du premier problème récurrent exprimé par l'audience
  (matière première du futur E1).
- Publier le bilan trimestriel : ce qui a marché, ce qui a été tué, pourquoi.
- **Livrable J+90** : 1 ou 2 concepts vivants, un revenu mesuré même faible, et
  un actif possédé (liste email + pages indexées) qui n'appartient à aucune
  plateforme.

**Ce qu'il ne faut pas attendre de ces 90 jours** : un revenu significatif.
**Ce qu'il faut en attendre** : des décisions fondées sur des chiffres réels,
et la fin de l'incertitude sur trois ou quatre hypothèses majeures.

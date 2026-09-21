# 03 — Plan d'exécution

Règle qui prime sur tout ce document : **aucune production de contenu avant que
le circuit de mesure existe**. Publier sans mesurer, c'est fabriquer une opinion,
pas une donnée.

---

## PHASE 1 — Les comptes à créer (jour 1-2, ~2 h)

| Compte | Pour quoi | Coût | Remarque |
|---|---|---|---|
| **beehiiv** | Newsletter A2 | 0 € | Gratuit jusqu'à 2 500 abonnés, 0 % sur les abonnements payants |
| **TikTok** (pseudo) | A1 acquisition | 0 € | France éligible au Creator Rewards (10 k abonnés / 100 k vues 30 j) |
| **YouTube** (chaîne pseudo) | A1 Shorts | 0 € | Lire la politique de contenu non authentique **avant** de publier |
| **Google Search Console** | D3/A5 | 0 € | Indispensable dès la première page publiée |
| **eBay Partner Network** | Affiliation | 0 € | Vérifier le barème FR réel une fois connecté |
| **Amazon Partenaires** | Affiliation d'appoint | 0 € | 1-3 % sur les jeux : marginal, à ne pas surinvestir |
| **Compte de mesure** (fichier ou Supabase) | Tableau de bord `05` | 0 € | La base existe déjà côté SaaS |

**Ne pas créer** : Instagram, X, LinkedIn, Pinterest, Discord. Non pas parce
qu'ils sont mauvais, mais parce que 4 h/jour réparties sur 8 plateformes ne
produisent aucun signal exploitable. Ils s'ouvriront à la phase SCALE.

**Contrainte légale** dès le premier compte monétisé : pseudonyme autorisé, mais
mention « Publicité »/« Collaboration commerciale » obligatoire sur tout contenu
contenant un lien d'affiliation, et mentions légales identifiant l'éditeur sur
le site (cf. `06`).

---

## PHASE 2 — Les outils gratuits (jour 2-3)

Déjà disponibles, à coût nul : **GitHub Actions** (l'automatisation la plus
précieuse du dispositif : ~20 crons qui tournent sans serveur),
**Python + le moteur existant**, **ChatGPT payant** (déjà souscrit),
**beehiiv**, **GitHub Pages** (hébergement statique), **Search Console**,
**Supabase** (offre gratuite, déjà en place).

Détail, alternatives et seuils de bascule payante : [`09-outils-et-budget.md`](09-outils-et-budget.md).

---

## PHASE 3 — L'architecture technique

```
   [ Moteur PokéDeals existant ]   (scan 83+ boutiques, eBay, Vinted, LBC)
                 |
                 v
   [ Base de faits : cotes.json + historique + stock + précommandes ]
                 |
     +-----------+-----------+-----------------+
     |           |           |                 |
     v           v           v                 v
  A2 news.    D3 compara.  A1 scripts       A4 alertes
  (beehiiv)   (statique)   (TikTok/Shorts)  (Telegram/email)
     |           |           |                 |
     +-----------+-----------+-----------------+
                 |
                 v
        [ Tableau de bord unique ]  <- clics, inscrits, revenus, coûts
                 |
                 v
        [ Décision hebdo : CONTINUER / MODIFIER / AMPLIFIER / ARRÊTER ]
```

Principe directeur : **une seule base de faits, plusieurs sorties**. Chaque
nouveau concept est une *sortie* de la base existante, jamais une nouvelle
collecte. C'est ce qui rend le coût marginal d'un concept quasi nul.

---

## PHASE 4 — Les premiers workflows (semaine 1)

| Workflow | Fréquence | Entrée | Sortie | Automatisation |
|---|---|---|---|---|
| `generer_newsletter` | hebdo (samedi) | cotes + historique + précommandes | brouillon beehiiv | Auto, **validation humaine avant envoi** |
| `generer_comparateur` | quotidien | stock boutiques | pages statiques | Auto complète |
| `generer_scripts_video` | quotidien | meilleurs deals du jour | 3 scripts + données | Auto, **publication humaine** |
| `collecter_metriques` | quotidien | plateformes + Search Console | tableau de bord | Auto complète |
| `niche_radar` | hebdo (lundi) | sources externes (`04`) | fiches d'opportunité | Auto, **arbitrage humain** |

Ces workflows suivent exactement le modèle déjà éprouvé dans ce dépôt : cron
GitHub Actions + écriture d'un fichier d'état + garde-fous. Rien de neuf à
apprendre.

---

## PHASE 5 — Les premiers contenus (semaine 2)

- **A2** : 4 numéros préparés à l'avance, publiés 1/semaine. Structure fixe :
  1 indice de marché, 3 mouvements de prix, 2 bonnes affaires vérifiées, 1
  calendrier de sorties.
- **D3** : 200 pages produit générées, puis 50/jour. **Règle absolue : pas une
  page sans donnée réelle** (prix, disponibilité, historique). Une page vide est
  une dette de référencement, pas un actif.
- **A1** : 1 vidéo/jour pendant 30 jours, 3 formats testés (comparaison de prix,
  variation de cote, alerte précommande), 10 vidéos chacun.

**Qualité** : chaque contenu doit apporter une information que le spectateur
n'avait pas. Le jour où un contenu n'existe que pour remplir le calendrier, il
ne se publie pas — c'est exactement le comportement que les plateformes
sanctionnent désormais au niveau du compte.

---

## PHASE 6 — Les tests (jour 1 à 90)

| # | Hypothèse | Test | Durée | Seuil de succès | Si échec |
|---|---|---|---|---|---|
| **H1** | L'audience veut une synthèse hebdo par email | Publier 8 numéros, capter sur tous les canaux | 60 j | ≥ 300 inscrits **et** ≥ 35 % d'ouverture | Passer l'info en Telegram/Discord, tuer le format email |
| **H2** | Cette audience paie | Offre à 19 € proposée aux inscrits | à J+75 | ≥ 2 % d'achat | Renoncer au produit, miser sur affiliation + B2B |
| **H3** | Les boutiques acceptent un accord | Contacter 20 boutiques déjà scannées | 30 j | ≥ 3 accords | Monétiser D3 par affiliation généraliste uniquement |
| **H4** | Le contenu « donnée » surperforme | 30 vidéos, 3 formats | 30 j | ≥ 3 vidéos > 10 k vues **et** ≥ 100 inscrits attribués | Arrêter A1, réallouer sur D3/A5 |
| **H5** | La cote FR a une valeur B2B | Démo à 10 pros | 45 j | ≥ 3 pilotes payants | Reporter A3 de 6 mois |

**Chaque test a une date de fin écrite à l'avance.** Un test sans date se
transforme toujours en projet qu'on n'ose plus arrêter.

---

## PHASE 7 — Les métriques

Suivies quotidiennement et automatiquement (schéma complet dans [`05`](05-tableau-de-bord.md)) :
inscrits/jour, taux d'ouverture et de clic, **clics sortants** (le vrai
prédicteur de revenu), conversions, revenu par contenu, coût, temps de
production par contenu.

**Interdits de tableau de bord** : nombre d'abonnés sur les réseaux, likes,
impressions seules. Ce sont des indicateurs de vanité qui font continuer des
projets morts.

---

## PHASE 8 — Les critères de décision (revue hebdomadaire, 30 min, le dimanche)

Pour chaque concept actif, une seule question : **le signal mesuré est-il en
progression par rapport à la semaine précédente ?**

- 3 semaines sans progression → **MODIFIER** (changer l'angle, pas le concept) ;
- 3 semaines de plus sans progression → **ARRÊTER**, sans discussion ;
- seuil de test atteint → **AMPLIFIER** (cf. règle de SCALE dans `05`).

La revue est courte par construction : si elle dure plus de 30 minutes, c'est
que le tableau de bord ne dit pas ce qu'il doit dire.

---

## PHASE 9 — La monétisation (à partir de J+45, jamais avant)

Ordre d'activation, du moins risqué au plus engageant (détail chiffré dans
[`06`](06-monetisation-risques.md)) :

1. affiliation sur le comparateur et la newsletter (0 engagement) ;
2. accords directs avec les boutiques (H3) ;
3. sponsoring de newsletter (à partir de ~1 000 abonnés) ;
4. produit numérique (test de H2) ;
5. offre premium récurrente ;
6. A3 en B2B self-serve ;
7. revenus publicitaires des plateformes — **en dernier**, parce que c'est le
   revenu le plus faible et le plus fragile (RPM FR 0,40-1,20 €).

---

## PHASE 10 — L'automatisation (continue)

Ce qui s'automatise dès maintenant, ce qui reste humain, et pourquoi :
[`07-automatisation-agents.md`](07-automatisation-agents.md). Règle : on
n'automatise **jamais** une étape qu'on n'a pas encore faite à la main au moins
cinq fois — sinon on automatise une erreur.

---

## Plan des 90 premiers jours

### Jours 1-7 — Fondations (ne rien publier)
- Créer les comptes (phase 1), lire les politiques de monétisation.
- Écrire `generer_newsletter` et `collecter_metriques`.
- Générer les 200 premières pages du comparateur.
- Préparer 4 numéros de newsletter et 10 scripts vidéo d'avance.
- **Livrable** : tout est prêt, rien n'est public.

### Jours 8-37 — Premier cycle de test
- A1 : 1 vidéo/jour (30 au total, 3 formats).
- A2 : 1 numéro/semaine.
- D3 : +50 pages/jour, Search Console surveillée.
- B1 : ajouter un 2ᵉ TCG à la watchlist (2 h une seule fois).
- Contacter 20 boutiques (H3) — 5/semaine, par email, sans relance agressive.
- **Livrable J+37** : H4 et H3 tranchées.

### Jours 38-60 — Concentration
- Arrêter ce qui n'a pas atteint son seuil, **sans exception**.
- Doubler la production sur le format gagnant de A1.
- Activer l'affiliation sur les pages et numéros les plus cliqués.
- **Livrable J+60** : H1 tranchée ; premiers euros ou preuve d'absence de
  monétisation.

### Jours 61-90 — Première monétisation et préparation du palier suivant
- Tester l'offre à 19 € (H2) auprès des inscrits.
- Démarcher 10 pros pour A3 (H5) — uniquement si H1 est validée.
- Publier le bilan trimestriel : ce qui a marché, ce qui a été tué, pourquoi.
- **Livrable J+90** : un portefeuille réduit à 1 ou 2 concepts vivants, chacun
  avec un revenu mesuré (même faible) et un plan d'amplification.

**Ce qu'il ne faut pas attendre de ces 90 jours** : un revenu significatif.
Ce qu'il faut en attendre : **des décisions fondées sur des chiffres réels**,
et un actif possédé (liste email + trafic) qui n'appartient à aucune plateforme.

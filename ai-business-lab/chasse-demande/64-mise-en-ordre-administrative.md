# 64 — Mise en ordre administrative avant les premiers appels (10/10/2026)

Demande de l'utilisateur : « tout mettre en ordre avant d'appeler les premiers prospects ». Liste suivie dans
l'ordre ci-dessous ; chaque fait vient de la page officielle citée, lue le 10/10/2026.

| # | Démarche | Où | État |
|---|---|---|---|
| 1 | Espace professionnel impots.gouv (code d'activation par courrier) | impots.gouv.fr → Votre espace professionnel | À faire (téléphone) |
| 2 | Espace URSSAF auto-entrepreneur (déclarations, suivi ACRE) | autoentrepreneur.urssaf.fr ou appli | À faire (téléphone) |
| 3 | Compte bancaire réservé à DIG16 | voir § 1 (Indy, gratuit) | À faire (téléphone) |
| 4 | Déclaration initiale de CFE 1447-C-SD + exonération FRR+ | espace pro impots.gouv, **avant le 31/12/2026** | Après l'étape 1 (PC) |
| 5 | Plateforme agréée de facturation électronique (réception obligatoire depuis le 01/09/2026) | voir § 1 | À faire |
| 6 | Encaissement par prélèvement SEPA mensuel | voir § 2 | Choix à valider (frais) |
| 7 | Google Search Console | `63` § 3 | PC |
| 8 | Activation du formulaire FormSubmit (lien reçu sur contact@dig16.fr) | boîte contact@dig16.fr | À vérifier |
| 9 | France Travail (si inscrit) | appli France Travail | Selon situation |

## 1. Facturation électronique et compte pro : Indy (offre Essentiel, 0 €)

- Liste officielle DGFiP des plateformes agréées (page modifiée le 22/09/2026, fichier
  `liste_pa_attente_rapport_audit.xlsx`, 149 opérateurs) : **INDY** et **ABBY** y figurent.
  https://www.impots.gouv.fr/je-consulte-la-liste-des-plateformes-agreees
- Page tarifs d'Indy (lue le 10/10) : offre Essentiel « 0€ » : « Facturation électronique (Plateforme agréée) »,
  « Devis et factures en illimité », « Compte pro avec IBAN et CB ». Factures récurrentes : offre Plus ; livre des
  recettes et déclaration URSSAF : offre Autonomie. https://www.indy.fr/tarifs/
- Abby (offre Basique 0 €) : facturation électronique, devis et factures illimités, livre des recettes ; pas de
  compte bancaire. https://abby.fr/tarifs
- Choix proposé : **Indy Essentiel** (compte pro + plateforme agréée + factures, gratuit), livre des recettes tenu par
  Claude (tableur) tant que l'offre gratuite suffit. Les « mandats de prélèvement » d'Indy servent à **être prélevé**
  (débiteur), pas à prélever les clients (wikicompta.indy.fr, article 9388795).

## 2. Encaissement des abonnements par prélèvement SEPA

| Outil | Tarif officiel (lu le 10/10, hors TVA) | Pour 49 € | Pour 79 € |
|---|---|---|---|
| GoCardless (plan Standard) | « 1 % + 0,20 € par transaction », plafonné à 2 € (transactions nationales), « pas de frais de mise en place » — https://gocardless.com/fr-fr/tarifs/ | 0,69 € | 0,99 € |
| Stripe (prélèvement SEPA + Billing) | « 0,35 € par paiement réussi », 3,50 € par échec, 15 € par litige — https://stripe.com/fr/pricing/local-payment-methods ; Billing « 0,7 % » — https://stripe.com/fr/billing/pricing | 0,69 € | 0,90 € |

Franchise en base de TVA : la TVA sur ces frais n'est pas récupérable (coût réel majoré si elle est facturée).
Choix proposé : **GoCardless** (fait pour le prélèvement récurrent : le client signe le mandat en ligne, aucuns
frais d'échec affichés sur la page lue) ; décision de l'utilisateur (engage des frais).

## 3. CFE (formulaire 1447-C-SD)

- À déposer **au plus tard le 31 décembre de l'année de création** ; une exonération voulue dès la première année
  doit être demandée **sur ce formulaire** (BOFiP, conditions de dépôt de la 1447-C-SD ; formulaire :
  https://www.impots.gouv.fr/formulaire/1447-c-sd/declaration-initiale-de-cotisation-fonciere-des-entreprises).
- Dépôt hors délai : l'exonération n'est pas accordée pour l'année (BOFiP).
- Annexe 1447-E-SD pour les exonérations absentes du formulaire principal. Exonération FRR+ : ligne exacte
  **[à vérifier sur la notice 2026 au moment du remplissage]**.
- Année de création : pas de CFE (dépliant CET 2026 d'impots.gouv) ; réduction de la base l'année suivante
  **[à vérifier sur la notice 2026]**.

## 4. Objectif de l'utilisateur (10/10) : « quand un client signe, le moins de choses à faire »

Chaîne visée après chaque signature : ce que Claude fait seul, et les rares gestes qui restent à l'utilisateur
(ceux qui engagent son identité ou son argent).

| Étape | Qui | Outil |
|---|---|---|
| Vérifier le client avant signature (annuaire officiel + BODACC) | Claude | `outils/verif_entreprises.py` |
| Devis et contrat pré-remplis, envoyés pour signature électronique | Claude prépare ; l'utilisateur relit et envoie | modèles devis/CGV (Drive « Dig ») |
| Mandat de prélèvement envoyé au client | Claude prépare le lien | GoCardless (§ 2) |
| Questionnaire de lancement envoyé au client (textes, photos, horaires) | Claude | `Dig-Questionnaire-lancement-site.pdf` |
| Construction du site (7 jours), compte Cloudflare au nom du client | Claude ; l'utilisateur valide l'envoi | démos + Cloudflare Pages |
| Facture mensuelle émise par la plateforme agréée | Claude prépare, l'utilisateur valide le premier mois | Indy (§ 1) |
| Livre des recettes, déclaration URSSAF (rappel à chaque échéance) | Claude tient le livre ; l'utilisateur déclare (identité) | tableur + appli URSSAF |
| Modifications demandées (3 jours ouvrés), bilan mensuel | Claude | Gmail + routine |
| Retard de paiement : relance, puis procédure `45` | Claude rappelle et rédige | `45-impayes-se-proteger.md` |

À construire au premier client payant (règle « pas de construction sans demande ») : le tableau de bord
clients (`39` § 6.4) et les modèles d'emails de chaque étape.

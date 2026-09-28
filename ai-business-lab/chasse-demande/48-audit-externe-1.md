# 48 — Audit externe n° 1 (reçu le 28/09/2026) et suite donnée

Prompt utilisé : `supports/prompt-audit-externe.md`. L'auditeur (une autre IA) a lu le site et
la démo menuisier, pas le dépôt. Note moyenne : 4,5/10. Message central : « bon produit, vrai
marché, cadre légal soigné — et zéro contact humain ; 30 jours 100 % terrain, 0 % construction ».

## 1. Vérifications faites à la source (28/09/2026)

| Affirmation de l'audit | Verdict | Source lue |
|---|---|---|
| Franchise de TVA services : 37 500 € | **Exact** (seuil majoré 41 250 €) | Service Public Entreprendre F21746, « Vérifié le 01 janvier 2026 » |
| Facturation électronique : réception obligatoire au 01/09/2026, émission au 01/09/2027 pour les micro-entreprises | **Exact** (« 1er septembre 2026 » / « 1er septembre 2027 ») | economie.gouv.fr, « Tout savoir sur la facturation électronique » |
| Vendre sans immatriculation = travail dissimulé | **Exact**, article **L8221-3** du code du travail (version du 01/01/2023) : « l'exercice à but lucratif […] par toute personne qui […] n'a pas demandé son immatriculation au registre national des entreprises […] ». Déjà prévu : rien de commercial avant la création (39, section 9, point 1) | Légifrance |
| Dénigrement : « art. D. 32-1 loi 1881 » | **Référence erronée** (cet article n'existe pas dans cette loi). La base habituelle est la responsabilité civile (article 1240 du Code civil) — **à vérifier** avant de l'affirmer. Le fond du conseil reste juste : prix publics, sans jugement | — |
| « 2 refus sur ~37 réponses » | **Mauvaise lecture** : 37 éditeurs contactés ; réponses = 2 refus + accusés de réception automatiques | 25-reprise-atlassian.md |
| « La démo menuisier reste générique » | **Normal** : les démos publiques utilisent des entreprises fictives (écrit dans les mentions légales). Les démos personnalisées des prospects ne sont **pas** en ligne (dossier de travail et livret PDF privés) | site, mentions légales |
| Mentions légales incomplètes (nom, SIREN « à venir ») | **Exact** : version de présentation ; à compléter le jour de la création | site-dig/mentions-legales.html |
| Conversion 10-20 % en face-à-face | **Opinion non sourcée**, à mesurer | — |

## 2. Ce qui est juste et appliqué ou à appliquer

- **Critique principale acceptée** : 0 contact client en 9 jours, alors que la règle n° 1 exige
  une preuve de demande. Priorité absolue : montrer des démos à de vrais prospects.
- **Gel des constructions** : plus de nouveau document, de nouvelle page ni de nouvelle
  automatisation pour la piste Dig tant qu'il n'y a pas de preuve de demande. Exceptions :
  les corrections et ce qui sert directement aux premiers rendez-vous.
- **Piste Atlassian** : on ne fait que la relance du 08/10, rien d'autre avant un « oui ».
- **Démos personnalisées** : jamais publiées en ligne sans accord écrit ; montrées sur écran,
  supprimées en cas de refus (règle ajoutée au contrôle qualité).

## 3. Décisions qui appartiennent à l'utilisateur (posées le 28/09)

1. **Test de demande sans vente** : 10 à 30 visites « étude de marché » (montrer la démo,
   demander l'avis et l'intérêt, sans signature ni paiement) **avant** la création ; puis
   création de la micro-entreprise dès le premier « oui ferme ». *Point juridique à confirmer :
   l'article L8221-3 vise « l'exercice à but lucratif » ; une étude sans vente ni contrat
   n'est pas une vente, mais aucune signature ni aucun paiement avant l'immatriculation.*
2. **Réduire à 3 formules** (Essentiel, Visibilité, Prestige) pour le discours en boutique ;
   Présence et Achat restent « sur demande ».
3. **Base de vidéos Finary/Fintales** : l'auditeur la juge hors sujet. Elle tourne seule
   (Gemini gratuit, fiches groupées) et ne prend pas de temps à l'utilisateur ; décision de
   l'utilisateur : continuer, ralentir ou arrêter.
4. Réponses aux questions de l'auditeur (temps disponible par jour, etc.).

---

# Audit externe n° 2 (PDF reçu le 28/09/2026, 9 pages)

Même prompt, autre IA. Verdict plus dur : **abandon immédiat de la piste Atlassian**, 100 % du
temps sur Dig, arrêt des vidéos et du point automatique, 100 appels et 20 visites en 10 jours.
Notes : pistes 4, demande 2, offre 7, acquisition 6, juridique 5, Atlassian 1, temps 3,
livrables 8, risques 4, potentiel 6 (1 500 à 3 000 €/mois de revenu récurrent visé).

## Vérifications à la source (28/09/2026)

| Affirmation | Verdict | Source lue |
|---|---|---|
| Contrat hors établissement entre professionnels (≤ 5 salariés, hors activité principale) : rétractation de 14 jours et formulaire obligatoires (L221-3) | **Exact, et déjà traité** dans `40-cadre-legal-sites.md` (L221-3, L221-18, L221-10) et dans le parcours de vente de `41` | 40 (vérifié le 25/09 sur Légifrance) |
| Atlassian exige vérification et double authentification pour devenir partenaire | **Exact** : « Marketplace Partner enrollment completed (agreement, due diligence, 2SV) » | developer.atlassian.com, « Register as an Atlassian Marketplace Partner » |
| SOC 2 / ISO 27001 / bug bounty payant obligatoires | **Exagéré** : exigés seulement pour les niveaux Silver, Gold et Platinum du programme (« Platinum… SOC II Type 2 or ISO 27001:2022 », « Gold… audits scheduled », « Silver… Bug Bounty… the most installs »), pas pour entrer sur la Marketplace | developer.atlassian.com, « Marketplace Partner Program » |
| « Un particulier ne peut pas franchir ces barrières » | **Contredit** : plusieurs éditeurs ciblés sont des vendeurs individuels (ex. le vendeur 1215814, « individuel »). Mais la vérification (due diligence) suppose une identité et, pour nous, une entreprise créée avant tout transfert | 25-reprise-atlassian.md |
| « Plus de 95 % des utilisateurs payants déjà migrés vers Forge » | **Correction** : notre propre fichier `24-atlassian-fin-connect.md` note déjà qu'« Atlassian affirme que plus de 95 % des postes payants ont migré ». Le marché résiduel est donc petit | 24 (blog officiel Atlassian) |
| Démos publiques avec logos et coordonnées de vrais artisans | **Faux** : les démos en ligne sont fictives (mentions légales, section 3) ; les démos personnalisées restent privées | site-dig |
| Signer des contrats « sous condition suspensive d'immatriculation » avant la création | **Déconseillé** : non vérifié juridiquement ; règle maintenue : aucune signature ni aucun paiement avant l'immatriculation | L8221-3 |
| 0 € de création = risque d'impayé et marge initiale négative | **Juste** : décision de prix pour l'utilisateur (frais de mise en service ou premier mois payé d'avance) ; procédure d'impayés dans `45` | 45-impayes-se-proteger.md |

## Nouvelles décisions pour l'utilisateur

- Piste Atlassian : l'audit n° 1 dit « relance du 08/10 seulement », l'audit n° 2 dit « abandon
  immédiat ». Avis de Claude : la relance coûte presque 0 ; la garder, sans aucun autre travail.
- Offre : ajouter des frais de mise en service ou faire payer le premier mois d'avance, pour
  couvrir le travail de départ et limiter les impayés.
- Assurance RC professionnelle : devis à demander au moment de la création (déjà prévu dans 39).

---

# Audit externe n° 3 (reçu le 28/09/2026)

Même prompt, troisième IA, sans accès au site ni au dépôt. Le plus prudent des trois : continuer
Dig 30 jours comme **test commercial limité** ; suspendre Atlassian sauf la relance du 08/10.
Notes : 4, 1, 3, 3, 3, 2, 2, 4, 3, 2. Canal conseillé en premier : **l'appel professionnel ciblé**
(40 appels), démo privée seulement si l'artisan est intéressé, visite ensuite. Scénarios à 12 mois
sans probabilité : 0 à 18 clients (0 à 1 170 €/mois bruts).

## Erreurs de notre dossier relevées par l'audit n° 3 (vérifiées)

1. **Atlassian — les clients ne perdent pas l'accès.** Blog officiel Atlassian « Announcing
   Connect End of Support » (17/03/2025) : « Customers who have Connect apps installed won't lose
   access to the app, but this is an undesired state for customers due to lack of support ».
   Blog du 06/08/2025 : « Connect will no longer receive security updates or feature updates.
   Over time, some Connect features may stop working ». Notre message aux éditeurs disait
   « your customers may lose these apps » : **formulation trop forte**. La relance du 08/10 doit
   dire « plus de mises à jour de sécurité, fonctions qui peuvent cesser de marcher avec le
   temps » (correction reportée dans `25-reprise-atlassian.md`).
2. **Le prompt d'audit sous-estimait les refus** : il disait « au moins 2 refus » alors que le
   dossier en compte **10 sur 37** au 27/09 (1 ticket en cours, 26 silences). Erreur de Claude,
   corrigée dans `supports/prompt-audit-externe.md`.

## Autres points vérifiés

| Affirmation | Verdict | Source lue (28/09/2026) |
|---|---|---|
| Les « pages par commune » peuvent être des pages satellites | **Exact, risque réel** : Google cite parmi les abus « Having multiple domain names or pages targeted at specific regions or cities that funnel users to one page ». Chaque page locale doit avoir un contenu propre et utile (chantiers réels, horaires, accès), sinon ne pas en faire | Google Search Central, « Spam policies for Google web Search » |
| Fiche Google gérée par un tiers : accord du client, propriété, transparence | **Exact** : « all end customers must retain ownership or co-ownership of their Business Profile at all times » ; « If you charge a management fee, you must let end customers know that Business Profile is a service provided at no extra cost » ; changements sans accord interdits | Google, « Business Profile third-party policies » |
| Prélèvement SEPA : pré-notification du montant et de la date (14 jours sauf délai convenu) | **À vérifier** dans les règles SEPA et dans le fonctionnement de Stripe ; à écrire dans le mandat et les CGV | — |
| Franchise TVA, facturation électronique, rétractation hors établissement | Exact (déjà vérifié : audits 1 et 2 ; fichier 40) | — |
| Revenu « net » de 1 400 €/mois pour 30 clients | Le calcul (39, section 7) retire cotisations 25,6 % et frais, **pas** l'impôt ni le temps passé : dire « après cotisations et frais », pas « net » | 39 |

## À appliquer (sans décision de prix)

- Mesurer le **temps réel** de fabrication d'une démo et d'un site livré (question commune aux
  3 audits) ; noter la propriété du code, du domaine et des accès en fin de contrat (déjà : « le
  site vous appartient »), à écrire noir sur blanc dans les CGV.
- Mention à ajouter dans l'offre et les CGV le jour de la création : « la fiche Google est un
  service gratuit de Google ; le client en reste propriétaire ».

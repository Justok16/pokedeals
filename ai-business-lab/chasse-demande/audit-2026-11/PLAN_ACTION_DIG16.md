# Plan d'action DIG16 (issu de l'audit du 04/11/2026)

Classé par priorité. Pour chaque action : qui la fait, et ce qu'elle engage.

## A. Priorité haute

| # | Action | Qui | Engage | Statut |
|---|---|---|---|---|
| A1 | Dire où se trouve « Audit 0.4.5 » (lien, dépôt ou fichier) | Utilisateur (une ligne) | Rien | **BLOQUÉ** : introuvable dans le dépôt, le Drive et Gmail |
| A2 | Sauvegarde durable du journal privé (`ETAT.md`) et des lots dans le Drive « Dig », chaque semaine au point du dimanche soir | Claude, après le « oui » de l'utilisateur (coût en jetons : environ 15 000 par copie) | Rien d'autre que le quota | **À DÉCIDER** |
| A3 | Mesure d'audience : obtenir de Metricool la preuve d'exemption CNIL, sinon remplacer par un compteur sans tiers (fonction Cloudflare Pages) | Claude prépare ; l'utilisateur choisit | Perte éventuelle des statistiques Metricool du site | **À DÉCIDER** |
| A4 | Transferts hors UE : vérifier l'adhésion de Cloudflare et de Devro LABS (FormSubmit) au Data Privacy Framework, puis compléter les mentions légales avec la preuve | Claude | Modification juridique : relecture et accord de l'utilisateur avant publication | **À FAIRE** (site officiel illisible depuis le conteneur le 04/11 ; réessayer avec un autre outil) |

## B. Au premier client (règle « construire sur demande »)

| # | Action | Qui |
|---|---|---|
| B1 | Ouvrir le livre des recettes (`outils/compta/livre_recettes.py`, CSV privé) et faire envoyer par l'utilisateur une capture de l'export des factures d'Indy, pour éviter la double saisie | Claude, avec une capture de l'utilisateur |
| B2 | Paragraphe « sous-traitants » des clients (Indy, GoCardless, DocuSeal, Google) dans les mentions et les CGV, vérifié le jour même | Claude ; publication validée par l'utilisateur |
| B3 | Registre des traitements simplifié (modèle CNIL), en privé dans le Drive « Dig » | Claude |
| B4 | Ranger les DPA (contrats de sous-traitance) de FormSubmit, Metricool et Cloudflare dans le Drive | Claude |

## C. Échéances réglementaires (déjà programmées)

| Date | Quoi | Rappel |
|---|---|---|
| 06/11/2026 | Impôts « Adhérer aux services » | trig_01PapKxGXAECdRyQHBwssBz7 |
| 10/12/2026 | CFE 1447-C-SD avant le 31/12 | trig_01K1FQ78F7BjPoMyp3zGXssc |
| 05/01/2027 | 1re déclaration URSSAF trimestrielle | voir 64 § 0 |
| 13/04/2027 | Déclaration des revenus 2026 (ZFRR+) | trig_01Ee2ux8W6i2nFZSug691sUK |
| **04/05/2027** | **Facturation électronique : émission et e-reporting (Indy)** | **trig_01NtmbRzdCZSdDdsMK21ikx1 (créé le 04/11)** |
| 01/09/2027 | Émission électronique obligatoire et e-reporting (transactions et paiements, tous les deux mois) | même rappel |
| 30/09/2027 | Fin de l'ACRE | trig_01B4ZT6gs7oqc3cz5HqKVxzX |

## D. Recommandations sans urgence

- Garder **Indy** comme logiciel et comme plateforme agréée. Ne désigner **aucune** autre plateforme (risque d'écraser la
  réception).
- Les outils hérités de l'étude de marché de septembre (catalogues d'applications) sont gardés tels quels ; ils ne
  coûtent rien.
- PokéDeals : code gardé, tâches arrêtées. Le dépôt pourra être allégé plus tard, sur décision de l'utilisateur.

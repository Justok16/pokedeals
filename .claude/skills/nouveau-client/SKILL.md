---
name: nouveau-client
description: Parcours complet et automatisé d'un nouveau client DIG16 (site créé, vendu ou offert) — vérification de l'entreprise, kit de 12 documents, contrôle qualité, signature électronique DocuSeal, Drive « Dig », facture et paiement, comptes au nom du client, référencement, rappels de suivi. À utiliser dès que l'utilisateur dit qu'un client signe, qu'un site client est créé ou livré, ou demande « les papiers » d'un client, pour que rien ne soit oublié.
---

# Nouveau client DIG16 : tout, dans l'ordre, sans rien oublier

Consignes : `72-kit-client-complet.md` (kit), `45-impayes-se-proteger.md` § 1 (vérifier avant de signer),
`44-controle-qualite.md` (avant tout envoi), `65-seo-sites-clients.md` (livraison, comptes, avis), `.claude/CLAUDE.md`.
Données du client et de DIG16 : **toujours privées** (scratchpad `prive/` ou Drive « Dig »), jamais dans le dépôt.
Au moindre doute sur un point qui engage (prix, remise, délai, identité) : demander à l'utilisateur.

## Étape 1 — Vérifier l'entreprise (avant toute signature)
1. Connecteur **Contract-Factory SIREN** : `search_company` (nom + commune), puis `get_company` et `get_etablissements`
   → SIREN, état actif, adresse, dirigeant (signataire), code NAF.
2. Secteur autorisé ? (liste des exclus dans `.claude/CLAUDE.md`). Sinon : stop, prévenir l'utilisateur.
3. BODACC (procédures collectives, radiation) : `python3 outils/verif_entreprises.py entree.json sortie.json /tmp/cj.txt`
   (relais Vercel ; entrée/sortie privées).
4. Écrire ces contrôles dans le JSON client privé, clé `dossier.controles` (point, résultat, source datée).

## Étape 2 — Le JSON client privé
Modèle : reprendre le JSON du client précédent (scratchpad `prive/`), remplacer **toutes** les valeurs. Champs : identité de
l'entreprise (étape 1), formule et prix **relus sur dig16.fr le jour même**, remise éventuelle (accord de l'utilisateur),
`dossier` : adresse_site, paiement, option_suivi, place_id (fiche Google), pages.

## Étape 3 — Produire le kit (12 documents)
`python3 outils/kit_client.py --prestataire <prive/dig16.json> --client <prive/client.json> --sortie <dossier privé>`
Puis `python3 outils/traces_autre_client.py <dossier du site> --avoid "<ancien client>" …` : aucune trace d'un autre client.

## Étape 4 — Contrôle qualité (obligatoire avant tout envoi)
Contrôle complet de `44-controle-qualite.md` : orthographe (`orthographe.py`, `typo_fr.py`), pages PDF lisibles sur
téléphone (`pdf_pages.py`), affirmations périmées, mêmes prix partout. Puis **relecteur en lecture seule** (agent).

## Étape 5 — Signature électronique (DocuSeal, gratuit : 10 demandes par mois)
Modèles prêts : 6628706 (devis + CGV), 6628707, 6628708, 6628709 (vérifier avec `load_template`).
Préparer `send_documents` avec les valeurs pré-remplies (rôles « DIG16 » et « Client ») ; **l'envoi au client est validé
par l'utilisateur** (c'est un engagement). Au-delà de 10 envois par mois : lien de signature envoyé depuis la boîte DIG16.

## Étape 6 — Ranger et transmettre
Envoyer les PDF à l'utilisateur (`SendUserFile`) et les déposer dans le Drive « Dig » (dossier du client).
Mettre à jour 64 § 0 et `scratchpad/appels/ETAT.md`.

## Étape 7 — Paiement et facture

- **Contrôle CFE 2026 (décision de l'utilisateur du 31/10/2026 : « oui, mais seulement si on approche de la limite »)** : pour toute vente signée avant le 31/12/2026, additionner le CA HT déjà encaissé en 2026 (livre des recettes) et celui de ce client, puis `python3 ai-business-lab/chasse-demande/outils/fiscal/simulateur.py --cfe2026 <total>`. Si le total dépasse ou approche 1 164 € HT : proposer à l'utilisateur de convenir avec le client d'un démarrage, d'une facture et d'un paiement en janvier 2027 (`31` § 2 ter, levier 5). Un client pressé reste prioritaire : on ne perd jamais une vente pour la CFE.
- Formules mensuelles : lien de mandat SEPA GoCardless (compte de l'utilisateur) à faire signer par le client.
- Facture : émise le jour de la mise en ligne définitive, par **Indy** (plateforme agréée de facturation électronique) ;
  Claude prépare, l'utilisateur valide. Inscrire la recette au livre des recettes.
- Rappeler à l'utilisateur le « rappel investissement » et la franchise de TVA (règles promises dans `.claude/CLAUDE.md`).

## Étape 8 — Livraison du site (`65` § 1)
`seo_client.py` sans ALERTE, `--schema` (entreprise locale), tests téléphone et ordinateur, Lighthouse ≥ 90, accessibilité,
formulaire testé (`test_formulaire.py`), aucune police chargée depuis Google, IndexNow. Comptes **au nom du client**
(domaine, hébergement, fiche Google, Search Console, Bing ; `65` § 2), DIG16 gestionnaire. PV de réception à signer.

## Étape 9 — Rappels de suivi (send_later ou create_trigger)
- J+1 après livraison : PV de réception signé ? facture émise ? paiement reçu ?
- Chaque mois (Visibilité, Prestige) : rapport mensuel (`65` § 4).
- Avant échéance de paiement : contrôle du prélèvement ; retard → `45` § 3.
- 45 jours avant l'expiration du nom de domaine du client : renouvellement.
- Kit avis Google : dès que la fiche du client est validée.

## Étape 10 — Fin
Une ligne dans 64 § 0 et `46` si un outil ou une étape a été améliorée ; commit + push des fichiers **publics** seulement.
Message à l'utilisateur : ce qui est prêt, et « À TOI : » uniquement pour les signatures, l'identité ou le paiement.

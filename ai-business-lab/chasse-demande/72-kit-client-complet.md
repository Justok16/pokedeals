# 72 — Kit client complet : tout ce qui accompagne un site, par formule (26/10/2026)

Demande de l'utilisateur du 26/10 : « Quand je te demande de me créer un site pour un client, je veux aussi que tu me
crées tout ce qui va avec. L'administratif, les supports… tout ce que tu proposes dans chaque formule. Quand un site est
créé, je veux que le client et moi-même n'ayons plus qu'à signer les documents et c'est réglé. »

Règle (dans `.claude/CLAUDE.md`) : **un site client n'est jamais livré seul**. À chaque site (même offert), Claude produit
le kit complet avec `python3 outils/kit_client.py --prestataire <privé> --client <privé> --sortie <dossier privé>`,
le contrôle (`44-controle-qualite.md` + relecteur en lecture seule), l'envoie à l'utilisateur et au Drive « Dig »,
et ne laisse au client et à l'utilisateur que les signatures et ce qu'aucun outil ne peut faire à leur place
(identité, paiement, comptes à leur nom).

## 1. Ce que produit le kit (dossier privé, jamais dans le dépôt)

| N° | Document | Formules | Qui signe / qui fait | Outil ou modèle |
|---|---|---|---|---|
| 0 | Fiche de contrôle du client avant signature (annuaire officiel, BODACC, secteur, signataire) | toutes | Claude (interne) | `kit_client.py` + `verif_entreprises.py` (`45` § 1) |
| 1 | Devis et bon de commande + information et formulaire de rétractation | toutes | client « Bon pour accord » + DIG16 | `documents_client.py`, `supports/modele-devis.html` |
| 2 | Conditions générales de vente | toutes | remises avec le devis | `supports/cgv-dig.html` |
| 3 | Facture (projet, datée et émise le jour de la mise en ligne définitive) | toutes | DIG16 | `supports/modele-facture.html` |
| 4 | Questionnaire de lancement pré-rempli | toutes | complété au rendez-vous de 20 min | `supports/questionnaire-lancement-site.html` |
| 5 | Accord de réalisation gracieuse | site offert | client + DIG16 | `accord_gracieux.py` |
| 6 | Procès-verbal de réception du site (contrôles faits, réserves, acceptation) | toutes | client « Site reçu et accepté » + DIG16 | `supports/kit-client/pv-reception.html` |
| 7 | Mode d'emploi du site (compris, modifications, paiement, arrêt, problèmes, parrainage) | toutes, texte propre à la formule | remis au client | `supports/kit-client/mode-d-emploi.html` |
| 8 | « Vos comptes, à votre nom » (domaine, hébergement, formulaire, fiche Google, Search Console, Bing) | toutes | fait **avec** le client au rendez-vous | `supports/kit-client/vos-comptes.html` |
| 9 | Remise des fichiers du site | Achat, Prestige en une fois, départ d'un client | client « Fichiers reçus » + DIG16 | `supports/kit-client/remise-fichiers.html` |
| 10 | Textes d'annonce de la mise en ligne (page Facebook, fiche Google sans téléphone ni email, SMS, signature) | toutes | client publie | `kit_client.py` (texte) |
| 11 | Kit avis Google (carte A6 QR + messages) | Visibilité, Prestige | remis au client dès que sa fiche est ouverte | `kit_avis.py` (place_id) |
| — | LISEZMOI.md : qui signe quoi, qui fait quoi, quand | toutes | Claude | `kit_client.py` |
| — | Mandat de prélèvement SEPA (formules mensuelles et options) | mensuelles | client (lien GoCardless) | compte GoCardless de l'utilisateur (`64` § 2) |

Chaque phrase des documents reprend le devis, les CGV, l'accord gracieux ou dig16.fr : aucun engagement nouveau n'est
inventé. Si une formule change (prix, contenu), mettre à jour `kit_client.py` (`formule_info`) le même jour que le site.

## 2. Ce que Claude fait aussi, sans document (par formule)

| Étape | Essentiel | Visibilité | Achat | Prestige |
|---|---|---|---|---|
| Site 5 pages / sur mesure, galerie, formulaire de devis, mentions légales, données personnelles | ✓ | ✓ | ✓ | ✓ (+ anglais, réservation) |
| Contrôles de livraison (`65` § 1 : `seo_client.py` 0 ALERTE, tests téléphone/ordinateur, Lighthouse ≥ 90, accessibilité, formulaire testé, IndexNow) | ✓ | ✓ | ✓ | ✓ |
| Données structurées « entreprise locale » (`seo_client.py --schema`) | ✓ | ✓ | ✓ | ✓ |
| Comptes au nom du client, DIG16 gestionnaire (`65` § 2) | ✓ | ✓ | ✓ (puis remise) | ✓ |
| Fiche Google : textes et photos préparés | ✓ | ✓ + suivi mensuel (`65` § 4) | ✓ | ✓ + suivi mensuel |
| Kit avis Google | — | ✓ | — | ✓ |
| Rapport mensuel (visites, demandes, points d'amélioration) | ✓ | ✓ | option 15 €/mois | ✓ (abonnement) ou option 29 €/mois |
| Modifications (3 jours ouvrés) | 1/mois | 3/mois | option : 1 petite/mois | incluses (abonnement) |
| Remise des fichiers | en partant | en partant | à la livraison | en partant / à la livraison |

## 3. Ce qui reste au client ou à l'utilisateur (et pourquoi)

- **Signatures** : devis, accord gracieux le cas échéant, PV de réception, remise des fichiers.
- **Mandat SEPA** (formules mensuelles) : signé par le client sur le lien GoCardless de l'utilisateur.
- **Nom de domaine, hébergement, fiche Google, Search Console** : ouverts **au nom du client** (décision du 05/10) ; Claude
  prépare tout et guide au rendez-vous, mais la création des comptes demande l'identité et la carte bancaire du client.
- **Validation Google de la fiche** (appel, vidéo ou courrier) : seul le client peut la faire.
- **Première activation du formulaire** (email de confirmation reçu par le client) : un clic du client.

## 4. Points à trancher par l'utilisateur (posés le 26/10)

1. Signature : électronique (DocuSeal, gratuit et illimité — mais la conversion automatique des champs demande l'API
   complète, leçon du 19/10) ou papier au rendez-vous (PDF imprimé ou signé sur l'écran) ?
2. Mesure d'audience des sites clients pour le rapport mensuel : outil à choisir (sans cookie, gratuit, au nom du client).
3. Compte GoCardless : inscription terminée ? (sans lui, pas de mandat SEPA : paiement par virement en attendant).
4. Nom de domaine : acheté par le client (recommandé, à son nom) ou avancé par DIG16 puis refacturé ?

## 5. Historique

- 25/10 : règle « chaque site créé = documents pré-remplis » (documents 1 à 5, `documents_client.py`), testée sur FD Touchatou.
- 26/10 : kit complet (documents 0, 6 à 11, LISEZMOI), modèles `supports/kit-client/`, testé sur FD Touchatou (Prestige offerte).

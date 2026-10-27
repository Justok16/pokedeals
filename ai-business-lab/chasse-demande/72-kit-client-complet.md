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

## 4. Décisions de l'utilisateur (26/10, le soir même)

1. **Signature électronique par email, avec DocuSeal.** Vérifié sur docuseal.com/pricing le 26/10 : offre cloud « Basic » à 0 $,
   **« 10 request emails per month »**, **API non incluse** (« eSignature API : No » ; Pro à 20 $ par mois). Donc : pas d'API ;
   le connecteur DocuSeal (déjà relié) sert à créer les modèles et à envoyer les demandes ; les champs à remplir et à signer
   sont placés **une fois** par l'utilisateur dans l'éditeur DocuSeal sur des modèles génériques (devis, accord gracieux,
   PV de réception, remise des fichiers) ; ensuite chaque envoi est automatique (`send_documents`, valeurs pré-remplies).
   Au-delà de 10 emails par mois : envoyer soi-même le lien de signature (depuis la boîte DIG16). À mettre en place : voir § 6.
2. **Mesure d'audience des sites clients** : l'outil sans cookie de l'hébergeur (Cloudflare Web Analytics, déjà utilisé sur
   dig16.fr), sur le compte du client ; le rapport mensuel s'appuie dessus + Search Console.
3. **Paiement** : « on propose tout » : prélèvement SEPA (mandat GoCardless signé en ligne) **ou virement**, au choix du client.
4. **Nom de domaine** : enregistré par DIG16 **au nom du client**, coût avancé puis **refacturé au prix coûtant**.
   Comptabilité (BOFiP BOI-TVA-BASE-10-10-30, lu le 26/10) : un « débours » exclu du chiffre d'affaires suppose une facture
   du tiers au nom du client (ou mentionnant que DIG16 agit pour lui) et un compte rendu exact ; la facture du bureau
   d'enregistrement étant au nom de DIG16, la ligne refacturée est **comptée dans le chiffre d'affaires** (environ 10 € par
   client et par an, sans marge) : simple et sans risque.

## 5. Historique

- 25/10 : règle « chaque site créé = documents pré-remplis » (documents 1 à 5, `documents_client.py`), testée sur FD Touchatou.
- 26/10 : kit complet (documents 0, 6 à 11, LISEZMOI), modèles `supports/kit-client/`, testé sur FD Touchatou (Prestige offerte).
- 26/10 soir : 4 décisions de l'utilisateur appliquées (§ 4) ; CGV art. 3 et devis : nom de domaine enregistré par DIG16 au nom du client, avancé et refacturé au prix coûtant.

## 6. Signature électronique : mise en place (à faire)

1. **Fait le 26/10** : `outils/modeles_docuseal.py` produit les 4 PDF génériques (identité du prestataire intégrée, donc privés : sortie hors du dépôt), les aperçus annotés (bleu = DIG16, rouge = Client) et `LISEZMOI-champs.md` (noms exacts des champs). Modèles créés vides par le connecteur (le PDF ne peut pas être chargé par lui sans adresse publique) : n° 6628706 (devis + CGV), 6628707 (accord gracieux), 6628708 (PV de réception), 6628709 (remise des fichiers), lien `https://docuseal.com/templates/<n°>/edit`. PDF, aperçus et liste des champs envoyés à l'utilisateur ; note privée « DIG16 – Modèles DocuSeal : liens et champs » dans le Drive « Dig ».
2. **À TOI (une fois, sur ordinateur, environ 20 minutes)** : ouvrir chaque lien, importer le PDF du même numéro, placer les champs sur les cadres jaunes en recopiant exactement leur nom (rôles « DIG16 » et « Client »). Quota gratuit : 10 emails de demande par mois ; au-delà, envoyer soi-même le lien de signature.
   **27/10 (soir) : modèle 1 (6628706, devis + CGV) TERMINÉ par l'utilisateur, guidé sur captures** : rôles « DIG16 » et « Client », 11 champs vérifiés par `load_template` (noms, rôles, types exacts) ; « Exécution immédiate » rendue facultative selon l'utilisateur (non lisible par le connecteur). Astuces confirmées : choisir le rôle en haut à droite, outil puis rectangle dessiné à la souris, renommer en cliquant sur le nom dans l'étiquette de la zone (case à cocher : dans la colonne de droite), ne jamais taper dans la zone (sinon valeur par défaut). Restent les modèles 2, 3 et 4.
3. Ensuite, à chaque client : `send_documents` avec les valeurs pré-remplies ; le client signe sur son téléphone ; DIG16 contresigne ; le PDF signé est rangé dans le Drive « Dig ».


# 45 — Se protéger des impayés (fiche validée par l'utilisateur le 27/09/2026)

À rappeler à l'utilisateur **dès qu'un client signe** (vérification) et **dès
qu'un paiement est en retard** (procédure). Sources officielles lues le
27/09/2026 ; revérifier les montants au moment de s'en servir.

## 1. Avant de signer : vérifier le client (fait par Claude à chaque signature)

- Annuaire officiel : <https://annuaire-entreprises.data.gouv.fr> (entreprise
  active ou fermée). Depuis le conteneur : relais Vercel `/api/entreprise?q=…`.
- BODACC (API opendatasoft `annonces-commerciales`, champ `registre` = SIREN) :
  aucune annonce « Procédures collectives » (redressement, liquidation,
  sauvegarde) ni « Radiations ».
- Outil : `outils/verif_entreprises.py`.

## 2. Ce que le modèle Dig protège déjà

- **Abonnement mensuel** : un impayé coûte un mois (49 à 79 €). Les conditions
  de vente prévoient la **mise en pause du site** jusqu'au paiement.
- **Gros montants** (achat 690 €, Prestige 1 990 €) : **acompte de 30 à 50 %
  avant de commencer**, solde avant la mise en ligne définitive.
- **Prélèvement SEPA** (mode choisi le 27/09) : avec le mandat classique
  (« CORE »), le payeur peut demander le remboursement **sans justification
  pendant 8 semaines** (Banque de France,
  <https://www.banque-france.fr/fr/a-votre-service/particuliers/mieux-connaitre-moyens-paiement/prelevement-sepa>).
  Mandat « B2B » sans ce droit : *à vérifier* avant de le choisir.

## 3. Si un client ne paie pas, dans l'ordre

1. Relance aimable par email (1 à 2 fois).
2. Mise en demeure par lettre recommandée (date limite + rappel des pénalités).
3. Pénalités légales entre professionnels (Service Public, page vérifiée le
   07/08/2026, <https://entreprendre.service-public.gouv.fr/vosdroits/F23211>) :
   - indemnité forfaitaire de recouvrement : **40 € par facture impayée**,
     une seule fois ;
   - pénalités de retard : taux BCE + 10 points, soit **12,40 %** au
     2ᵉ semestre 2026 (minimum légal : 3 fois le taux d'intérêt légal) ;
   - ces deux mentions **doivent figurer dans les CGV et sur les factures**.
     **Fait le 05/10** : `supports/Dig-CGV.pdf`, `Dig-Modele-devis.pdf`, `Dig-Modele-facture.pdf`
     (générés par `outils/documents_commerciaux.py` ; mentions de facture vérifiées sur F31808, 11/08/2026).
4. Injonction de payer au tribunal de commerce (Service Public,
   <https://entreprendre.service-public.gouv.fr/vosdroits/F38156>) : requête
   en ligne, sans avocat, frais de greffe **33,47 €** ; pas d'audience ; le
   débiteur a **1 mois** pour faire opposition.

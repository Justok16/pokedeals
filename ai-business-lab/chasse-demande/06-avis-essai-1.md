# Analyse d'avis — essai 1 (24/09, ~01:45 UTC)

Réseau ouvert par l'utilisateur. Accès : App Store (recherche iTunes 200,
flux d'avis partiellement 403), Google Play 200, apps.shopify.com 200,
Trustpilot 403 (anti-robot).

**Échantillon** : thèmes « invoice », « appointment booking », « inventory » ;
États-Unis et France ; 8 apps par thème et par boutique. **1 685 avis à 1 ou 2
étoiles.** Source primaire (avis bruts) ; classement par mots-clés, donc
approximatif. Détail : `outils/resume-24-09-essai1.md` (le CSV brut n'est pas
versionné).

| Motif de plainte | Avis | Plus fort sur |
|---|---|---|
| Facturation abusive (prélèvement surprise, résiliation, essai piège) | 323 | facturation : 227 sur 782 (29 %) |
| Fonction manquante ou retirée | 274 | réservation |
| Bugs, synchronisation | 226 | réservation |
| Support absent | 173 | facturation |
| Perte de données | 106 | stock |

## Signal le plus net

Des **petits pros qui utilisaient l'app depuis des années** se retrouvent
**bloqués hors de leurs propres données** par un nouveau mur payant, ou
facturés par surprise. Exemples cités (verbatim abrégé) :
- « utilisée 4 ans, aujourd'hui bloquée par un mur payant, je ne peux plus
  faire de factures » (Invoice Maker) ;
- « impossible de marquer une facture payée sans renouveler à 79 $ »
  (Invoice2go) ;
- Sortly (stock) : « facturé 468 $ sans prévenir » ; « je payais 119 $/mois,
  facturé 5 376 $ pour une offre entreprise dont je n'ai pas besoin ».

## Ce que ça vaut à la grille (provisoire)

- 5, 6 ✓ : les plaignants **paient déjà** et le manque est tracé.
- 8 ✗ à vérifier : des factures gratuites existent (Zoho Invoice, Wave…) ;
  le manque est **la confiance et le prix juste**, pas une fonction. Une
  promesse « vos données restent à vous, prix bloqué » est copiable (point 9).
- Piste la plus concrète à creuser : **stock simple pour petits pros**
  (salons, caves à vin, collectionneurs) fuyant Sortly — à vérifier : taille,
  alternatives, prix.

**Pas encore une opportunité.** Essai volontairement court : la limite
d'utilisation hebdomadaire de l'utilisateur est presque atteinte
(réinitialisation le 28/09 19:00).

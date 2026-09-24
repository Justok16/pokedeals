# Piste B : « lots de produits » pour BigCommerce — grille et test

Choisie par l'utilisateur le 24/09 (« les deux en parallèle » : tester cette
piste et continuer la recherche).

## Pourquoi cette fonction

| Mesure | Shopify | BigCommerce |
|---|---|---|
| Apps « bundle » | 670 | 11 |
| Avis cumulés | 69 718 | 8 |
| Meilleure app | 5,0 sur des milliers d'avis | 4 avis (Integer Bundle Buddy) ; Smart Bundles AI noté 1 |
| Fonction native | Shopify Bundles (2,9/5) | **aucune** (contournement : listes à choix « pick list ») |

Demande visible sur le forum officiel BigCommerce : « Is it possible to
create product bundles », « how do I set up product bundles? »
(support.bigcommerce.com). Sources primaires : nos relevés des deux
boutiques ; secondaires : folio3, avada, modernretail.

## Grille anti-DigCost (25 points)

| # | Constat | État |
|---|---|---|
| 1 ★ | Abonnement mensuel payé par le marchand ; prix de référence Shopify 10 à 30 $/mois ; Bundlebees à 19,99 $/mois sur BigCommerce | ✓ (prix exact à fixer par le test) |
| 2 ★ | Produit à nous | ✓ |
| 3 ★ | Le marchand qui paie est celui qui garde l'app installée | ✓ |
| 4 | 1 500 €/mois ≈ 50 clients à 39 $ ; 10 000 €/mois ≈ 330 clients = 0,9 % des ~37 000 boutiques | exigeant |
| 5 ★ | Preuve de paiement : massive sur Shopify, faible sur BigCommerce (apps payantes sans avis) | **à prouver par le test** |
| 6 ★ | Manque : pas de fonction native, fils du forum, meilleure app à 4 avis | ✓ |
| 7 | Contournement gratuit natif (listes à choix) : partiel, sans gestion du stock des composants | ⚠ |
| 8 ★ | 11 apps, aucune établie | ✓ |
| 9 | Avantage : qualité et gestion du stock des composants ; copiable | ⚠ |
| 10 ★ | Canal sans démarchage : fiche sur la place de marché BigCommerce + réponses publiques aux fils du forum | ✓ (accepté par l'utilisateur le 23/09) |
| 11 | **Commission 20 % du revenu** pour une app publique hors facturation unifiée (contrat partenaire, partie C.3, commerce.com — source primaire). Approbation obligatoire (exigences publiées). Identité : compte développeur et facturation à son nom | ✓ connu |
| 12 | Hébergement nécessaire (serveur, OAuth, webhooks) : Vercel + Supabase déjà utilisés par l'utilisateur, 0 € au départ | ✓ |
| 13 ★ | Faits étiquetés dans ce fichier | ✓ |
| 14 ★ | Risque que BigCommerce ajoute des lots natifs (Shopify l'a fait) | ⚠ moyen |
| 15 ★ | Dépendance totale à BigCommerce, **en recul d'environ 8 %** | ⚠ fort |
| 16 ★ | Coût par client très faible (pas d'IA lourde) ; commission 20 % comprise | ✓ |
| 17 | Usage continu tant que la boutique vend des lots | ✓ |
| 18 | Ni trop tôt ni trop tard ; plateforme mûre | ✓ |
| 19 ★ | Aucun secteur à risque | ✓ |
| 20 | Support : les bugs de stock des lots génèrent des tickets (voir avis Bundles.app sur Shopify) | ⚠ |
| 21 | Les marchands installent couramment des apps d'éditeurs inconnus | ✓ |
| 22 | Aucun | ✓ |
| 23 | Micro-SaaS revendable (places de cession de type Acquire) | ✓ |
| 24 | Petit marché : plafond réaliste de l'ordre de 10 000 $/mois | ⚠ |
| 25 | **Meilleure raison d'échouer** : BigCommerce se recentre sur les grands comptes, qui font développer leurs lots par des agences ; la longue traîne qui achèterait une app à 39 $ s'en va. | à mesurer |

**Bilan : aucun point éliminatoire en échec ; trois fragilités (5, 15, 25).**
Le point 5 se tranche par un test, avant toute construction.

## Test avant construction (ordre imposé, étape 2)

1. Une page : ce que fait l'app, **prix affiché (39 $/mois, 14 jours
   d'essai)**, bouton « Me prévenir au lancement » (adresse email).
2. Diffusion sans démarchage : réponses publiques, sous pseudonyme, aux fils
   du forum BigCommerce qui demandent des lots — avec la solution native
   gratuite expliquée d'abord, le lien ensuite.
3. **Seuil de décision à 21 jours : 15 inscriptions de marchands BigCommerce
   = construire ; moins de 5 = abandonner la piste.** Entre les deux :
   prolonger de 14 jours.

À faire par l'utilisateur (le reste par Claude) : valider le nom et le
prix ; créer le formulaire d'inscription (outil gratuit, à choisir) ;
publier les réponses sur le forum.

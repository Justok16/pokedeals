## Session du 08/10/2026 — audit restocks FR et correctifs ciblés

Mandat : six produits 30e anniversaire FR, vendeurs français uniquement,
alertes Telegram sans achat, identité HTTP honnête et <= 1 départ/s/site.

- Shopify : disponibilité/prix/langue/lien évalués sur la variante retenue.
  Une fiche UPC Mentali/Noctali ne partage plus le stock des personnages.
  Champs disponibles absents/non booléens restent indéterminés.
- Woo Store API : un ID renvoyé par la recherche d’un autre personnage est
  comparé à TOUS les produits suivis avant déduplication. Un produit
  is_purchasable=False n’est pas déclaré commandable.
- Transport du radar uniquement : SessionRadarPolie impose une identité
  PokeDealsRestock et >=1s entre départs par hôte dans le processus.
  Les connecteurs historiques hors radar ne sont pas modifiés.
  La coordination entre runners distincts reste une limite explicite.
- Liste complément manuelle indépendante des fichiers générés : etw-tcg.com
  (SIRET déclaré 99367661800016), lorenzone.fr (93444064500018).
  Endpoints products.json et fiches .js HTTP 200 avec UA honnête ;
  notices légales et pages CGV consultées. Outpost Bruxelles exclu du
  complément car vendeur belge, même s’il vend des cartes FR.
- Recherche : UltraJeux ETB en livraison ; La Grande Récré bundle lisible
  directement en JSON-LD malgré recherche inutilisable ; Woo Store API
  UPC-TCG et PixelHeart publiques. PixelHeart réutilise un même EAN pour
  trois produits différents : ne pas enregistrer cet EAN comme alias.
- Foxchip : recherche interdite par robots.txt, ne pas l’intégrer.
  Fiche produit lisible mais offers absent : stock structuré indéterminé.
- Tradingcardsxxx bundle réservé VIP/REGULAR : available ne garantit pas
  l’éligibilité de l’acheteur. Mini Tins UltraJeux : magasin seulement.
- Tests : 816 passent, dont 15 nouveaux tests ; git diff --check propre.

Restent à traiter : voie rapide sur fiches connues, verrou partagé entre
runners pour les sites communs, émission dès fin de chaque boutique,
identifiants GTIN validés et variante/langue/vendeur, dates de livraison
séparées des dates de sortie, couverture FR des annuaires automatiques,
synthèse initiale pour les stocks déjà ouverts, watchdog en minutes.
Aucune hausse globale de cadence, aucun abonnement payant, aucun achat.

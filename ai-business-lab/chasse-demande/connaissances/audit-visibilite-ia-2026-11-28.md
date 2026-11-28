# Audit de visibilité IA de dig16.fr (28/11/2026)

Demande de l'utilisateur du 28/11 (« oui audit IA »). Méthode : skill `ai-seo`, lecture de robots.txt, llms.txt,
données structurées et sitemap ; 4 recherches Firecrawl (France) et 2 recherches Tavily (moteur utilisé par des
assistants IA). Essai d'interroger Gemini avec la recherche Google : refusé (accès 401), donc les réponses de l'IA
de Google n'ont pas pu être lues directement.

## Ce qui va bien
- robots.txt : tout est ouvert aux moteurs et aux IA (Content-Signal search, ai-input, ai-train = yes).
- llms.txt présent, à jour (formules et prix), sans Instagram.
- Données structurées : Organization + ProfessionalService, OfferCatalog (4 offres), FAQPage (22 questions).
- Recherche du nom « DIG16 » : 10 résultats sur 10 sont à DIG16 (site, Facebook, PagesJaunes, YouTube, Charente Libre, mairie de Ruffec).
- Recherche « site internet artisan Ruffec » : DIG16 présent 4 fois dans le top 6 (groupe Facebook, mairie de Ruffec, PagesJaunes, page Charente du site).
- Tavily « site internet artisan Charente abonnement 49 € » : la page Facebook DIG16 arrive en 1re position.

## Ce qui manque
- « création site internet artisan Charente » et « prix site internet artisan abonnement Charente » : DIG16 absent du top 10
  (agences d'Angoulême et de Charente-Maritime, guides de prix). Site ouvert depuis le 09/10 : peu de liens venant d'autres sites.
- Aucune date « mis à jour le » visible sur les pages ; seul le guide porte une date dans ses données (12/11).
- Une ancienne publication Instagram indexée dit « en ligne en 7 jours » (affirmation périmée) : elle disparaîtra avec le compte désactivé.

## Corrections proposées (à valider par l'utilisateur, rien n'est changé sans accord)
1. Afficher « Mis à jour le … » (date réelle) sur l'accueil, le guide et la page Charente.
2. Ajouter au guide une courte réponse chiffrée « Combien coûte un site internet pour un artisan en 2026 ? » avec des sources publiques datées (format repris par les IA).
3. Obtenir des mentions sur d'autres sites (gratuites, sans achat de liens) : annuaire d'Atout Ruffec, annuaire des entreprises de Val de Charente, fiche CCI ; et les premiers avis Google dès le premier client (jamais d'avis payé, inventé ou trié : `67`).

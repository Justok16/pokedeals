# Synthèses détaillées des chaînes (04/10/2026)

Chaîne de fabrication des documents `connaissances/<chaîne>/SYNTHESE-DETAILLEE.md` et `.pdf` :

1. regrouper les fiches par thème dans des fichiers `<chaîne>__<thème>.txt` (mots-clés sur le titre et la thèse) ;
2. `lancer.py` : une synthèse par thème via le relais `/api/avis` (Gemini gratuit ; variable MODELES pour changer de modèles quand un quota est épuisé) ;
3. `nettoyer.py` : retire les identifiants de vidéos inventés, corrige l'indentation des listes ;
4. `assembler.py` : ajoute en tête l'essentiel rédigé à la main (`intro_<chaîne>.md`), les règles officielles vérifiées et les chiffres périmés, puis produit Markdown, HTML et PDF.

À refaire quand une chaîne a beaucoup de nouvelles vidéos, et revérifier les règles officielles à la source (service-public.fr) à chaque fois.

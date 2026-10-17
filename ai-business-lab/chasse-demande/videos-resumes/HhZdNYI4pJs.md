# HhZdNYI4pJs — « I Tried 100+ Github Repos for Claude. These 6 Are the Best »

- Auteur : Nate Herk ; lien : https://youtu.be/HhZdNYI4pJs
- Envoyée par l'utilisateur le 15/10/2026 ; résumée le 15/10 par Gemini (gemini-3.1-flash-lite, via le relais)

### 1) Idée principale
L'auteur explique qu'il existe des milliers de dépôts GitHub pour Claude, mais que la plupart sont inutiles. Il présente une sélection de 10 outils optimisés pour automatiser des tâches complexes pour des clients (édition vidéo, gestion de données, création de sites web) afin de transformer ces outils "gratuits" en services payants pour les entreprises. Le message clé est de **se concentrer sur la résolution d'un problème client concret** plutôt que sur la technologie elle-même.

---

### 2) Liste des outils et dépôts
*   **Hyperframes (Heygen) :** Gratuit (open-source). Sert à créer des vidéos (captions, sous-titres, motion design) à partir d'instructions en langage naturel.
*   **Google Workspace CLI :** Nécessite une configuration avec un projet Google Cloud (gratuit). Permet à Claude de manipuler Drive, Gmail, Docs, etc., via une ligne de commande.
*   **Apify (MCP Server) :** Modèle hybride (certains scrappers sont gratuits, d'autres sont payants au volume). Sert à scraper des sites web (Instagram, Reddit, etc.) que Claude ne peut pas lire nativement.
*   **Scroll Craft :** Gratuit (créé par l'auteur). Permet de créer des sites web immersifs avec des effets de défilement ("scroll") avancés.
*   **Humanizer :** Gratuit (open-source). Réécrit le contenu pour qu'il ne ressemble pas à du texte généré par IA ("IA slop").
*   **Agent Skills (Addy Osmani) :** Gratuit. Aide à structurer le flux de travail de Claude (spécifications, plan, construction) pour éviter la perte de contexte dans les longs projets.
*   **Expo Official Skills :** Gratuit. Outil pour développer des applications mobiles (iOS/Android) avec Claude.
*   **Supabase / Stripe (Skills) :** Gratuit (pour les skills, mais les services sous-jacents sont payants selon l'usage). Permet de gérer les bases de données et les paiements sécurisés pour vos applications.
*   **Playwright CLI :** Gratuit. Permet d'ouvrir un navigateur réel pour tester et valider automatiquement les fonctionnalités d'une application avant de la livrer.
*   **Open SEO :** Gratuit (avec des limites de crédit). Fournit des données réelles sur les mots-clés, backlinks et classements pour des optimisations SEO concrètes.

---

### 3) Astuces concrètes et réutilisables
*   **Vente de "Packages" de contenu :** Ne vendez pas l'utilisation de l'outil, vendez le résultat (ex: "20 clips sous-titrés par mois" pour une salle de sport).
*   **Standardisation :** Utilisez l'outil *Agent Skills* pour découper les projets en tâches, ce qui rassure le client sur la progression.
*   **Sécurité et Test :** Utilisez *Playwright* pour valider visuellement que le site fonctionne avant de montrer le résultat au client.
*   **Gestion des coûts :** Ne vous précipitez pas à installer tous les plugins au début ; installez uniquement celui qui résout le problème immédiat du projet en cours pour éviter les bugs et les coûts inutiles.
*   **La règle des trois :** Pour rendre vos contenus plus "humains", utilisez le *Humanizer* pour ajuster vos textes (éviter les structures répétitives et les mots trop marketing).

---

### 4) Chiffres de revenus (affirmés par l'auteur)
*   **Abonnement développeur Apple :** 99 $ / an.
*   **Apify (Starter) :** 19 $ / mois (pay-as-you-go).
*   **Open SEO (Usage moyen estimé) :** 10 $ / mois.
*   **Les revenus générés auprès des entreprises :** Non précisés (l'auteur explique que vous vendez un service, le prix dépend donc de votre négociation avec le client).
*   **Économies annoncées par les outils (ex: Caveman, RTK, etc.) :** L'auteur souligne que les économies de "tokens" promises par certains outils sont souvent surestimées (entre 0 % et 10 % d'économie réelle constatée contre des promesses de 20 % à 65 %).

## Tri DIG16 (15/10/2026)

**Déjà en place** : ScrollCraft (`site-dig/moteur/scrollcraft.min.js`), skill `humanizer`, Playwright (`outils/test_pages.py` + test automatique GitHub), OpenSEO (connecteur), Google Drive/Gmail/Agenda (connecteurs), plan avant construction (plugin Superpowers, grille `00`). **Déjà appliqué** : DIG16 vend un résultat (un site en ligne en 7 jours, suivi mensuel), pas une technique. **Écarté** : Apify (payant au volume ; Firecrawl et Playwright suffisent), Expo (applications mobiles, hors sujet), Supabase/Stripe (pas de base de données ni de paiement en ligne sur nos sites ; prélèvements par GoCardless), HyperFrames (vidéo, réseaux en pause).

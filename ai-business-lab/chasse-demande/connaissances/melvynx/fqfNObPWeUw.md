# Création d'un backend Express + SQLite + Node.js et fetch côté frontend

Vidéo : https://youtu.be/fqfNObPWeUw · durée 35:08 · résumé Gemini (gemini-flash-lite-latest, lot de 8) du 2026-10-13
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1. **Idée principale :** Tutoriel complet pour créer un serveur backend Node.js (avec Express et SQLite) et une application frontend JavaScript interagissant avec ce serveur via l'API fetch.
2. **Outils, sites ou dépôts GitHub cités :**
   - **Node.js :** Gratuit, environnement d'exécution JavaScript.
   - **Express :** Gratuit, framework pour application web Node.js.
   - **SQLite :** Gratuit, système de gestion de base de données.
   - **Visual Studio Code (VS Code) :** Gratuit, éditeur de code.
   - **Nodemon :** Gratuit, outil de redémarrage automatique du serveur Node.
   - **SQLite3 (package npm) :** Gratuit, driver SQLite pour Node.
   - **Body-parser (package npm) :** Gratuit, middleware pour parser le corps des requêtes HTTP.
   - **Bookeeper Studio :** Gratuit (ou freemium), outil pour visualiser et gérer des bases de données SQLite.
3. **Astuces concrètes et réutilisables :**
   - Structurer un projet Node.js avec `npm init` et installer Express.
   - Configurer un serveur avec `app.listen` et définir des routes GET et POST avec Express.
   - Initialiser et exécuter des requêtes SQL (création de table, insertion) avec SQLite dans un module dédié (`db.js`).
   - Utiliser `body-parser` (ou `app.use(express.json())`) pour récupérer les données JSON envoyées dans les requêtes POST.
   - Configurer `cors` pour autoriser les requêtes cross-origin si le frontend et le backend sont sur des ports différents.
   - Récupérer les données depuis le frontend en JavaScript avec `fetch` et afficher dynamiquement les éléments dans le DOM (`document.createElement`).
4. **Chiffres de revenus annoncés :** Non précisé.

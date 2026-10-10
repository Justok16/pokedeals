# Pourquoi je n'utilise pas CREATE-REACT-APP (et tu devrais aussi)

Vidéo : https://youtu.be/PlIJSUkufuk · durée 13:17 · résumé Gemini (gemini-3.1-flash-lite-preview) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé de la vidéo, orienté sur votre recherche d'optimisation du développement :

### 1) Idée principale
L'auteur explique pourquoi le traditionnel `create-react-app` (CRA) est devenu obsolète et inefficace pour les développeurs React modernes. Il préconise l'utilisation de **Vite** comme outil de construction ("build tool"), car il est beaucoup plus léger, rapide et flexible. L'idée est d'optimiser radicalement le flux de travail (temps de chargement, configuration, maintenance) pour gagner en productivité.

### 2) Outils et ressources cités
*   **Vite JS :** Gratuit (open-source). C'est un outil de développement frontend qui remplace les "bundlers" traditionnels comme Webpack pour offrir des serveurs de développement instantanés et des builds plus rapides.
*   **Create React App (CRA) :** Gratuit. Outil historique pour créer des applications React, critiqué ici pour sa lourdeur et ses nombreuses dépendances inutiles.
*   **Vite-plugin-react-md :** Gratuit. Plugin pour Vite permettant d'afficher des fichiers Markdown en tant que composants React.
*   **Vite-plugin-ssr :** Gratuit. Plugin pour Vite facilitant le rendu côté serveur (SSR) de manière simplifiée.
*   **BeginReact.dev :** Plateforme de formation (payante). C'est le site personnel de l'auteur où il enseigne le développement React avec sa propre méthodologie.
*   **Idraw.js :** Gratuit. Site utilisé par l'auteur pour schématiser les concepts techniques (SSR vs CSR) lors de sa présentation.

### 3) Astuces concrètes et réutilisables
*   **Abandonner les outils "tout-en-un" lourds :** Privilégiez des outils modulaires comme Vite qui vous permettent de n'ajouter que les fonctionnalités (plugins) dont vous avez réellement besoin.
*   **Comprendre le Rendu (SSR vs CSR) :** L'auteur souligne l'importance de choisir le bon type de rendu. Le *Client-Side Rendering* (CSR) impose un temps de chargement vide ("loader") initial, alors que le *Server-Side Rendering* (SSR) permet un affichage immédiat, ce qui est crucial pour l'expérience utilisateur et le SEO.
*   **Optimiser les dépendances :** En passant de `create-react-app` à `Vite`, vous réduisez drastiquement le poids du dossier `node_modules` (l'auteur passe de 324 Mo à 41 Mo), ce qui accélère l'installation et réduit les risques de vulnérabilités logicielles.
*   **Le Hot Module Replacement (HMR) :** Utilisez Vite pour voir vos modifications de code apparaître en temps réel dans le navigateur de manière quasi instantanée (gain de temps significatif sur le développement itératif).

### 4) Chiffres de revenus
*   **Revenus annoncés :** Non précisé.
*   La vidéo ne porte pas sur le gain d'argent direct, mais sur l'optimisation de la productivité technique du développeur.

***Note sur Claude Code :*** *Bien que vous mentionniez Claude Code dans votre requête, cet outil n'est pas mentionné dans la vidéo. L'auteur se concentre exclusivement sur l'écosystème React et l'outillage de build (Vite vs Webpack).*

# Créer une Application sur iPad c'est POSSIBLE ? NON.

Vidéo : https://youtu.be/LagNorf_6JI · durée 25:59 · résumé Gemini (gemini-flash-lite-latest, lot de 9) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** L'auteur relève le défi de créer une application de dessin collaborative uniquement sur iPad, de la coder directement dans le cloud via GitHub Codespaces, et de la déployer sur Vercel, tout en surmontant les difficultés liées à l'absence d'ordinateur et de port USB.
2) **Outils, sites ou dépôts GitHub cités :**
- **iPad** (non précisé) : Tablette utilisée comme support unique pour tout faire.
- **GitHub Codespaces** (gratuit jusqu'à 60 heures par mois) : Environnement de développement hébergé dans le cloud pour coder en ligne.
- **React** (non précisé) : Framework JavaScript utilisé pour l'application.
- **Vite** (non précisé) : Outil de build pour l'application React.
- **Realtime Colors** (`realtimecolors.com`) (non précisé) : Site web pour visualiser et choisir des palettes de couleurs et polices.
- **Liveblocks** (non précisé) : Service pour ajouter des fonctionnalités de collaboration en temps réel (« live collaboration » / Liveblocks docs) dans l'application React.
- **Vercel** (non précisé) : Service d'hébergement et de déploiement de l'application web.
- **Visual Studio Code / VS Code** (non précisé) : Éditeur de code utilisé dans Codespaces.
3) **Astuces concrètes et réutilisables :**
- Utiliser GitHub Codespaces pour coder directement depuis une tablette (iPad) sans nécessiter de configuration locale lourde, en profitant du quota gratuit de 60 heures par mois.
- Utiliser un générateur de template React (via Vite) pour initialiser rapidement une application fonctionnelle dans le cloud.
- Utiliser le site `realtimecolors.com` pour choisir rapidement des harmonies de couleurs et les intégrer dans un design web avec des bordures et des fonds contrastés.
- Utiliser la bibliothèque **Liveblocks** pour mettre en place facilement une expérience collaborative en temps réel (présence, curseurs partagés, etc.) sur une application React.
- Gérer les coordonnées de la souris et du stylet (`Apple Pencil`) sur un élément HTML `Canvas` en soustrayant le décalage (`offsetLeft`, `offsetTop`) pour obtenir des tracés précis.
4) **Chiffres de revenus annoncés :** Non précisé.

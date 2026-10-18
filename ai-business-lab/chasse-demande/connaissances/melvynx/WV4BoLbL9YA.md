# Tuto NextJS : Création d’une App avec OpenAI de A à Z

Vidéo : https://youtu.be/WV4BoLbL9YA · durée 50:36 · résumé Gemini (gemini-flash-lite-latest, lot de 9) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Tutoriel complet pour intégrer l'API OpenAI (ChatGPT) dans une application web moderne (Next.js avec Tailwind CSS et DaisyUI), en expliquant comment configurer l'API, gérer les requêtes en mode normal ou en streaming, et créer un générateur de code Tailwind interactif.
2) **Outils, sites ou dépôt GitHub cités :**
- **OpenAI API** : service payant d'intelligence artificielle.
- **Next.js** : framework React (gratuit).
- **Tailwind CSS** : framework CSS (gratuit).
- **DaisyUI** : bibliothèque de composants pour Tailwind CSS (gratuit).
- **Vercel AI SDK** (`ai` / `@vercel/ai`) : bibliothèque npm (gratuit) pour intégrer des fonctionnalités de streaming et de chat IA.
- **Visual Studio Code** : éditeur de code (gratuit).
- **Escalidraw** : outil de schéma (gratuit).
3) **Astuces concrètes et réutilisables :**
- Initialiser un projet Next.js avec Tailwind et TypeScript via la commande `pnpm create next-app@latest`.
- Installer et configurer DaisyUI comme plugin dans `tailwind.config.js` pour styliser rapidement l'interface.
- Créer une route API dans Next.js (`app/api/tailwind/route.ts`) pour gérer les requêtes POST vers l'API OpenAI.
- Configurer la clé secrète OpenAI dans un fichier `.env.local` (`OPENAI_API_KEY`) et l'ajouter au `.gitignore` pour des raisons de sécurité.
- Utiliser le mode **Streaming** (`stream: true` ou le SDK Vercel AI avec `StreamingTextResponse`) pour afficher le texte généré par l'IA mot à mot en temps réel (« type effect »), améliorant considérablement l'expérience utilisateur par rapport au mode normal (bloc entier).
- Structurer les prompts avec des rôles distincts (`system`, `user`, `assistant`) pour guider précisément le comportement de l'IA (ex: « Write only Tailwind code in response »).
- Utiliser le package `ai` et `useCompletion` côté front-end pour connecter l'interface utilisateur à la route API et afficher dynamiquement le code ou le HTML généré.
4) **Chiffres de revenus annoncés :**
- **5 $** : montant de crédit gratuit offert par OpenAI lors de la création d'un compte.

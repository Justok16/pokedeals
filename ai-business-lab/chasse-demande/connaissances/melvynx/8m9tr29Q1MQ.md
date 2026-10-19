# Découverte : L'intégration de TanStack AI

Vidéo : https://youtu.be/8m9tr29Q1MQ · durée 1:30 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-19
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** :
Le créateur présente la sortie du kit SDK open-source « TanStack AI » par TanStack, conçu comme une alternative modulaire et agressivement typée (TypeScript) aux SDK d'IA existants (comme celui de Vercel), facilitant l'intégration multi-fournisseur dans les applications web.

2) **Outils, sites ou dépôts GitHub cités** :
- **TanStack AI SDK (`@tanstack/ai`)** : outil open-source (gratuit), sert de SDK unifié pour intégrer des API d'IA (OpenAI, Anthropic, Gemini, etc.) dans différents frameworks web.
- **Next.js / Express / Remix** : frameworks web (gratuits), servent de socles pour exécuter des applications.
- **Vercel** : plateforme et créateur de l'AI SDK concurrent (gratuit/payant), mentionné comme référence existante.

3) **Astuces concrètes et réutilisables** :
- Utiliser `toolDefinition` pour déclarer les outils (inputs et outputs schématiques) et associer des actions exécutables par le LLM de manière sécurisée et typée.
- Configurer un serveur d'API de chat compatible avec le hook `useChat` côté front-end (React) pour récupérer les réponses en streaming de manière fluide.

4) **Chiffres de revenus annoncés (affirmés par l'auteur)** :
- Chiffres de revenus : non précisés.

---

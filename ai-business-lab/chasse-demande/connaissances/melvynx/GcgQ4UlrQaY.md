# VLOG : Création d’une app React Native avec Claude Code A à Z

Vidéo : https://youtu.be/GcgQ4UlrQaY · durée 28:32 · résumé Gemini (gemini-flash-lite-latest, lot de 6) du 2026-10-11
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Le créateur explique comment il a utilisé l’outil d'IA **Claude Code** pour coder et lancer rapidement une application mobile iOS native (pour son service *SaveIt.now*) en partant de zéro, de manière assistée par l'intelligence artificielle, sans savoir coder à l'origine en React Native.

2) **Outils, sites et dépôts GitHub cités :**
*   **Claude Code :** Outil d'IA (mentionné comme gratuit ou utilisé via son intégration) pour générer du code, créer des fichiers de plans, configurer Metro pour monorepo, configurer l'authentification avec *Better Auth*, etc.
*   **SaveIt.now :** Le produit/service SaaS du créateur (payant ou freemium selon le service, non précisé en détail).
*   **Tamagui UI (`tamagui.dev`) :** Librairie UI cool en React Native pour les thèmes et composants (statut non précisé explicitement payant/gratuit, vraisemblablement open-source/gratuit).
*   **Neon (`neon.tech`) :** Fournisseur de base de données / documentation / service cloud (statut non précisé).
*   **Expo / React Native :** Frameworks de développement mobile (gratuits/open-source).
*   **App Store Connect / TestFlight :** Plateformes d'Apple pour publier et tester l'application mobile (gratuites pour les développeurs enregistrés).
*   **GitHub / Gist :** Plateforme de code (non précisé si payant ou gratuit, version standard utilisée).
*   **Now TS (`now.ts` / `mlv.sh/ai`) :** Sponsor de la vidéo, plateforme de formation pour devenir un "développeur 10x" (payant / masterclass payante ou abonnements mentionnés via un lien de parrainage).
*   **Masterclass IA / Blueprint (`ai-blueprint.dev`) :** Masterclass du créateur pour expliquer comment utiliser Claude Code (payant via la promotion).

3) **Astuces concrètes et réutilisables :**
*   Demander à Claude Code de créer d'abord un fichier Markdown de plan (ex: `explore-plan-code-test` ou plan d'intégration Expo) avant de modifier directement le code, ce qui permet de structurer les étapes et de garder un fil conducteur modifiable.
*   Utiliser des "web searches" itératives et demander à l'outil de lire la documentation officielle (comme celle de *Better Auth* ou d'Expo) pour configurer l'authentification et les routes correctement.
*   Configurer les en-têtes CORS dans les middlewares du serveur Next.js pour autoriser les appels d'API depuis les extensions, le web et les applications mobiles iOS (liens profonds/deep links).
*   Laisser Claude Code générer et corriger les erreurs de compilation de manière itérative en lui fournissant les logs d'erreurs textuels du terminal.
*   Pour les modifications mineures (comme l'ajout d'une fonction *pull-to-refresh* avec React Query), donner des instructions précises de configuration en ciblant des blocs de code spécifiques.

4) **Chiffres de revenus annoncés (« affirmé par l'auteur ») :**
*   *Non précisé.*

---

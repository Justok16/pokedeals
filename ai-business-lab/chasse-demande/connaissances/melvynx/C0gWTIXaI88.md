# Créer un gestionnaire de dialog Avec Now.ts

Vidéo : https://youtu.be/C0gWTIXaI88 · durée 1:59 · résumé Gemini (gemini-flash-lite-latest, lot de 5) du 2026-10-19
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Présentation d'un wrapper de dialogue et d'un gestionnaire de dialogues (`DialogManager`) permettant de générer des fenêtres modales de confirmation et des alertes complexes avec un minimum de lignes de code.
2) **Outils, sites ou dépôts cités :**
- **NaotS** (ou `naots.app.fr`) : Boilerplate ou ressource de l'auteur intégrant ces fonctionnalités.
- **Zustand** : Librairie de state management (gratuite) utilisée pour gérer l'état global des dialogues.
3) **Astuces concrètes et réutilisables :**
- Créer un `DialogManager` basé sur Zustand pour centraliser l'affichage des dialogues, des actions et des conditions dans toute l'application.
- Utiliser des fonctions de test et de validation pour s'assurer que le code de dialogue fonctionne correctement avant le rendu dans le layout via un renderer global.
4) **Chiffres de revenus :** Non précisé.

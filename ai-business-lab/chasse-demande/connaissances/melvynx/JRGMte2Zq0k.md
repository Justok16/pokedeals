# TUTO/COURS sur Zustand avec React

Vidéo : https://youtu.be/JRGMte2Zq0k · durée 42:05 · résumé Gemini (gemini-flash-lite-latest, lot de 2) du 2026-10-16
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** La vidéo présente la bibliothèque **Zustand** comme un gestionnaire d'état léger, performant et simple d'utilisation pour React, en le comparant au Context API et à Redux, tout en démontrant son intégration dans un panier d'achat avec gestion des favoris, des toasts et de la persistance des données.

2) **Outils, sites ou dépôts GitHub cités :**
- **Zustand :** (gratuit / open-source) Bibliothèque légère de gestion d'état pour React, alternative plus simple et plus performante à Redux ou au Context API.
- **Redux Toolkit :** (gratuit / open-source) Bibliothèque de gestion d'état plus lourde comparée à Zustand (dont la taille du bundle est environ 10 fois supérieure).
- **GitHub :** (gratuit) Plateforme d'hébergement de code source permettant de consulter la documentation et le code source de Zustand.
- **Lucide React :** (gratuit / open-source) Bibliothèque d'icônes utilisée pour les boutons (ex. étoiles, caddies).
- **Radix UI / Sonner :** (mentionnés comme alternatives ou composants de toast) Bibliothèques de composants et de notifications (toasts) pour React.

3) **Astuces concrètes et réutilisables :**
- Utiliser Zustand en dehors des composants React pour créer un store global indépendant, ce qui évite les re-renders inutiles et simplifie grandement le code par rapport au Context API.
- Utiliser `useShallow` (ou `useStore` avec un sélecteur) pour éviter les re-renders superflus lorsque l'état d'un objet ou d'un tableau change, en s'abonnant uniquement aux propriétés nécessaires.
- Intégrer le middleware `persist` de Zustand pour sauvegarder et synchroniser automatiquement l'état du store (ex. le panier) avec le stockage local (LocalStorage) sans configuration complexe.

4) **Chiffres de revenus annoncés :**
- Non précisé.

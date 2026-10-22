# Comment debug une application React comme un Senior Développeur

Vidéo : https://youtu.be/jiDW-o7gZaU · durée 14:36 · résumé Gemini (gemini-flash-lite-latest, lot de 6) du 2026-10-15
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Ce tutoriel explique comment utiliser les outils de développement React (React DevTools) pour analyser les performances, inspecter l'arbre des composants, comprendre les rendus et optimiser une application React.

2) **Outils, sites ou dépôts GitHub cités** :
   - **Google** : Gratuit, moteur de recherche pour trouver l'extension.
   - **Chrome Web Store** : Gratuit, plateforme de téléchargement de l'extension Chrome.
   - **React Developer Tools (React DevTools)** : Gratuit, extension de navigateur pour inspecter et profiler les applications React (plus de 4 millions d'utilisateurs).
   - **React** : Gratuit, bibliothèque JavaScript.
   - **Next.js** : Gratuit, framework React mentionné dans un exemple.
   - **Lucide** : Gratuit (ou bibliothèque d'icônes open source), mentionné via une dépendance d'icônes.
   - **mlv.sh/react** : Gratuit (lien fourni par l'auteur), plateforme d'exercices et de formation sur React.

3) **Astuces concrètes et réutilisables** :
   - Installer **React DevTools** depuis le Chrome Web Store et utiliser le bouton d'extension (qui s'allume en bleu sur les pages React en mode production) pour inspecter les composants.
   - Utiliser l'onglet **Components** pour visualiser l'arbre des composants, inspecter les `props`, les `hooks` (comme `useState` ou `useEffect`) et modifier les états en direct pour tester le comportement de l'application.
   - Utiliser l'onglet **Profiler** (en cliquant sur le bouton d'enregistrement) pour analyser les rendus (`renders`), identifier quels composants se re-rendent et mesurer leur durée en millisecondes afin de repérer les goulots d'étranglement.
   - Activer dans les paramètres (Settings) l'option « Highlight updates when components render » pour visualiser visuellement (via des flashs de couleur) les composants qui se re-rendent lors des interactions.
   - Utiliser le bouton flèche (Inspect) pour sélectionner un élément dans la page et retrouver directement son composant associé dans l'arbre DevTools.
   - Utiliser le bouton source (icône de fichier) pour afficher directement le code source d'un composant sélectionné.

4) **Chiffres de revenus annoncés** : Non précisé.

---

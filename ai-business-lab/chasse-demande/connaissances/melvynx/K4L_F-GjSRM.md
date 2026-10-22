# 5 PRINCIPES REACT: Ne rate plus tes entretiens !

Vidéo : https://youtu.be/K4L_F-GjSRM · durée 10:12 · résumé Gemini (gemini-flash-lite-latest, lot de 5) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** L'auteur démystifie 5 principes fondamentaux de React souvent mal compris (le JSX, les rendus/renders, le DOM virtuel/reconciliation, les useEffect/cleanup, et la gestion du DOM par React) afin d'améliorer la productivité, d'éviter les optimisations inutiles et de progresser dans le développement web.
2) **Outils, sites ou dépôts GitHub cités :**
- **Prettier** (gratuit, formateur de code en ligne) ;
- **BeginReact / Masterclass** (cours d'une heure gratuit sur le JSX et le ReactDOM, avec bonus interactifs, lien en description) ;
- **Codesandbox** (utilisé pour des exemples de code interactifs en direct).
3) **Astuces concrètes et réutilisables :**
- Considérer le JSX uniquement comme du "sucre syntaxique" qui se transforme en JavaScript pur (`React.createElement`).
- Ne pas chercher à optimiser les renders de manière prématurée ; la réconciliation et le snapshot de React permettent de synchroniser l'état (state) avec l'interface (UI) de façon optimale sans code superflu.
- Ne pas s'inquiéter du fonctionnement interne de ReactDOM, car React s'en charge.
- Distinguer la phase de synchronisation (le code principal du `useEffect`), la fonction de retour (cleanup pour la déconnexion) et les dépendances pour éviter les bugs.
- Laisser React piloter le DOM et ne jamais utiliser de manipulations directes comme `querySelector` ou modifier les styles via des références (`ref`).
4) **Chiffres de revenus annoncés :**
- Non précisé.

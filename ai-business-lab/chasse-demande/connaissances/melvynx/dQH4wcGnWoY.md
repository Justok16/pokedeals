# N'utilise pas de DEFAULT EXPORT en JavaScript, sauf pour...

Vidéo : https://youtu.be/dQH4wcGnWoY · durée 6:51 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-19
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Pourquoi l'utilisation des *default exports* (`export default`) dans le code JavaScript/TypeScript est déconseillée au profit des *named exports* (exports normés) afin d'éviter les erreurs d'importation, les incohérences de nommage et les problèmes de maintenance.

2) **Outils, sites ou dépôts GitHub cités :**
- *VS Code* (Éditeur de code) : Gratuit. Utilisé pour l'écriture du code, la démonstration des erreurs de renommage et l'utilisation du tooling.
- *Next.js* (Framework React) : Gratuit. Mentionné comme exemple où les `export default` sont parfois requis pour les pages (`pages/` ou `app/`), mais où il faut limiter leur usage ailleurs.
- *Notion* (Application de prise de notes) : Gratuit / payant. Utilisé pour héberger la mindmap récapitulative des extensions et conseils.

3) **Astuces concrètes et réutilisables :**
- Préférer les *named exports* (ex: `export function NomDuComposant()`) plutôt que les `export default` pour permettre à l'IDE de détecter automatiquement les erreurs de renommage et de faciliter le refactoring.
- Éviter d'importer des composants avec des noms incohérents par rapport à leur fichier d'origine, ce qui réduit la lisibilité de la codebase sur le long terme.

4) **Chiffres de revenus annoncés :**
- Non précisé.

---

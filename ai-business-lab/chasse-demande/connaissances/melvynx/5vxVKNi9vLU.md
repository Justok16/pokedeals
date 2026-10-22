# Je teste Tanstack/Form pour la première fois (killer de react-hook-form ?)

Vidéo : https://youtu.be/5vxVKNi9vLU · durée 23:25 · résumé Gemini (gemini-flash-lite-latest, lot de 8) du 2026-10-12
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :**
L'auteur compare différentes bibliothèques de gestion de formulaires en React (notamment React Hook Form face au nouveau TanStack Form), détaille l'installation et l'implémentation de TanStack Form avec Zod, et souligne son orientation vers la scalabilité et le typage strict TypeScript.

2) **Outils, sites, dépôts GitHub et services cités :**
* **TanStack Form** (gratuit/open source) : Nouvelle bibliothèque de gestion de formulaires headless, performante et type-safe pour TS/JS, React, Vue, Angular, Solid et Lit.
* **React Hook Form** (gratuit/open source) : Bibliothèque historique de formulaires pour React.
* **TanStack Router / Query / Table / Virtual / Ranger / Start** (gratuit/open source) : Autres bibliothèques de l'écosystème TanStack.
* **Zod** (gratuit/open source) : Bibliothèque de validation de schémas.
* **React** (gratuit/open source) : Bibliothèque JavaScript.
* **GitHub** (gratuit) : Plateforme de code source.
* **Prisma** (gratuit/open source) : ORM (mentionné dans le projet de test).
* **Next.js** (gratuit/open source) : Framework React (utilisé dans l'application de démonstration).
* **Shadcn/UI** (gratuit/open source) : Bibliothèque de composants UI (mentionnée pour les composants visuels).
* **Lien de formation payant de l'auteur :** `mlv.sh/mlv.sh/react` (mentionné à la fin de la vidéo).

3) **Astuces concrètes et réutilisables :**
* Utiliser `createFormHookContext` ou `useAppForm` pour factoriser la création de formulaires et réduire le code répétitif (boilerplate) dans l'application.
* Intégrer un validateur comme Zod directement dans les options du formulaire pour valider les champs (`onChange`, `onSubmit`).
* Créer des composants de champs réutilisables (comme `InputField` ou `TextareaField`) en connectant les props de TanStack Form (`field.state.value`, `field.handleChange`, etc.) pour garder un code propre et type-safe.
* Utiliser `form.Subscribe` pour écouter l'état du formulaire (par exemple, pour afficher un loader lors de la soumission `isSubmitting`).

4) **Chiffres de revenus annoncés :**
* Non précisé.

---

# TUTO Server Actions en NextJS : La nouvelle feature React

Vidéo : https://youtu.be/7AvrO4fL10A · durée 29:31 · résumé Gemini (gemini-flash-lite-latest, lot de 8) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Maîtriser les **Server Actions** dans Next.js pour remplacer les API routes traditionnelles et simplifier le développement fullstack.
2) **Outils, sites ou dépôts GitHub cités :**
   - **Next.js** : Framework React gratuit.
   - **Prisma** : ORM gratuit pour interagir avec la base de données.
   - **YouCode** : Plateforme de formation du créateur (cours payants/gratuits).
3) **Astuces concrètes et réutilisables :**
   - Déclarer une Server Action en ajoutant la directive `"use server"` au sommet d'une fonction asynchrone (dans un Server Component ou un fichier séparé).
   - Passer une Server Action directement dans la prop `action` d'un élément `<form>`, ou l'utiliser avec l'attribut `formAction` sur un bouton.
   - Utiliser `revalidatePath('/chemin')` dans une Server Action pour rafraîchir les données de la page côté client après une mutation.
   - Utiliser le hook `useFormStatus` (ou `useTransition`) dans un Client Component pour gérer l'état de chargement (`pending`) d'un bouton lors de la soumission d'un formulaire.
4) **Chiffres de revenus annoncés :** Non précisé.

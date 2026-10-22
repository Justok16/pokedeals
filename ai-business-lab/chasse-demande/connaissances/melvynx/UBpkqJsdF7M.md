# ILS ONT RÉSOLU l’Upload D’image avec NextJS

Vidéo : https://youtu.be/UBpkqJsdF7M · durée 9:45 · résumé Gemini (gemini-flash-lite-latest, lot de 8) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Utiliser **Vercel Blob** pour gérer l'upload de fichiers et d'images de manière simple et efficace dans des applications Next.js.
2) **Outils, sites ou dépôts GitHub cités :**
   - **Vercel Blob** : Service de stockage d'objets cloud (intégré à Vercel), avec un plan gratuit (Hobby) et des offres payantes (Pro). Il sert à stocker et récupérer des fichiers/images.
   - **Codeline** : Plateforme de formation payante du créateur (mentionnée pour ses cours).
   - **@vercel/blob** : Bibliothèque npm gratuite pour interagir avec Vercel Blob.
3) **Astuces concrètes et réutilisables :**
   - Créer un Blob Store directement depuis le dashboard Vercel et récupérer les variables d'environnement (`BLOB_READ_WRITE_TOKEN`).
   - Installer le package via `pnpm install @vercel/blob`.
   - Utiliser `put` côté serveur dans une Server Action Next.js pour envoyer le fichier et récupérer son URL publique.
   - Utiliser `FormData` pour récupérer les fichiers soumis via un formulaire HTML et les traiter côté serveur (`use server`).
4) **Chiffres de revenus annoncés :** Non précisé.

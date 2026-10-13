# Comment utiliser ChatGPT image dans ton application ?

Vidéo : https://youtu.be/zhSsIav_VvA · durée 11:20 · résumé Gemini (gemini-flash-lite-latest, lot de 4) du 2026-10-12
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Intégrer la génération et l'édition d'images via l'API OpenAI dans Next.js en combinant l'utilisation du SDK officiel et d'AWS S3 (ou du stockage local) pour manipuler les fichiers générés.
2) **Outils, sites ou dépôts GitHub cités** :
   - **OpenAI API (SDK officiel / `experimental_generateImage` / `images.edit`)** : API d'intelligence artificielle (payant à l'utilisation).
   - **Zod** : Librairie de validation de schémas (gratuit).
   - **UploadThing** : Solution de gestion de fichiers et d'uploads (freemium).
   - **Amazon S3** : Service de stockage cloud (payant à l'usage).
   - **Vercel Blob** : Stockage de fichiers cloud (freemium).
3) **Astuces concrètes et réutilisables** :
   - Activer et vérifier son organisation sur la plateforme OpenAI pour obtenir une clé API valide et accéder aux modèles de génération d'images.
   - Utiliser `experimental_generateImage` ou `images.edit` pour créer ou modifier des images à partir de prompts textuels dans une Server Action.
   - Sanitize les prompts textuels (`toLowerCase`, suppression des caractères spéciaux) avant de les passer à l'API pour éviter les erreurs de génération.
4) **Chiffres de revenus annoncés** : Non précisé.

# Tuto : Upload des images avec AWS S3 en NextJS !

Vidéo : https://youtu.be/6xaeUAcMyrQ · durée 26:24 · résumé Gemini (gemini-flash-lite-latest, lot de 4) du 2026-10-12
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Configurer AWS S3 et intégrer l'API d'génération d'images d'OpenAI dans une application Next.js pour stocker et afficher dynamiquement des avatars et des miniatures.
2) **Outils, sites ou dépôts GitHub cités** :
   - **Amazon S3** : Service de stockage cloud (payant à l'usage, env. 0,023 $ par Go).
   - **OpenAI API / DALL-E (GPT Image)** : API d'génération et d'édition d'images (payant à l'utilisation).
   - **Origin UI** : Librairie de composants graphiques/fichiers (gratuit).
   - **AWS SDK (Client S3)** : Librairie pour interagir avec S3 en Node.js (gratuit).
3) **Astuces concrètes et réutilisables** :
   - Configurer les politiques CORS et d'accès public sur un bucket AWS S3 pour permettre l'affichage direct des fichiers uploadés via des URLs publiques.
   - Utiliser `FormData` et `Buffer.from` pour traiter et envoyer des fichiers binaires vers S3 depuis une Server Action Next.js.
   - Nettoyer et formater les noms de fichiers (`sanitizePrompt`) pour éviter les erreurs de caractères spéciaux lors de la génération et de l'enregistrement des images.
4) **Chiffres de revenus annoncés** : Non précisé.

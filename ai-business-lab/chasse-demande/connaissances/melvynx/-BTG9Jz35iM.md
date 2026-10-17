# Comment upload des vidéos en NextJS avec Mux.com

Vidéo : https://youtu.be/-BTG9Jz35iM · durée 20:59 · résumé Gemini (gemini-flash-lite-latest, lot de 8) du 2026-10-14
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Cette vidéo présente une méthode simple et efficace pour intégrer l'upload de vidéos dans une application React ou Next.js en utilisant l'API de Mux, tout en expliquant les problématiques d'architecture (génération d'URL d'upload sécurisée côté serveur, formulaire client, stockage et récupération du `playbackId` dans la base de données).
2) **Outils, sites ou dépôts GitHub cités** :
   - **Tailwind Play** : Site (gratuit) — utilisé pour montrer un exemple d'interface avec lecteur vidéo.
   - **Mux (mux.com)** : Site / API (payant, tarification à l'usage avec une période d'essai/tokens gratuits au départ, puis facturé au stockage et à la lecture/delivery) — service tiers utilisé pour gérer l'upload, l'encodage et la lecture des vidéos.
   - **Escalidraw** : Site (gratuit) — utilisé pour schématiser le parcours de l'upload entre le client, le serveur et Mux.
   - **Prisma** : ORM (gratuit) — utilisé pour interagir avec la base de données (sauvegarde des données d'upload et du `playbackId`).
   - **Next.js** : Framework (gratuit) — utilisé pour créer l'application web.
   - **shadcn/ui** : Bibliothèque de composants (gratuit) — utilisée pour les éléments d'interface (formulaires, boutons, cartes).
   - **`@mux/mux-upload-react`** : Package npm (gratuit) — composant React pour gérer l'interface d'upload vers Mux.
   - **`@mux/mux-player-react`** : Package npm (gratuit) — composant React pour lire les vidéos Mux.
3) **Astuces concrètes et réutilisables** :
   - Ne jamais permettre au client de générer directement l'URL d'upload vers Mux sans passer par le serveur, pour des raisons de sécurité et de contrôle des droits (vérifier si l'utilisateur est admin, par exemple).
   - Créer une Server Component ou une route API pour appeler l'API de Mux (`mux.video.uploads.create`) et obtenir une `directUpload` URL avec un niveau de sécurité public.
   - Utiliser le composant `<MuxUploader>` en lui passant l'endpoint (l'URL d'upload générée) et configurer le callback `onSuccess` pour mettre à jour l'état local et afficher un formulaire de titre de vidéo.
   - Récupérer l'`uploadId` via le formulaire, appeler l'API Mux (`mux.video.uploads.retrieve(uploadId)`) pour obtenir l'`assetId` et le `playbackId`, puis stocker ces informations en base de données.
   - Intégrer le lecteur vidéo `<MuxPlayer>` en lui transmettant le `playbackId` pour diffuser la vidéo.
   - Personnaliser le lecteur Mux en modifiant la couleur d'accentuation (`accentColor`) ou la couleur principale (`primaryColor`) avec des codes hexadécimaux pour l'harmoniser avec le design de l'application.
4) **Chiffres de revenus annoncés** : Non précisé.

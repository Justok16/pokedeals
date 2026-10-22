# TUTO / COURS NextJS Server Action + API Route en 1 HEURE (3/5)

Vidéo : https://youtu.be/baNfqwCB7cs · durée 1:01:08 · résumé Gemini (gemini-flash-lite-latest) du 2026-10-12
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé de la vidéo en français, structuré selon tes demandes :

---

### 1. Idée principale
La vidéo est une masterclass d'une heure sur la manipulation des données (mutations) en **Next.js** à l'aide des **Server Actions** et des **API Routes**, en expliquant comment créer, valider (avec Zod), mettre à jour et supprimer des données (reviews) de manière sécurisée et performante (notamment en comparant les approches client/serveur, et en utilisant des bibliothèques de type-safety comme `next-safe-action`).

---

### 2. Outils, sites et dépôts GitHub cités
* **Next.js** (Framework React) — *Gratuit* (Open Source) : Utilisé pour bâtir l'application web complète (côté serveur et client).
* **Prisma** (ORM / Base de données) — *Gratuit / Open Source* : Utilisé pour interagir avec la base de données (rechercher, créer, mettre à jour, supprimer des reviews).
* **Zod** (Bibliothèque de validation de schémas) — *Gratuit / Open Source* : Utilisé pour valider et typer les données des formulaires et des API.
* **shadcn/ui** (Bibliothèque de composants UI) — *Gratuit / Open Source* : Utilisé pour intégrer des composants d'interface utilisateur propres (formulaires, boutons, etc.).
* **next-safe-action** (`next-safe-action` / package npm) — *Gratuit / Open Source* : Bibliothèque de type-safety pour gérer et valider les Server Actions en toute sécurité dans Next.js.
* **React** — *Gratuit* : Bibliothèque de base pour la construction d'interfaces.

*(Note : Aucun dépôt GitHub spécifique ou URL de dépôt n'a été nommé explicitement par son nom de repo, hormis les instructions d'installation des packages npm comme `pnpm add next-safe-action zod` et les liens vers les docs officielles mentionnés à l'oral comme `mlv.sh/nextjs`).*

---

### 3. Astuces concrètes et réutilisables
* **Utilisation de `"use server"`** : Permet de déclarer une fonction exécutée côté serveur directement dans un Server Component ou une Server Action, évitant de surcharger le client.
* **Validation des formulaires avec `FormData` et Zod** : Récupérer les données brutes d'un formulaire via l'objet `FormData` natif et les valider proprement (côté serveur) pour garantir la sécurité et l'intégrité des données avant de les insérer en base de données avec Prisma.
* **Rafraîchissement ciblé avec `revalidatePath()`** : Pour forcer Next.js à purger le cache d'une route spécifique et à recharger les données instantanément après une mutation, sans avoir à recharger toute la page manuellement.
* **Gestion des états de chargement (`useTransition` / `useFormStatus` / `useActionState`)** : Permet d'afficher des indicateurs de chargement ou de bloquer les boutons (`disabled`) pendant qu'une Server Action est en cours d'exécution.
* **Sécurisation robuste avec `next-safe-action`** : Centraliser la gestion des erreurs, les middlewares et le typage strict des paramètres d'entrée/sortie des actions serveur pour éviter les bugs d'exécution et les plantages inattendus (codes 500).

---

### 4. Chiffres de revenus annoncés
* **Affirmé par l'auteur** : *Non précisé* (aucun chiffre de revenus ou de gains financiers n'est mentionné dans la vidéo, le contenu étant purement technique et axé sur le développement web).

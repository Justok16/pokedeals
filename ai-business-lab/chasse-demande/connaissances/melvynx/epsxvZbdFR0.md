# DECOUVERTE de NextJS 13 (INCROYABLE) AVEC UNE PETITE APP - REACT - SSR

Vidéo : https://youtu.be/epsxvZbdFR0 · durée 28:28 · résumé Gemini (gemini-flash-lite-latest) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé de la vidéo, structuré selon tes consignes :

### 1) Idée principale
La vidéo présente les nouveautés de Next.js 13 à travers le développement en direct d'une application de type « to-do list ». L'auteur explore la distinction entre *Server Components* et *Client Components*, l'utilisation de Prisma pour la gestion de la base de données (avec SQLite), et l'intégration de bibliothèques d'interface (Tailwind CSS et daisyUI) pour créer une application web interactive et moderne.

---

### 2) Outils, sites et dépôts GitHub cités
* **Next.js 13** : Framework React (version bêta présentée).
  * *Modèle économique* : Gratuit (open source).
  * *Utilité* : Développement d'applications web full-stack, routage basé sur les dossiers, gestion des composants côté serveur et client.
* **Prisma** : ORM (Object-Relational Mapping).
  * *Modèle économique* : Gratuit (open source).
  * *Utilité* : Gestion et manipulation de la base de données (associé ici à SQLite).
* **SQLite** : Système de gestion de base de données relationnelle.
  * *Modèle économique* : Gratuit (open source).
  * *Utilité* : Stockage léger des données de l'application.
* **Tailwind CSS** : Framework CSS utilitaire.
  * *Modèle économique* : Gratuit (open source).
  * *Utilité* : Design et mise en forme rapide des interfaces directement dans le code HTML.
* **daisyUI** : Bibliothèque de composants pour Tailwind CSS.
  * *Modèle économique* : Gratuit (open source).
  * *Utilité* : Ajout rapide de composants UI prêts à l'emploi (boutons, champs de texte, interrupteurs/switches).

---

### 3) Astuces concrètes et réutilisables
* **Séparation Layout / Page** : Utiliser le dossier `app/` de Next.js 13 pour séparer les éléments communs (comme une barre de navigation dans `layout.tsx`) du contenu spécifique de chaque page (`page.tsx`).
* **Server Components par défaut** : Dans Next.js 13, les composants sont des *Server Components* par défaut, ce qui permet d'interroger directement la base de données (ex. `prisma.todo.findMany()`) sans utiliser de hooks comme `useEffect`.
* **Directive Use Client** : Ajouter `'use client';` au sommet d'un composant pour l'exécuter côté client (nécessaire pour les formulaires, les écouteurs d'événements et les hooks React).
* **Rafraîchissement du routeur** : Utiliser le hook `useRouter()` et la méthode `router.refresh()` pour actualiser les données affichées après une modification (création ou mise à jour d'un élément) sans recharger toute la page.
* **Gestion des erreurs (Error Boundary)** : Créer un fichier `error.tsx` pour isoler et gérer les erreurs de rendu de manière élégante au niveau des composants.
* **États de chargement (Loading UI)** : Utiliser un fichier `loading.tsx` pour afficher un indicateur de chargement automatique pendant la récupération des données.

---

### 4) Chiffres de revenus annoncés
* **Revenus annoncés** : Non précisé (aucun chiffre d'affaires ou montant de gains n'est mentionné dans la vidéo).

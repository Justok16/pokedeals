# TUTO / COURS sur le DOM en JavaScript COMPLET (3/3)

Vidéo : https://youtu.be/WlEAYk_blgs · durée 1:50:17 · résumé Gemini (gemini-flash-lite-latest) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé de la vidéo, structuré selon tes demandes :

### 1) Idée principale
La vidéo est un tutoriel de développement web en JavaScript axé sur la manipulation du DOM (Document Object Model). Le créateur (Melvynx) montre comment reproduire pas à pas un quiz interactif dynamique, similaire à un projet créé à partir d'une vidéo sur ChatGPT, en partant de zéro (installation de VS Code, configuration de Vite) jusqu'au déploiement du code sur GitHub Pages. L'objectif est d'aider les développeurs à bien comprendre les bases de JS, la structure d'un site web, la gestion des variables, des tableaux, des chaînes de caractères, ainsi que l'utilisation des sélecteurs (querySelector), des événements (addEventListener), et le déploiement gratuit d'une application en ligne.

---

### 2) Outils, sites et dépôts GitHub cités
*   **Visual Studio Code (VS Code)** — *Gratuit* : Éditeur de code source utilisé pour écrire et développer l'application.
*   **Vite.js** *(Vite)* — *Gratuit* : Outil de build et de développement frontend ultra-rapide utilisé pour lancer le serveur local et structurer le projet.
*   **GitHub** — *Gratuit* : Plateforme de gestion de code source utilisée pour créer le dépôt distant et stocker le projet.
*   **GitHub Pages** — *Gratuit* : Service d'hébergement web de GitHub utilisé pour déployer et rendre l'application accessible publiquement en ligne.
*   **Notion** — *Gratuit / Payant* (version gratuite utilisée ici) : Application de prise de notes utilisée pour centraliser les feuilles de style CSS et les ressources partagées.
*   **CodeSandbox** — *Gratuit* : Plateforme de développement en ligne (mentionnée pour retrouver du code source ou s'exercer).

---

### 3) Astuces concrètes et réutilisables
*   **Utiliser Vite.js** pour démarrer un projet JavaScript moderne rapidement avec la commande `npm create vite@latest`.
*   **Privilégier `querySelector` et `querySelectorAll`** plutôt que les anciennes méthodes (`getElementById`, `getElementsByClassName`) pour cibler les éléments HTML de manière moderne et flexible grâce aux sélecteurs CSS.
*   **Manipuler le DOM dynamiquement** en créant des éléments via `document.createElement`, en modifiant leur contenu avec `innerHTML` ou `innerText`, et en les insérant dans la page avec `appendChild` ou `insertBefore`.
*   **Utiliser `insertAdjacentHTML` ou des template strings** pour injecter du code HTML structuré directement depuis le JavaScript.
*   **Gérer la propagation des événements** (`bubbling` vs `capturing`) et comprendre comment utiliser `event.stopPropagation()` pour stopper la propagation non désirée des clics.
*   **Automatiser le déploiement** d'une application web statique sur **GitHub Pages** en configurant correctement le fichier `vite.config.js` (`base`) et en automatisant le tout avec un fichier de workflow GitHub Actions (`.github/workflows/github-page.yml`).

---

### 4) Chiffres de revenus annoncés
*   *Affirmé par l'auteur* : **Non précisé** (la vidéo est un tutoriel technique de programmation et ne mentionne aucun montant ni objectif de gain financier).

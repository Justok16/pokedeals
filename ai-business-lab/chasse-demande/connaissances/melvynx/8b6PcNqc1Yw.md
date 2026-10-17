# CLOUDFLARE CLONE Next.js en 1 semaine avec IA (Vinext avec Vite.js)

Vidéo : https://youtu.be/8b6PcNqc1Yw · durée 21:03 · résumé Gemini (gemini-3.5-flash-lite) du 2026-10-08
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé de la vidéo, structuré pour quelqu'un qui cherche à gagner de l'argent légalement avec l'IA et Claude Code :

---

### 1) Idée principale
Un ingénieur de Cloudflare a recréé en une semaine une alternative à **Next.js** nommée **vinext** en utilisant l'IA (notamment **Claude Code**). Ce projet démontre qu'avec l'IA, il est désormais possible de réimplémenter des frameworks complexes et d'optimiser radicalement le coût et la vitesse de développement de logiciels, tout en posant les bases d'une nouvelle ère pour les développeurs (et de nouvelles opportunités pour monétiser des services ou des compétences sur ces technologies).

---

### 2) Outils, sites et dépôts GitHub cités

* **Cloudflare / Cloudflare Blog**
  * *Type :* Gratuit (plateforme cloud / hébergement).
  * *Utilité :* Hébergement des applications, Workers, et source de l'article analysé.
* **Next.js**
  * *Type :* Open source / Gratuit (framework React).
  * *Utilité :* Framework frontend populaire mais complexe à déployer sur des architectures serverless sans adaptation.
* **vinext** (dérivé de Vite + Next)
  * *Type :* Open source / Gratuit (disponible sur GitHub).
  * *Utilité :* Un "drop-in replacement" pour Next.js basé sur Vite, conçu pour s'exécuter nativement sur les Cloudflare Workers.
* **Vite**
  * *Type :* Open source / Gratuit.
  * *Utilité :* Outil de build frontend rapide utilisé par la majorité de l'écosystème hors Next.js.
* **Turbo / Turbopack**
  * *Type :* Gratuit.
  * *Utilité :* Outil de build associé à Next.js.
* **Cloudflare Workers**
  * *Type :* Gratuit / Payant (selon l'usage).
  * *Utilité :* Plateforme serverless edge-first pour exécuter du code (ex. déploiement de vinext).
* **OpenNext**
  * *Type :* Open source / Gratuit.
  * *Utilité :* Approche précédente pour adapter Next.js à d'autres hébergeurs (via "reverse engineering").
* **GitHub** (Dépôt GitHub de vinext)
  * *Type :* Gratuit.
  * *Utilité :* Hébergement du code source du projet `vinext`.
* **Claude Code / OpenCode / Claude (par Anthropic)**
  * *Type :* Payant (via des jetons/API tokens).
  * *Utilité :* Assistant IA utilisé pour écrire le code, gérer les tests, refactoriser et concevoir toute l'architecture de vinext.
* **Vercel**
  * *Type :* Gratuit / Payant.
  * *Utilité :* Plateforme d'hébergement concurrente (qui a réagi aux annonces de vinext).
* **Coderly.com / `mlvyn.dev`** *(Plateforme personnelle du créateur de la vidéo)*
  * *Type :* Payant (formation / masterclass).
  * *Utilité :* Plateforme de formation proposant un programme sur l'utilisation de Claude Code et l'IA pour coder 3 fois plus vite ("Code 3x plus vite avec L'IA").

---

### 3) Astuces concrètes et réutilisables

* **Exploiter les tests existants pour l'IA :** Au lieu de créer de nouveaux tests pour une IA, récupérez une suite de tests existante (par exemple les milliers de tests E2E d'un dépôt open source comme Next.js) et demandez à l'IA de s'y conformer pour valider son propre code de manière automatisée.
* **Boucle de rétroaction itérative (Tâches -> Tests -> Merge) :** Divisez le développement en petites tâches claires, laissez l'IA écrire le code et les tests, lancez les tests automatiquement, fusionnez si tout est vert, ou demandez à l'IA de corriger ses erreurs si les tests échouent.
* **Utiliser les agents IA pour la revue de code :** Mettez en place des agents IA pour relire le code et corriger les bugs en amont (le projet a ainsi exécuté des centaines de sessions de review automatisée).
* **Remplacement direct ("Drop-in replacement") :** Créer des outils qui s'intègrent sans friction dans des piles technologiques existantes (par exemple, remplacer simplement `next` par `vinext` dans les scripts sans tout réécrire) facilite grandement l'adoption par les développeurs.

---

### 4) Chiffres de revenus annoncés (marqués « affirmé par l'auteur »)

* **Coût de création du projet (en tokens IA) :** 
  * *Affirmé par l'auteur :* Environ **1 100 $** en jetons API Claude pour recréer le framework de zéro en une semaine.

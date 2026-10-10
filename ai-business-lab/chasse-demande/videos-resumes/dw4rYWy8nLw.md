# Top 15 Things built with Claude OPUS 5.5

Vidéo : https://youtu.be/dw4rYWy8nLw · chaîne Code Bear · envoyée par l'utilisateur le 29/09/2026 · résumé Gemini (gemini-3.5-flash) du 2026-09-29
(chiffres et affirmations des auteurs : non vérifiés)

Voici un résumé complet de la vidéo, structuré pour vous aider à comprendre comment exploiter ces technologies pour créer et monétiser des projets avec l'IA.

---

### 1) Idée principale
La vidéo présente un classement des **15 meilleures créations** (jeux, animations, simulations et applications web interactives) réalisées en seulement quelques jours grâce aux capacités de génération de code de l'IA de l'Anthropic (**Claude / Opus 5.5**). L'idée centrale est de montrer qu'avec **un seul prompt** (ou très peu d'instructions), des utilisateurs sans compétences avancées en programmation peuvent créer des produits numériques complets, fonctionnels, prêts à être déployés et potentiellement monétisés (en tant qu'applications SaaS, jeux Web, ou outils éducatifs).

---

### 2) Outils, sites et technologies cités

Voici les outils et technologies mentionnés dans la vidéo, leur coût et leur utilité :

*   **Claude (Opus / "Opus 5.5")** (par Anthropic) :
    *   *Statut :* Payant (via abonnement Claude Pro à 20$/mois ou via l'API à la consommation).
    *   *Rôle :* L'IA principale qui a généré l'intégralité du code, des graphismes (via code), de la musique et de la logique de tous les projets présentés.
*   **Blender** (mentionné au projet #7) :
    *   *Statut :* Gratuit et Open Source.
    *   *Rôle :* Logiciel 3D contrôlé par l'IA (via un script Python généré par Claude) pour créer une scène 3D procédurale d'un château avec des feux d'artifice.
*   **HTML5 / JavaScript / WebGL / P5.js** (technologies sous-jacentes des projets) :
    *   *Statut :* Gratuit.
    *   *Rôle :* Langages générés par l'IA pour faire tourner les jeux (comme le clone de *Dark Souls* ou *Minecraft*) et les animations directement dans un navigateur web, souvent dans un seul fichier HTML autonome.
*   **Dépôts GitHub ou sites spécifiques :** *Non précisés* (la vidéo mentionne uniquement les pseudonymes des créateurs sur le réseau social X/Twitter, mais pas de liens directs vers des dépôts de code).

---

### 3) Astuces concrètes et réutilisables pour créer des produits

La vidéo révèle plusieurs techniques de prompt et d'architecture système réutilisables pour vos propres projets :

*   **Le prompt "Max Effort" (Effort Maximum) :** Pour le projet #4 (un showreel de motion design), l'utilisateur a simplement demandé à l'IA de faire une vidéo de 15 secondes "comme si elle était un motion designer professionnel et de se donner à fond" (*"go all out"*). Donner une personnalité d'expert à l'IA pousse la qualité de son code au maximum.
*   **L'architecture multi-agents :** Pour le projet #2 (un clip vidéo de 2,5 minutes), l'utilisateur a utilisé Claude pour coordonner **7 sous-agents IA** travaillant en parallèle. Chaque sous-agent s'est occupé de coder une scène spécifique. C'est une méthode idéale pour les projets complexes.
*   **Génération "Zero-Dependency" (Sans bibliothèque externe) :** Plusieurs projets (comme le mosaic en carrelage de verre #13) ont été codés dans **un seul fichier HTML**, sans charger d'images ou de bibliothèques externes. Tout est dessiné en code (CSS/Canvas). Cela garantit des applications ultra-légères, faciles à héberger gratuitement (sur GitHub Pages ou Vercel).
*   **Musique et sons générés par le code :** Plusieurs créateurs ont demandé à Claude d'écrire du code audio (Web Audio API) pour synthétiser des instruments de musique directement dans le navigateur, évitant ainsi d'avoir à importer des fichiers audio lourds ou soumis à des droits d'auteur.

---

### 4) Chiffres de revenus et coûts annoncés

*   **Revenus générés par les créateurs :** *Non précisés* (la vidéo se concentre sur la popularité des projets en nombre de vues sur X, allant de 70 000 à plus de 3 millions de vues).
*   **Coûts de création (API Claude) mentionnés par les auteurs :**
    *   Le château 3D sur Blender (Projet #7) a coûté environ **13 $** de jetons (tokens) API.
    *   L'application interactive d'optique "Lens Lab" (Projet #1, qui a fait plus de 3 millions de vues) a été développée en 1h26 pour un coût d'API de **25,86 $**.

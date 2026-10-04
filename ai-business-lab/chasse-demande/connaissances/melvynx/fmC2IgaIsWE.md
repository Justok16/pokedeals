# Kombai 2.0 ajoute le design mode et change le code pour toujours (mieux et que Claude Design)

Vidéo : https://youtu.be/fmC2IgaIsWE · durée 18:56 · résumé Gemini (gemini-3.8-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) L'idée principale
Les agents IA de développement (comme Claude Code ou Codex) sont très performants pour la logique de programmation, mais produisent généralement des interfaces utilisateur (UI/UX) génériques ou mal finies. La solution présentée consiste à intégrer **Kombai** et son nouveau **Design Mode** dans son flux de travail : cela permet de concevoir, d'itérer visuellement sur un canevas (génération de style guides, thèmes, variantes) puis de convertir directement le design validé en code de production adapté à sa propre stack technique.

---

### 2) Outils, sites et dépôts cités

* **Kombai (kombai.com)**
  * **Modèle économique :** Gratuit (offre *Free* incluant 300 crédits/mois : 150 à l'inscription + 50/jour) / Payant (offre *Pro* à partir de 20 $/mois pour 2 000 crédits, plans équipe/entreprise).
  * **Utilité :** Extension pour éditeur de code (VS Code) et agent IA spécialisé frontend. Il permet de générer des systèmes de design, d'explorer des maquettes interactives sur canevas (*Design Mode*), d'éditer le CSS, et d'implémenter automatiquement les composants dans le projet (*Code Mode*).
* **Extension Kombai pour navigateur (Chrome)**
  * **Modèle économique :** Inclus avec Kombai.
  * **Utilité :** Ouvre un navigateur synchronisé avec le chat de l'éditeur pour inspecter, sélectionner visuellement des éléments du DOM (titre, boutons, conteneurs) et envoyer des instructions de retouche ciblées à l'agent.
* **Thumbfa.st**
  * **Modèle économique :** Payant / Freemium (SaaS de l'auteur).
  * **Utilité :** Projet SaaS de l'auteur (générateur de miniatures YouTube par IA) servant d'exemple pratique pour refondre les cartes d'inspiration et le tableau de bord d'administration des feedbacks.
* **Claude Design** (cité brièvement à titre de comparaison)
  * **Modèle économique :** Non précisé dans la vidéo.
  * **Utilité :** Outil de génération de design, critiqué ici pour ne pas avoir un accès direct au contexte et au code source d'une application existante.
* **Claude Code / Codex** (mentionnés comme références d'agents de code)
  * **Modèle économique :** Non détaillé dans la vidéo.
  * **Utilité :** Outils de développement par invite de commande / agents IA d'ingénierie logicielle.
* **Technologies & bibliothèques mentionnées dans la stack :**
  * *React, Next.js, Vite, Tailwind CSS, shadcn/ui, Convex, Lucide Icons, TanStack Router/Query* (toutes open source / gratuites).

---

### 3) Astuces concrètes et réutilisables

1. **Séparer la phase visuelle de la phase d'implémentation :**
   * Utiliser d'abord le mode **Design** pour créer un guide de style cohérent (palette de couleurs, typographie, espacements, rayons de courbure) et tester plusieurs variantes sur un canevas sans toucher aux fichiers source.
2. **Utiliser l'outil de sélection visuelle (*Snip* / Sélecteur DOM) :**
   * Plutôt que d'écrire de longs prompts pour décrire un bug visuel, capturez la zone exacte ou l'élément concerné via l'extension navigateur/canevas et demandez une modification précise (ex. : supprimer un badge, ajuster le ratio en 16:9, masquer les actions dans un menu déroulant).
3. **Réutiliser les composants existants du projet :**
   * Au moment de basculer en mode **Code**, ordonnez explicitement à l'agent d'utiliser les composants UI déjà installés dans le projet (ex. boutons *shadcn*, icônes *Lucide*, formatage de date) pour éviter qu'il ne recrée du code CSS/HTML redondant à partir de zéro.
4. **Itérer avec des variations automatiques (*Surprise me* / *Generate variants*) :**
   * Exploitez les options de génération automatique pour tester des déclinaisons d'écrans selon les tailles d'affichage (version mobile, tablette, desktop) et les thèmes (Dark/Light mode) avant validation.

---

### 4) Chiffres de revenus annoncés

* **Non précisé** : Aucun chiffre de gains ou de revenus n'est mentionné ou affirmé par l'auteur dans cette vidéo.

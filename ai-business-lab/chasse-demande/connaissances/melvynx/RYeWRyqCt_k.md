# CODEX : Créer une application iOS en moins de 20 minutes

Vidéo : https://youtu.be/RYeWRyqCt_k · durée 23:01 · résumé Gemini (gemini-3.7-flash) du 2026-10-03
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
L’objectif est de concevoir, développer et tester une application mobile native (iOS / Android) fonctionnelle en moins d'une journée (et d'en prototyper la base en une vingtaine de minutes) sans écrire une seule ligne de code à la main. Le processus repose sur l'utilisation d'un agent de code IA (**Codex App**), d'un environnement d'exécution léger (**Bun**), de l'application de test mobile (**Expo Go**) et de modules d'instructions spécialisés (**skills**) pour le design, le cadrage du projet, la résolution de bugs et la génération d'icônes.

---

### 2) Outils, sites et dépôts GitHub cités

* **Codex App (OpenAI Developers)**
  * *Statut :* **Payant** (inclus avec les abonnements ChatGPT Plus, Pro, Business, Enterprise).
  * *Rôle :* Application de bureau servant d'environnement de commande et d'agent IA pour générer, modifier le code du projet et exécuter des commandes terminal.
* **Expo Go (App Store / Google Play)**
  * *Statut :* **Gratuit**.
  * *Rôle :* Application mobile permettant de prévisualiser et tester l'application directement sur son smartphone via un simple QR code sur le même réseau Wi-Fi.
* **Bun (`bun.sh`)**
  * *Statut :* **Gratuit / Open source**.
  * *Rôle :* Runtime JavaScript et gestionnaire de paquets utilisé pour initialiser le projet Expo et lancer le serveur de développement rapidement.
* **Guide Notion (partagé par l'auteur)**
  * *Statut :* **Gratuit**.
  * *Rôle :* Checklist pas-à-pas contenant les commandes terminal et les prompts à copier-coller.
* **Skills / Dépôts GitHub (installables via `npx skills add ...`) :**
  * `expo/skills` (`building-native-ui`) — *Gratuit / Open source* : Fournit à l'IA les bonnes pratiques pour créer des interfaces natives iOS avec Expo (Liquid Glass, Expo Router, SF Symbols).
  * `vercel/agent-skills` (`react-native-skills`) — *Gratuit / Open source* : Guide l'IA sur l'optimisation des performances et les patterns React Native.
  * `jakubkrehel/make-interfaces-feel-better` — *Gratuit / Open source* : Améliore les micro-interactions, bordures et animations de l'interface.
  * `mattpocock/skills` (`grilling` / `grill-me`) — *Gratuit / Open source* : Lance un interrogatoire interactif où l'IA pose des questions précises pour verrouiller le cahier des charges avant de générer le code.
  * `melvynx/aiblueprint` (Dépôt GitHub de l'auteur) :
    * `skill app-icon` — *Gratuit* : Génère automatiquement les logos/icônes de l'application via les capacités de génération d'images et configure les fichiers dans le projet.
    * `skill appstore-connect` — *Gratuit* : Instructions et scripts pour automatiser la connexion et l'envoi de versions TestFlight vers l'App Store.
    * `skill apex` / `agents setup` — *Mentionné dans la présentation* : Workflow automatisé d'analyse, d'exécution et d'auto-test.
* **Sites et formations de l'auteur :**
  * `codelynx.dev` : Blog et formations de l'auteur.
  * `mlv.sh/fm` (AI Builder Mobile) : Page d'inscription à une mini-formation gratuite partagée par l'auteur.
* **Xcode / Simulateur iOS**
  * *Statut :* **Gratuit** (sur macOS).
  * *Rôle :* Permet de simuler un iPhone directement sur l'écran d'ordinateur (alternative plus avancée à Expo Go).

---

### 3) Astuces concrètes et réutilisables

1. **Ne pas demander de tout coder d'un coup :** Utiliser le skill `grilling` pour que l'IA pose d'abord 10 à 15 questions de clarification (périmètre de la V1, format des données, logique de validation). Cela évite de générer du code inutile ou hors sujet.
2. **Compatibilité Expo Go :** Lors de la création du projet avec `bun create expo --template default`, sélectionner impérativement la version SDK recommandée pour Expo Go (*For learning with Expo Go*) afin d'éviter les rejets de version sur smartphone.
3. **Prévisualisation instantanée sans compte développeur Apple :** Lancer le projet avec `bun run start` (ou `bun run dev`) et scanner le QR code affiché dans le terminal avec l'application Expo Go. L'ordinateur et le smartphone doivent être connectés au **même réseau Wi-Fi**.
4. **Corriger les erreurs par capture d'écran :** En cas d'écran rouge / crash sur le téléphone, faire une capture d'écran du message d'erreur, la glisser directement dans le chat de Codex et taper simplement `fix it`.
5. **Guidage visuel précis :** Envoyer des captures d'écran de l'application à l'IA en annotant avec des flèches/textes les éléments à déplacer (ex. : « déplacer le bouton Ajouter en haut à droite ») et demander un style épuré avec Tailwind CSS et composants natifs.

---

### 4) Chiffres de revenus annoncés

* **Aucun montant chiffré (revenus, ventes, abonnements) n'est mentionné dans la vidéo.**
* L'auteur affirme uniquement qu'il est possible de *« faire de l'argent avec »* et qu'il a déjà publié une petite application (nommée *Daily AI Citation*) créée en *« moins de 1 jour »* (*affirmé par l'auteur*).

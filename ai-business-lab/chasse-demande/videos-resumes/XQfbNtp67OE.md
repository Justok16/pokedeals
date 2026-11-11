# XQfbNtp67OE — « I Spent $5,000 Using Claude Fable 5.2 (This Feels Different) »

- Auteur : Riley Brown ; lien : https://youtu.be/XQfbNtp67OE
- Envoyée par l'utilisateur le 11/11/2026 ; résumée le 11/11 par Gemini (via le relais, modèle gemini-3.6-flash)
- Les prix et les chiffres ci-dessous sont « affirmés par l'auteur », non vérifiés.

## Tri pour DIG16 (11/11)

- **Rien à appliquer aujourd'hui** : la vidéo montre ce qu'un modèle récent sait fabriquer (3D dans Blender, montage vidéo, jeux, présentations, cartes électroniques), avec des budgets de plusieurs centaines à plusieurs milliers de dollars. Budget 0 € et nouvelles vidéos en pause jusqu'au premier client payant.
- **Déjà en réserve** : Blender piloté par script (`connaissances/reserve-prete.md`, vidéo lKIhUBjCgZM du même auteur).
- **Ajouté à la réserve** : v2.video (révision de montages vidéo par versions et commentaires horodatés ; page lue le 11/11 : outil en ligne de commande pour macOS, prix non indiqué sur la page).
- **Écartés** : RunPod (location de cartes graphiques, payant), KiCad, Autodesk Inventor et RoboDojo (matériel et robotique, hors sujet).
- **Déjà en place** : pages et documents interactifs (Artifacts) ; Remotion et Hyperframes : cités seulement, sans usage tant que les vidéos sont en pause.

## Résumé (Gemini)

Voici le résumé structuré de la vidéo :

---

### 1) L'idée principale
La vidéo présente les capacités du modèle d’IA **Claude Fable 5.2** (d’Anthropic), qualifié par l'auteur d'**AGVI** (*Artificial General Visual Intelligence*). L'objectif est de montrer comment ce type d'IA visuelle et agentique permet d'automatiser entièrement la production 3D, le montage vidéo, le développement de jeux vidéo, la création de présentations complexes et la conception matérielle (hardware) à partir de simples consignes en langage naturel.

---

### 2) Outils, sites et dépôts GitHub cités

*   **Claude / Claude Code / Claude App (Anthropic)**
    *   **Statut :** Payant (via abonnement / consommation d'API ; l'auteur indique avoir dépensé environ 5 000 $ en tokens sur 48h).
    *   **Utilisation :** Orchestration globale des tâches via du code (Python, JS), contrôle de logiciels tiers, création d'applications, de jeux et de vidéos.
*   **Blender**
    *   **Statut :** Gratuit (Open-source).
    *   **Utilisation :** Création et rendu de scènes 3D, éclairage, animation et modélisation, pilotés à 100 % par des scripts Python générés par l'IA.
*   **RunPod**
    *   **Statut :** Payant (location de GPU dans le cloud à la minute).
    *   **Utilisation :** Calcul à distance des rendus 3D lourds en 4K (ex. 10 GPU loués pour réduire 5h de rendu local à 52 minutes pour environ 6 $).
*   **v2.video**
    *   **Statut :** Gratuit.
    *   **Utilisation :** Plateforme / dépôt présenté comme "le GitHub du montage vidéo". Permet le contrôle de version (*version control*), le suivi des itérations de montage par l'IA et l'ajout de commentaires horodatés.
*   **Remotion / Hyperframes / JavaScript / Tesseract**
    *   **Statut :** Gratuit / Open-source (selon l'outil).
    *   **Utilisation :** Stacks de développement et bibliothèques de code utilisées pour le montage vidéo programmatique et l'extraction de texte.
*   **Claude Artifacts (Whiteboards, Sheets, Data)**
    *   **Statut :** Inclus dans l'écosystème Claude.
    *   **Utilisation :** Tableaux blancs interactifs (style Figma/Excalidraw), feuilles de calcul et visualisations de données manipulables directement par l'IA et l'utilisateur.
*   **KiCad & Autodesk Inventor**
    *   **Statut :** KiCad (Gratuit/Open-source), Autodesk Inventor (Payant).
    *   **Utilisation :** Outils de conception électronique (layout PCB) et mécanique (boîtiers 3D) pour la conception de matériel (ex. création d'un Tamagotchi).
*   **RoboDojo**
    *   **Statut :** Non précisé (Benchmark de recherche).
    *   **Utilisation :** Environnement de simulation robotique utilisé pour évaluer le contrôle de robots physiques par l'IA.

---

### 3) Astuces concrètes et réutilisables

1.  **Automatisation 3D via Python dans Blender :**
    *   Plutôt que de modéliser à la main, demandez à l'IA d'écrire un script Python d'automatisation pour Blender afin de créer la scène 3D, gérer les caméras, la lumière, la mise au point et exporter la séquence.
2.  **Rendu Cloud économique avec RunPod :**
    *   Faîtes exécuter vos scripts de rendu Blender sur une ferme de GPU distants (RunPod) via l'API pour accélérer drastiquement la production d'images/vidéos 4K à moindre coût.
3.  **Montage vidéo par consigne ("Agentic Editing") :**
    *   Placez vos rushs bruts dans un dossier, connectez l'IA et donnez-lui des instructions de découpe, d'accélération, d'effets sonores et de cadrage. L'IA analyse les images et génère le fichier édité.
4.  **Workflow de révision vidéo par commentaires horodatés :**
    *   Utilisez un outil de versioning (comme `v2.video`) pour poser des annotations à des secondes précises. L'IA lit les commentaires et applique automatiquement les corrections dans la version suivante.
5.  **Génération automatique de diaporamas de recherche :**
    *   Fournissez un document de référence ou une URL à l'IA avec une problématique métier. L'IA recherche les données, génère des graphiques précis à l'échelle et produit une présentation complète.
6.  **"Vibe coding" pour le matériel (Hardware) :**
    *   Faites concevoir par l'IA la carte électronique (PCB sur KiCad), le boîtier industriel (Inventor) et le rendu marketing (Blender) en une seule chaîne d'instructions.

---

### 4) Chiffres de revenus annoncés

*   **Revenus générés / annoncés :** Aucun chiffre de chiffre d'affaires ou de revenus personnels n'est mentionné dans la vidéo (*affirmé par l'auteur*).
*   *Remarque sur les coûts cités par l'auteur :*
    *   Dépenses en tokens d'IA : ~5 000 $ en 48 heures sur Claude (*affirmé par l'auteur*).
    *   Coût de rendu Cloud (RunPod) : 5,75 $ (~6 $) pour 1329 images en 4K (*affirmé par l'auteur*).
    *   Coût de génération d'un jeu vidéo complet via API : ~550 $ (*affirmé par l'auteur*).

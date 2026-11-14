# Ctwpe-aCHiU — « Claude Fable 5.2 just made me nut »

- Auteur : WeeklyHow ; lien : https://youtu.be/Ctwpe-aCHiU
- Envoyée par l'utilisateur ; résumée le 14/11/2026 par Gemini (via le relais, modèle gemini-3.5-flash)
- Les chiffres ci-dessous sont « affirmés par l'auteur », non vérifiés.

## Tri pour DIG16 (14/11)

Démonstration en anglais de Fable 5.2 : un faux bureau d'ordinateur dans une page web, un petit jeu vidéo (Three.js) et une animation 3D d'un chiot fabriquée dans Blender, chacun à partir d'une seule consigne.

- **Blender piloté par l'IA (ici par le connecteur « Blender MCP »)** : en réserve ; l'idée est déjà notée (`connaissances/reserve-prete.md`, ligne « Blender piloté par Claude Code », du 09/11). Le connecteur lui-même n'est pas encore chez nous : dépôt, licence et contenu à lire à la source avant toute installation (le résumé le dit gratuit et libre, non vérifié). À ressortir après le premier client payant, à la reprise des nouvelles vidéos, ou si un client veut une vidéo de présentation.
- **Jeu vidéo dans le navigateur (Three.js)** : Three.js est déjà chez nous (skills `threejs-web`, `threejs-animation`) ; un jeu est hors sujet pour des sites d'artisans : écarté.
- **Faux bureau d'ordinateur dans une page web, modèles de sites à revendre** : écarté, hors sujet (aucune demande d'artisan ; règle n° 1 : pas de construction sans demande).
- **Niveau d'effort « très élevé » pour les gros chantiers** : écarté comme réglage par défaut ; nos consignes gardent le niveau moyen au quotidien et élevé pour un site client (conseil du 24/10). Le réglage appartient à l'utilisateur.
- **Modèle puissant pour le plan et les blocages, modèle léger pour les retouches** : déjà dans nos consignes (« Modèle à utiliser », 24/10).
- **Mythos 5.2 (accès restreint, recherche)** : écarté, hors sujet.
- **Coûts cités (8 $ et 40 $ par million de jetons, 76,33 $ de crédits consommés, 6 % de la limite de la semaine pour les trois projets)** : affirmés par l'auteur, non vérifiés ; aucun achat (budget 0 €). Aucun chiffre de revenu dans la vidéo.

Conclusion : rien à installer, rien à changer ; seule la 3D dans Blender reste en réserve pour la reprise des vidéos.

## Résumé (Gemini)

Voici le résumé détaillé de la vidéo, structuré spécifiquement pour une personne souhaitant créer des produits ou services commercialisables (applications web, jeux, assets 3D) avec l'IA et Claude Code.

---

### 1) Idée principale

La vidéo démontre la capacité des modèles d'IA avancés (associés à des agents de codage et au protocole **MCP**) à concevoir et exécuter automatiquement de A à Z des projets complexes et monétisables à partir d'un seul prompt :
1. **Un système d'exploitation Web complet (Web OS style macOS)** interactif (gestionnaire de fichiers, lecteurs audio, fenêtres, effets graphiques).
2. **Un jeu vidéo par navigateur 2D/3D (Three.js)** prêt à l'emploi avec menu, animations, contrôles et effets de parallaxe.
3. **Une animation 3D complète sous Blender** (modélisation d'un chiot, rigging, texturation, animation et rendu vidéo MP4).

L'auteur souligne que ces outils permettent d'automatiser le travail de développement et de création 3D, même si les modèles haut de gamme doivent être réservés aux tâches complexes pour optimiser les coûts.

---

### 2) Outils, sites et dépôts cités

* **Claude / Anthropic (Claude Code / Fable 5.2 / Opus 5.5)**
  * **Nom exact :** Claude / Anthropic (modèles Fable / Opus).
  * **Statut :** Payant (Tarif affiché : 8 $/million de tokens en entrée, 40 $/million de tokens en sortie pour Fable 5.2).
  * **Usage :** Agent de codage principal pour générer le code complet des applications, gérer l'environnement de développement local et exécuter des tâches automatisées.
* **Claude Mythos 5.2**
  * **Nom exact :** Claude Mythos 5.2 (Anthropic).
  * **Statut :** Accès restreint sur candidature (*Life Sciences* et *Cyber Verification Programs*).
  * **Usage :** Modèle réservé à la recherche en cybersécurité et biomédicale.
* **Blender MCP (Model Context Protocol)**
  * **Nom exact :** Blender MCP.
  * **Statut :** Gratuit / Open-source (Intégration d'agent).
  * **Usage :** Permet à l'IA de piloter directement l'interface et les scripts de Blender à distance pour créer des objets 3D, appliquer des matériaux/fourrures, animer la rig, régler les caméras et générer le rendu MP4 sans intervention humaine directe.
* **Three.js**
  * **Nom exact :** Three.js.
  * **Statut :** Gratuit (Bibliothèque JavaScript Open-source).
  * **Usage :** Moteur 3D/2D Web utilisé par l'IA pour programmer le jeu vidéo ("Fable Knight").
* **Stack Web Standard (HTML, CSS, JS, Python HTTP Server)**
  * **Statut :** Gratuit.
  * **Usage :** Déploiement et exécution locale du projet Web OS.

---

### 3) Astuces concrètes et réutilisables pour générer de la valeur

1. **Création d'applications Web interactives à vendre (Templates/SaaS) :**
   * Prompt type pour créer une interface Web OS : Demander à l'agent de créer un dossier de projet complet reproduisant l'interface d'un OS moderne en HTML/CSS/JS, incluant la gestion de fenêtres, un lecteur de musique fonctionnel et des fenêtres modales.
2. **Création de jeux Web (Web Games / Instant Games) :**
   * Utiliser Three.js couplé à un prompt demandant une mécanique de jeu complète (menus, niveaux, défilement parallaxe, contrôles clavier, effets visuels et bandes-sons intégrées).
3. **Automatisation de la création d'assets 3D et vidéos (Freelance 3D / Stock Video) :**
   * Grâce à **Blender MCP**, déléguer la création 3D complexe à l'agent : modélisation organique, génération du squelette (rigging), création de la scène (arbres, fleurs, ciel), animation des membres et rendu vidéo final en MP4 (24 FPS, 1080p).
4. **Gestion du niveau d'effort de l'agent (*Effort Level*) :**
   * Régler le paramètre d'effort sur **"Extra High"** lors du lancement de projets nécessitant du code lourd et sans erreur (jeu complet ou script 3D).
5. **Optimisation des coûts d'IA :**
   * Réserver les modèles très puissants et coûteux pour l'architecture initiale ou la résolution de problèmes bloquants, puis utiliser des modèles plus légers pour les ajustements légers d'interface utilisateur.

---

### 4) Chiffres de revenus annoncés

* **Revenus de vente ou de monétisation :** *Non précisé* (la vidéo est une démonstration technique de création de projets et ne détaille pas la revente directe).
* **Coûts de fonctionnement affichés par l'auteur (à titre indicatif) :**
  * *Crédits consommés au total sur son compte :* 76,33 $ *(affirmé par l'auteur)*.
  * *Consommation pour les 3 projets de la vidéo :* Augmentation de 6 % de sa limite hebdomadaire d'utilisation (passant de 9 % à 15 %) *(affirmé par l'auteur)*.

# GdMnqbGPlyY — « I Tested Fable 5.2 vs Opus 5.5 Building Websites, Apps, Motion Graphics (Unexpected Results) »

- Auteur : Jason Lee ; lien : https://youtu.be/GdMnqbGPlyY
- Envoyée par l'utilisateur ; résumée le 14/11/2026 par Gemini (via le relais, modèle gemini-3.5-flash)
- Les chiffres ci-dessous sont « affirmés par l'auteur », non vérifiés.

## Tri pour DIG16 (14/11)

Comparaison en anglais de Fable 5.2 et d'Opus 5.5 sur trois travaux faits avec Claude Code : la refonte d'un vieux site, une copie de Canva et une vidéo animée de 30 secondes ; avec la publicité de l'hébergeur Hostinger.

- **Fable « architecte » dans la session principale, Opus ou Sonnet « bâtisseurs » dans des sous-sessions** : déjà dans nos consignes (`connaissances/consignes-detaillees.md`, « Modèle à utiliser », conseil du 24/10 ; sous-agents avec le modèle choisi, déjà en place). Le réglage appartient à l'utilisateur.
- **Avec des références visuelles et une charte claires, Opus 5.5 fait aussi bien que Fable pour bien moins cher (d'après les essais de l'auteur)** : conforte notre méthode, déjà en place : photos et logo du client d'abord, couleur tirée du logo, skill `design-md-references`. Rien à changer.
- **Expliquer une demande par un enregistrement de l'écran commenté à la voix, au lieu de nombreuses captures** : À VOIR PAR CLAUDE. Idée absente de nos fiches ; aujourd'hui l'utilisateur envoie des captures une par une. À faire : vérifier d'abord si un fichier vidéo peut être envoyé dans la conversation depuis le téléphone ; si oui, faire un essai sur une courte vidéo avec les outils gratuits déjà notés dans `connaissances/boite-a-outils.md` (ffmpeg pour tirer des images, faster-whisper pour écrire ce qui est dit) ; si l'essai marche, proposer à l'utilisateur cette façon de montrer une correction de site et l'écrire dans les consignes. Si l'envoi d'une vidéo n'est pas possible, garder les captures.
- **Refonte d'un vieux site pris en exemple (car-part.com)** : déjà notre métier ; nouvelles démos en pause jusqu'au premier client payant.
- **Copie de Canva (application en ligne)** : écartée ; hors sujet, et copier l'outil d'une marque est contraire à notre règle (s'inspirer, ne jamais copier une identité).
- **Vidéo animée fabriquée par le code** : déjà chez nous (skill `motion-broll`, noté dans `connaissances/boite-a-outils.md`) ; nouvelles vidéos en pause jusqu'au premier client payant.
- **Hostinger, son connecteur et Hostinger Reach (payants, code de réduction de l'auteur)** : écartés, comme les fois précédentes ; nos sites sont sur Cloudflare Pages, au nom de chaque client, sans coût d'hébergement.
- **Higgsfield (images et plans générés)** : déjà en réserve et payant (`connaissances/reserve-prete.md`, lu le 16/10) ; seulement si un client paie des vidéos. Epidemic Sound (musique, payant) : écarté (budget 0 €).
- **Remises à zéro gratuites de la limite d'usage, à voir dans les réglages du compte** : non vérifié ; menu cité de mémoire par l'auteur, à lire sur la page d'aide officielle avant d'en parler à l'utilisateur.
- **Chiffres cités (41,61 $ contre 18,77 $ pour la refonte, 54,60 $ contre 47,62 $ pour la copie de Canva, 68,64 $ contre 22,31 $ pour la vidéo ; tarifs au million de jetons ; 45 millions de dollars par an pour le site pris en exemple ; prix Hostinger)** : affirmés par l'auteur, non vérifiés.

Conclusion : rien à installer ; une idée à étudier (l'enregistrement d'écran commenté pour montrer une correction), le reste est déjà en place, en réserve ou écarté.

## Résumé (Gemini)

Voici le résumé détaillé de la vidéo pour vous aider à optimiser l'utilisation de Claude Code et développer des projets informatiques ou des services rentables.

---

### 1) Idée principale
La vidéo compare de manière pratique l'utilisation de **Claude Fable 5.2** et **Claude Opus 5.5** via Claude Code pour créer des produits digitaux commercialisables (redesign de sites web existants, création d'applications web interactives/clones d'outils SaaS comme Canva, et génération de vidéos motion graphics en code). 

L'objectif est de démontrer comment optimiser ses coûts de développement : utiliser le modèle le plus cher (Fable 5.2) uniquement pour la réflexion et l'architecture, et déléguer le codage aux modèles plus abordables (Opus 5.5 / Sonnet 5.5) pour préserver ses marges financières.

---

### 2) Outils, sites et dépôts GitHub cités

*   **Claude Fable 5.2** *(Payant : 8 $ / 40 $ par million de tokens)* : Modèle le plus avancé d'Anthropic. Il excelle dans la réflexion complexe, l'architecture et possède de très bons choix esthétiques par défaut.
*   **Claude Opus 5.5** *(Payant : 4 $ / 20 $ par million de tokens)* : Modèle de travail quotidien, 2 fois moins cher que Fable 5.2, très efficace et rapide pour l'exécution de code.
*   **Claude Sonnet 5.5** *(Payant - prix exact non précisé)* : Cité comme modèle alternatif économique pour exécuter des tâches secondaires de codage ou de rédaction.
*   **Mythos 5.2, GPT-6 Astra, Gemini 4 Carbon** *(Statut tarifaire non précisé)* : Modèles d'IA cités lors de la présentation des benchmarks de performance.
*   **Car-part.com** *(Gratuit d'accès)* : Ancien site d'annonces de pièces auto d'occasion servant d'exemple pratique pour être entièrement re-designé et modernisé par l'IA.
*   **Hostinger** *(Payant : offre à partir de 2,79 $/mois ou 2,51 $/mois avec le code promo JASONLEE)* : Hébergeur web partenaire doté d'une intégration directe avec Claude pour déployer en ligne un site généré par l'IA en une seule commande textuelle.
*   **Hostinger Reach** *(Payant - détails non précisés)* : Outil d'email marketing assisté par IA d'Hostinger.
*   **Canva** *(Gratuit / Payant)* : Application de création graphique servant de modèle pour la création d'un clone web fonctionnel.
*   **Higgsfield MCP** *(Outil / Serveur MCP - statut tarifaire non précisé)* : Outil d'IA permettant de générer automatiquement des images et assets visuels intégrés dans le code des projets.
*   **Epidemic Sound** *(Payant)* : Banque sonore permettant d'associer une musique et des effets audio à des vidéos d'animations créées en code.
*   **Dépôts GitHub :** Aucun dépôt GitHub spécifique n'est cité dans la vidéo.

---

### 3) Astuces concrètes et réutilisables

1.  **Méthode "Architecte / Bâtisseur" (Nested Sessions / Sessions imbriquées) :**
    *   Utilisez **Fable 5.2** dans la session principale comme "l'Architecte" (pour définir le Business Model, l'UX/UI, la structure de l'application et la stratégie de marché).
    *   Créez ensuite des sous-sessions (*sub-sessions*) basées sur **Opus 5.5** ou **Sonnet 5.5** ("les Bâtisseurs") pour coder chaque partie spécifique (écrans de l'application, landing page, rédaction pour les stores).
    *   Laissez Fable 5.2 contrôler et assembler le travail final.
2.  **Prompt par enregistrement d'écran (Screen Recording + Voix off) :**
    *   Plutôt que d'écrire de longs prompts ou de prendre des dizaines de captures d'écran pour cloner une application, enregistrez votre écran tout en navigant sur l'application cible et expliquez vos besoins à l'oral. Donnez ce fichier vidéo directement à Claude Code.
3.  **Gestion des coûts selon le niveau de directive :**
    *   Si vous lancez un projet sans références visuelles précises (*Prompt simple / One-shot*), Fable 5.2 choisira de meilleurs designs et finitions visuelles par défaut.
    *   Si vous fournissez vos propres références visuelles et une charte claire, **Opus 5.5** produira un résultat équivalent pour un coût 2 à 3 fois inférieur.
4.  **Déploiement direct via API/Connecteurs :**
    *   Raccordez vos outils de déploiement (ex: connecteur Hostinger dans Claude) pour mettre votre site ou SaaS en ligne sur un serveur réel directement depuis l'interface de discussion de Claude.
5.  **Utiliser les "Limit Resets" d'Anthropic :**
    *   Vérifiez régulièrement dans *Settings > Usage* sur votre compte Anthropic : vous pouvez bénéficier de réinitialisations gratuites de votre limite d'utilisation de 5 heures pour Fable.

---

### 4) Chiffres de revenus et coûts annoncés *(affirmés par l'auteur)*

*   **Revenu annuel de Car-part.com :** Environ **45 millions de dollars par an** *(affirmé par l'auteur)*.
*   **Coûts et temps de génération par l'IA selon les tâches *(affirmés par l'auteur)* :**
    *   *Redesign de site web (Car-part.com) :*
        *   Fable 5.2 : **41,61 $** (Durée : 92 min)
        *   Opus 5.5 : **18,77 $** (Durée : 40 min)
    *   *Création d'un clone fonctionnel de Canva (Kanva) :*
        *   Fable 5.2 : **54,60 $** (Durée : 104 min)
        *   Opus 5.5 : **47,62 $** (Durée : 92 min)
    *   *Création d'une vidéo de lancement Motion Graphics (30 sec en code) :*
        *   Fable 5.2 : **68,64 $** (Durée : 137 min)
        *   Opus 5.5 : **22,31 $** (Durée : 84 min)

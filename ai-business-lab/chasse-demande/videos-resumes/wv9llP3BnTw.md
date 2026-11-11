# wv9llP3BnTw — « CLAUDE 2.0 : ces nouveautés changent TOUT »

- Auteur : Henri · ExplorIA ; lien : https://youtu.be/wv9llP3BnTw
- Envoyée par l'utilisateur le 11/11/2026 ; résumée le 11/11 par Gemini (via le relais, modèle gemini-3.5-flash)
- Les prix et les chiffres ci-dessous sont « affirmés par l'auteur », non vérifiés.

## Tri pour DIG16 (11/11)

- **Rien à installer.** La vidéo présente des fonctions de Claude (documents, présentations et maquettes modifiables, tableaux Google Sheets, sous-tâches en parallèle, question posée pendant un travail, suivi depuis le téléphone, « Mods »). Les prix et les noms d'offres cités sont « affirmés par l'auteur », non vérifiés à la source.
- **Déjà en place chez nous** : pages et documents publiés (Artifacts), conversations de service en parallèle, suivi depuis le téléphone (conversation dans le cloud).
- **À retenir pour l'utilisateur** : poser une question pendant qu'un travail tourne, sans l'interrompre (commande citée par l'auteur ; à vérifier dans l'aide officielle avant de la lui conseiller).
- **Écartés** : formation et accompagnement payants de l'auteur ; « Mod » décoratif `agent-crew` (sans utilité pour DIG16).
- **Chiffres** (clients de l'auteur, mini-application « compte rendu de chantier » vendue plus de 5 000 €) : affirmés par l'auteur. Rejoint l'idée du 19/10 (automatisations pour artisans, `64` § 0) : rien construit sans preuve de la demande (règle n° 1).

## Résumé (Gemini)

Voici le résumé structuré de la vidéo pour vous aider à tirer parti de Claude 2.0 et Claude Code :

---

### 1) Idée principale
La vidéo présente les **10 nouveautés majeures de Claude 2.0 / Claude Code**. L'assistant IA évolue d'un simple générateur de texte vers un **système agentique autonome et unifié**, capable de créer des documents éditables, des présentations, des maquettes Web, de modifier directement vos fichiers Google Sheets, de gérer des sous-tâches en parallèle et d'être personnalisé via des "Mods". L'objectif est d'accélérer considérablement la productivité pour vendre des prestations de services IA ou optimiser la gestion d'une entreprise.

---

### 2) Outils, sites et dépôts GitHub cités

*   **Claude 2.0 / Claude Code (Anthropic)** *(Modèle économique : Freemium)* :
    *   *Gratuit* : Accès aux fonctions visuelles de base (Claude Docs, Claude Slides, Claude Design).
    *   *Pro (~20 $/mois)* : Accès à Claude Code, aux sous-tâches autonomes et à la création de Mods.
    *   *Max / Ultra (jusqu'à 200 $/mois)* : Pour faire sauter les limites d'utilisation hebdomadaires lors de gros volumes de travail.
*   **Opus 5.5 / Sonnet 5.5** *(Inclus dans les abonnements Claude)* : Modèles d'IA intégrés dans l'interface unique pour gérer les tâches complexes ou rapides.
*   **Google Sheets & Gmail** *(Gratuit / Freemium)* : Connecteurs intégrés à Claude pour modifier directement les tableaux et rédiger des e-mails.
*   **AWS, Salesforce, Snowflake** *(Payant / Outils d'entreprise)* : Sources de données connectables aux tableaux de bord *Claude Dashboard*.
*   **ExplorIA Labs** *(Payant - Agence B2B)* : Agence de l'auteur accompagnant les entreprises dans l'intégration de systèmes d'agents IA.
*   **Le Cercle (par ExplorIA Labs)** *(Payant - Formation & Coaching 1-to-1)* : Programme d'accompagnement pour aider des indépendants à lancer leur activité d'intégration/conseil IA.
*   **GitHub - `agent-crew`** (par l'utilisateur `bebi1337`) *(Gratuit / Open-source)* : Dépôt de communauté permettant d'installer un "Mod" affichant des petits personnages animés représentant les sous-agents travaillant en arrière-plan.

---

### 3) Astuces concrètes et réutilisables

1.  **Création de documents & présentations en 1 clic :**
    *   Utilisez le mot-clé **`Claude Docs`** pour générer un document texte riche et éditable par blocs dans un panneau latéral (Artefact). Vous pouvez sélectionner une section ou un tableau précis et demander à Claude de modifier *uniquement* cet élément.
    *   Utilisez **`/slides`** ou **`Claude Slides`** pour convertir un texte ou une proposition commerciale en une présentation visuelle (éditable et exportable en PowerPoint/PDF).
    *   Demandez **`design`** ou **`Claude Design`** pour transformer un cahier des charges en une maquette visuelle interactive d'un site web ou d'une application mobile.
2.  **Gestion directe de Google Sheets :**
    *   Fournissez le lien de votre fichier Google Sheets dans le prompt. Claude peut y créer un nouvel onglet, écrire de véritables formules de calcul, calculer des retards de paiement et appliquer des mises en forme conditionnelles (ex: couleurs de priorité) sans écraser le fichier d'origine.
3.  **Sessions imbriquées (Sous-tâches en parallèle) :**
    *   Demandez à Claude Code de traiter un dossier contenant plusieurs fichiers complexes (ex: 4 devis PDF de mutuelle) en lançant une **sous-session d'analyse autonome par fichier**. Une "Session Maître" récupère ensuite les résultats pour synthétiser un comparatif global.
4.  **Poser des questions à la volée avec `/btw` (By The Way) :**
    *   Pendant que Claude exécute une tâche lourde dans la fenêtre principale, tapez **`/btw [votre question]`** dans la barre de chat. La réponse s'affichera dans un volet secondaire à droite **sans interrompre ni relancer le travail en cours**.
5.  **Contrôle à distance depuis son smartphone (Remote Control) :**
    *   Activez l'option *Remote Control* dans les paramètres de Claude Code. Vous pouvez ensuite suivre, relancer ou poser des questions sur les sessions en cours sur votre ordinateur directement depuis votre téléphone portable.
    *   *Option recommandée :* Activez l'option "Maintenir l'ordinateur éveillé pendant que Claude travaille" dans les paramètres pour éviter que la mise en veille ne coupe le traitement.
6.  **Créer des "Mods" personnalisés sans coder :**
    *   Vous pouvez décrire en langage naturel l'interface que vous voulez ajouter à Claude (ex: *"Crée un panneau à droite avec un robot en SVG animé qui dort quand tu es inactif et réfléchit quand tu travailles"*). Claude génère le code du Mod en arrière-plan et l'installe dans votre environnement.

---

### 4) Chiffres de revenus annoncés (*affirmés par l'auteur*)

*   **Étude de cas Mélissa (MCD Community / Client ExplorIA Labs) :** *"x2 de chiffre d'affaires en 2 mois"* grâce à l'automatisation de la prospection et des calendriers éditoriaux.
*   **Gain de temps (Jérémie Calnaud) :** *"8 heures récupérées chaque semaine"*.
*   **Vente de prestation IA (Exemple sur la page du programme "Le Cercle") :** Une mini-app (compte-rendu de chantier) est mentionnée comme ayant été *"vendue plus de 5 000 € à une entreprise de rénovation"*.

# J'arrête Claude pour le combo Cursor + Codex

Vidéo : https://youtu.be/wi40rDb-4pI · durée 16:53 · résumé Gemini (gemini-3-flash-preview) du 2026-09-29
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé de la vidéo pour un utilisateur souhaitant optimiser son usage des agents d'IA de codage (comme Claude Code ou Cursor) dans un but entrepreneurial.

### 1) Idée principale
L'auteur analyse le retour en force de **Cursor** (couplé au modèle **Grok**) comme l'outil de développement IA le plus productif du moment. Il explique comment il a délaissé Claude pour Cursor parce que ce dernier est devenu une véritable interface d'agents capable de gérer des serveurs distants (VPS), de lancer des sous-agents spécialisés et de prévisualiser des modifications en temps réel, dépassant le simple cadre de l'éditeur de code (IDE) classique.

### 2) Outils, sites et dépôts cités
*   **Cursor (version "Origin")** (Payant/Abonnement) : IDE qui a évolué vers une interface d'agent complète. Il permet de piloter des tâches complexes sans interface de code traditionnelle.
*   **Grok 4.6** (Modèle utilisé via Cursor) : Cité par l'auteur comme le modèle le plus intelligent et rentable actuellement pour les tâches de code (Note : l'auteur cite "4.6", probablement une confusion avec une version spécifique ou Grok-2).
*   **Codex** (Payant) : Agent/système de codage utilisé par l'auteur pour les tâches d'architecture lourde (qualifié de "Ferrari" de l'IA).
*   **agent-burn** (Dépôt GitHub - Open Source) : Outil créé par l'auteur pour monitorer en temps réel sa consommation de tokens et le coût financier de ses agents IA.
*   **DeepSWE** (Site web) : Benchmark de référence comparant l'efficacité et le coût des différents agents de codage (Claude, GPT, Grok).
*   **Portly** (Application locale) : Outil utilisé par l'auteur pour gérer ses processus et serveurs locaux sans encombrer son terminal de développement.
*   **Lumail.io** : Le SaaS principal de l'auteur, cité comme exemple de produit générant des revenus et développé entièrement via ces outils.
*   **mlv.sh/fa** : Site de formation de l'auteur pour apprendre à coder avec l'IA.

### 3) Astuces concrètes et réutilisables
*   **Coder sur VPS (Serveur Distant) :** Pour éviter que les agents IA ne saturent le processeur (CPU) de votre ordinateur local, connectez Cursor à un VPS. L'IA travaille sur le serveur, laissant votre machine fluide.
*   **Le "Multi-tasking" d'instructions :** Sur l'interface de prévisualisation (Browser intégré), vous pouvez sélectionner plusieurs éléments et envoyer une file d'attente (queue) de modifications à l'IA sans attendre qu'elle finisse la première tâche.
*   **L'usage de Sous-Agents :** Ne demandez pas tout à un seul agent. Lancez un "Sub-agent" spécialisé (via la commande `/side` ou des prompts dédiés) pour des tâches de vérification, de revue de code ou de cohérence visuelle pendant que vous continuez à bâtir.
*   **Arbitrage des modèles :** Utilisez Grok (en mode "High Fast") pour les tâches quotidiennes rapides et gardez les modèles plus coûteux (comme Codex ou GPT-4) pour les problèmes d'architecture complexes.

### 4) Chiffres annoncés (Affirmés par l'auteur)
*   **Dépenses en tokens IA :** L'auteur affiche un coût total de **17 400 $** (spend) sur son dashboard pour le développement de ses projets.
*   **Volume de tokens :** Plus de **61,2 milliards de tokens** consommés au total.
*   **Productivité :** L'auteur affirme que sa configuration permet d'économiser **500 heures de Recherche & Développement (R&D)**.
*   **Revenus :** Non précisés (l'auteur mentionne que Lumail est son "SaaS principal", mais ne donne pas de chiffre d'affaires exact dans ce clip).

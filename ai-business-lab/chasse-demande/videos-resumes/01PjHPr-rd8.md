# 01PjHPr-rd8 — « 6 choses folles créées avec Claude Fable 5.2 »

- Auteur : Erwan | IA ; lien : https://youtu.be/01PjHPr-rd8
- Envoyée par l'utilisateur ; résumée le 14/11/2026 par Gemini (via le relais, modèle gemini-3.5-flash)
- Les chiffres ci-dessous sont « affirmés par l'auteur », non vérifiés.

## Tri pour DIG16 (14/11)

Vidéo de démonstrations : six créations faites par d'autres avec Claude Fable 5.2 (jeux en 3D, voiture en 3D dans Blender, circuit électronique, pièces mécaniques), puis des conseils pour bien diriger ce modèle sans vider son quota.

- **Jeux et scènes 3D, Blender piloté par script** : en réserve, déjà noté (`connaissances/reserve-prete.md`, ligne « Blender piloté par Claude Code », du 09/11) ; à ressortir après le premier client payant, à la reprise des nouvelles vidéos. Three.js : déjà chez nous (skills `threejs-web` et `threejs-animation`).
- **KiCad (circuits) et Autodesk Inventor (pièces mécaniques, payant)** : écartés, hors sujet pour des sites internet (déjà écartés le 11/11).
- **Sous-agents et relecteurs qui vérifient chaque partie** : déjà en place (relecteur en lecture seule du contrôle `44-controle-qualite.md`, `outils/controle_global.py`).
- **Décrire précisément le résultat attendu, avec des images de référence** : déjà notre méthode (questionnaire client, photos et logo du client d'abord, skill `design-md-references`).
- **Fable pour concevoir, Opus 5.5 pour exécuter ; le niveau d'effort règle la réflexion, pas la longueur des réponses** : déjà dans nos consignes (`connaissances/consignes-detaillees.md`, « Modèle à utiliser », conseil du 24/10 ; même idée notée le 11/11). Le réglage appartient à l'utilisateur.
- **« Enlever avant d'ajouter » : faire relire `CLAUDE.md` et les skills à la lumière du guide officiel d'Anthropic pour Fable 5.2, et retirer les règles devenues inutiles** : À VOIR PAR CLAUDE. Nos consignes ont été allégées le 21/10 et le 10/11, mais sans comparaison avec ce guide. À faire : lire le guide officiel de rédaction des consignes pour Fable 5.2 (documentation d'Anthropic, page à retrouver et à dater à la source), relire `.claude/CLAUDE.md` et la liste des skills, dresser la liste des règles en double ou écrites pour d'anciens modèles, et la proposer à l'utilisateur ; ne rien retirer sans son accord (ces consignes sont les siennes).
- **Coûts cités (environ 550 $ pour un jeu fabriqué en 8 heures, forfaits à 20 $ par mois, accès à Fable limité dans le temps)** : affirmés par l'auteur, non vérifiés ; aucun achat (budget 0 €).

Conclusion : rien à installer ; une seule idée à étudier (relecture de nos consignes avec le guide officiel de Fable 5.2), le reste est déjà en place, en réserve ou hors sujet.

## Résumé (Gemini)

Voici le résumé structuré de la vidéo, rédigé à l'intention de toute personne souhaitant exploiter **Claude Code** et l'IA pour développer des projets à valeur ajoutée.

---

### 1) Idée principale

La vidéo présente les capacités du modèle de langage **Claude Fable 5.2** d'Anthropic à travers six démonstrations impressionnantes (création autonome de jeux 3D, modélisation mécanique et électronique, animations guidées par du code). L'auteur explique que pour rentabiliser et maximiser l'usage de ce modèle extrêmement puissant (mais gourmand en quotas), il ne faut pas chercher de « prompt magique », mais adopter une méthodologie rigoureuse : automatiser l'auto-vérification par des sous-agents, auditer ses règles de prompting existantes et répartir intelligemment l'effort entre Fable 5.2 et des modèles plus économiques comme Opus 5.5.

---

### 2) Outils, sites et logiciels cités

*   **Claude / Claude Code / Claude Fable 5.2 / Opus 5.5** (Anthropic)
    *   *Statut :* Payant (sur abonnement Pro à 20 $/mois, Max/Ultra, ou à la consommation d'API). Accessibilité temporairement offerte/incluse selon les offres.
    *   *Usage :* Modèles d'IA et environnement agentique (Claude Code) pour la génération de code, la conception 3D, le raisonnement complexe et l'exécution de tâches autonomes long terme.
*   **Blender**
    *   *Statut :* Gratuit (Open Source).
    *   *Usage :* Modélisation, animation et rendu 3D pilotés intégralement en Python généré par l'IA.
*   **KiCad**
    *   *Statut :* Gratuit (Open Source).
    *   *Usage :* Conception de circuits imprimés (PCB) et d'électronique.
*   **Autodesk Inventor**
    *   *Statut :* Payant.
    *   *Usage :* Conception mécanique assistée par ordinateur (CAO/CAD) pour la création de boîtiers/pièces physiques.
*   **Three.js**
    *   *Statut :* Gratuit (Open Source).
    *   *Usage :* Moteur et bibliothèque JavaScript pour afficher des scènes 3D de haute qualité directement dans un navigateur web.
*   **Python**
    *   *Statut :* Gratuit (Open Source).
    *   *Usage :* Langage de programmation utilisé pour scripter et automatiser la création d'animations 3D image par image dans Blender.
*   **Guide de prompting d'Anthropic (`platform.claude.com`)**
    *   *Statut :* Gratuit (Documentation en ligne).
    *   *Usage :* Documentation officielle contenant les meilleures pratiques d'ingénierie de prompt pour Fable 5.2.
*   **X (Twitter)**
    *   *Statut :* Gratuit / Payant.
    *   *Usage :* Plateforme où ont été publiées les démonstrations de la communauté citées dans la vidéo.

---

### 3) Astuces concrètes et réutilisables pour vos projets avec Claude Code

1.  **Nettoyer avant d'ajouter (« Enlever avant d'ajouter ») :**
    *   *Principe :* Fable 5.2 suit les consignes au pied de la lettre. Vos anciennes instructions personnalisées (`CLAUDE.md`, mémoire, projets, skills) conçues pour d'anciens modèles risquent d'augmenter le coût en tokens ou d'engendrer des effets indésirables.
    *   *Astuce Claude Code :* Lancez un prompt d'audit automatique demandant au modèle de lire la documentation officielle d'Anthropic sur Fable 5.2, puis d'analyser votre fichier `CLAUDE.md` et vos *skills* pour relever les règles obsolètes sans rien modifier sans votre accord.

2.  **Activer le système de sous-agents et de vérificateurs :**
    *   Pour faire exécuter des projets complexes en autonomie (ex: jeux vidéo, rendus 3D), donnez au modèle la possibilité d'auto-évaluer son travail.
    *   *Mots-clés à intégrer au prompt :* `"Use subagents and critics to build and verify each part"` (*« Utilise des sous-agents et des critiques pour construire et vérifier chaque pièce »*).

3.  **Spécifier clairement l'état final et les étapes :**
    *   Ne vous contentez pas de décrire l'idée : définissez exactement ce à quoi ressemble le travail terminé et fournissez des images de référence ou des plans techniques (blueprints) quand c'est possible.

4.  **Optimiser le niveau d'effort et la longueur des réponses :**
    *   Le curseur d'effort (Low, Medium, High, XHigh, Max) ajuste la **profondeur de réflexion** de l'IA, mais **pas la longueur** de la réponse générée.
    *   Pour obtenir des réponses concises, indiquez-le explicitement dans le texte du prompt (ex: *"Réponds en trois lignes"*).

5.  **Adopter une stratégie hybride de répartition des modèles (Économie de coûts/quotas) :**
    *   Utilisez **Claude Fable 5.2** uniquement pour la phase initiale d'architecture, d'imagination et de conception du plan global (*« bâtir »*).
    *   Basculez ensuite sur **Claude Opus 5.5** (nettement moins cher et très capable) pour la phase d'exécution et de construction fine (*« construire »*).
    *   Par défaut, commencez vos tâches sur Opus 5.5. Ne montez sur Fable 5.2 que si Opus 5.5 échoue, même avec un effort réglé au maximum.

---

### 4) Chiffres de revenus annoncés

*   **Chiffres de revenus / gains financiers :** *Non précisé* (aucun chiffre d'affaires ou revenu financier personnel n'est affirmé par l'auteur dans la vidéo).
*   **Coûts techniques et métriques cités (affirmé par l'auteur / sources des démos) :**
    *   *Démo jeu de tir FPS (8h d'exécution sans intervention) :* ~550 $ de consommation API (~2,7 millions de tokens écrits / 445 millions de tokens lus).
    *   *Démo Bugatti 3D (2h30 d'exécution) :* Coût financier non précisé.
    *   *Forfait Pro :* 20 $/mois (accès à Fable inclus de manière limitée/temporaire jusqu'au 16 novembre 2026).
    *   *Forfaits Max et Ultra :* Accès standard incluant Fable jusqu'à 50 % de la limite hebdomadaire.

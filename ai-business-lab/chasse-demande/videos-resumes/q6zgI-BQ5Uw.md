# q6zgI-BQ5Uw — « Claude Fable 5.2 is Insane... These are the 9 HUGE Use Cases »

- Auteur : Jack Roberts ; lien : https://youtu.be/q6zgI-BQ5Uw
- Envoyée par l'utilisateur ; résumée le 14/11/2026 par Gemini (via le relais, modèle gemini-3-flash-preview)
- Les chiffres ci-dessous sont « affirmés par l'auteur », non vérifiés.

## Tri pour DIG16 (14/11)

Vidéo en anglais de Jack Roberts (auteur déjà trié les 15/10 et 25/10) : neuf usages de Fable 5.2 (jeux, sites, 3D dans Blender, montage de vidéos courtes), avec la publicité de ses propres systèmes payants et de Higgsfield.

- **Sites « haut de gamme » fabriqués par l'IA** : déjà notre métier et nos outils (skills de design, `gsap-*`, `threejs-*`) ; rien de nouveau dans le résumé.
- **Documents, présentations, tableaux et pages partagés par lien depuis Claude (« Artifacts »)** : déjà en place et déjà utilisés (pages privées publiées par lien, noté le 25/10 dans `46-registre-videos.md`). Pour un client, nos documents passent par le kit client (`outils/kit_client.py`) et le Drive « Dig » : rien à changer.
- **Copier l'interface d'une application à partir de captures d'écran** : écarté ; contraire à notre règle (s'inspirer, ne jamais copier l'identité d'une marque).
- **Essayer une page sur son téléphone par un QR code, puis « ajouter à l'écran d'accueil »** : sans objet pour nous ; l'utilisateur ouvre déjà les liens d'aperçu en ligne sur son téléphone, et `outils/test_pages.py` contrôle les largeurs de téléphone.
- **Étudier les vidéos qui marchent sur six points (émotion, 3 premières secondes, images, son, histoire, commentaires)** : déjà couvert par le skill `ig-viral` ; nouveaux contenus vidéo en pause jusqu'au premier client payant.
- **Blender piloté par des scripts écrits par l'IA** : en réserve, déjà noté le 09/11 (`connaissances/reserve-prete.md`) ; à la reprise des nouvelles vidéos, après le premier client payant.
- **Higgsfield et son connecteur (payant, promotion annoncée par l'auteur)** : déjà en réserve comme payant (`connaissances/reserve-prete.md`, lu le 16/10) ; écarté tant que le budget est de 0 €.
- **Glaido et « Stacked Shorts System » (systèmes payants de l'auteur pour les vidéos courtes)** : écartés (publicité de l'auteur, payants, vidéos en pause).
- **Jeux vidéo** : écartés, hors sujet.
- **Vercel** : déjà utilisé chez nous (relais des résumés) ; simple hébergeur des exemples de l'auteur.
- **Chiffres cités (79 300 vues, jeu « équivalent à 42 $ », entreprise revendue, « milliers de dollars » de monteur économisés, promotion de 60 %)** : affirmés par l'auteur, non vérifiés ; à ne jamais reprendre. Le résumé décrit Fable 5.2 comme « une couche au-dessus de Claude » : formulation du résumé automatique, non vérifiée.

Conclusion : rien à installer, rien à changer.

## Résumé (Gemini)

Voici un résumé de la vidéo pour une exploitation lucrative avec Claude Code et l'IA :

### 1) Idée principale
L'utilisation de **Fable 5.2** (une couche optimisée au-dessus de Claude) pour automatiser la création de produits numériques à haute valeur ajoutée : jeux vidéo, sites web premium, rendus 3D complexes et systèmes de montage vidéo automatisés. L'objectif est de transformer des instructions simples (prompts) en actifs commercialisables ou en outils de productivité pour entreprises.

### 2) Outils, sites et dépôts cités
*   **Fable 5.2** : Basé sur Claude d'Anthropic. (Payant/Abonnement). Sert à générer du code complexe pour des jeux, des sites web et des scripts 3D.
*   **Claude Office 2.0 (Artifacts)** : Inclus dans Claude. (Gratuit/Freemium). Remplace la suite Office (Docs, Slides, Sheets) et ajoute des fonctions de Design, Data et Whiteboard (tableau blanc interactif).
*   **Higgfield MCP / Higgfield AI** : (Payant - mention d'une promotion de -60%). Utilisé comme connecteur dans Claude pour générer des images et vidéos professionnelles intégrées directement dans les projets de code.
*   **Blender** : (Gratuit - Open Source). Logiciel de création 3D. Fable 5.2 est utilisé pour écrire les scripts permettant de modéliser des objets (ex: montres, voitures) sans manipuler le logiciel manuellement.
*   **Glaido / Glaido Podcast** : (Payant - système de l'auteur). Outil pour transformer des podcasts longs en "Shorts" (vidéos courtes) de manière automatisée.
*   **Stacked Shorts System** : (Payant - mentionné comme disponible en lien). Pipeline de création et de gestion de contenu viral automatisé.
*   **Vercel** : (Gratuit/Payant selon l'usage). Cité implicitement via les URLs des exemples pour l'hébergement des applications générées.

### 3) Astuces concrètes et réutilisables
*   **Clonage d'applications** : Pour répliquer une interface, l'auteur conseille de prendre des captures d'écran d'une application existante et de demander à Fable 5.2 de générer le code correspondant (UI/UX et logique).
*   **Transformation en Web App mobile** : Pour tester un jeu ou une app sur smartphone : générer un QR code de l'URL locale, l'ouvrir sur mobile (sur le même Wi-Fi), puis faire "Ajouter à l'écran d'accueil" pour obtenir une icône d'application native.
*   **Ingénierie inverse marketing** : Pour créer une publicité virale, analyser les succès existants sur 6 critères : l'émotion, les 3 premières secondes, les visuels, l'audio, l'histoire et les points forts des commentaires.
*   **Blender via Code** : Utiliser l'IA pour générer des fichiers `.py` (Python) à exécuter dans Blender pour créer des animations 3D complexes (ex: éclaté d'un produit) sans être expert en modélisation.
*   **Collaboration via Artifacts** : Partager les fenêtres "Artifacts" de Claude avec des clients ou partenaires pour une édition en temps réel (stratégie, tableaux de bord).

### 4) Chiffres de revenus et performances
*   **79,3K vues** : Performance affichée sur un tableau de bord pour un pipeline de vidéos courtes automatisées (affirmé par l'auteur).
*   **42 $** : Coût équivalent estimé pour le développement d'un jeu de aquarium (affirmé par l'auteur).
*   **"J'ai construit et vendu ma dernière startup tech"** : L'auteur affirme avoir déjà réalisé une sortie (exit) financière, bien que le montant exact ne soit **non précisé**.
*   **Économie de "milliers de dollars"** : L'auteur affirme que son système d'IA remplace un monteur vidéo humain qu'il payait très cher pour ses réseaux sociaux.

# stn5BMpT4FU — « Photoshop GRATUIT recréé avec Claude… j'ai testé »

- Auteur : ROBONOMIC IA ; lien : https://youtu.be/stn5BMpT4FU
- Envoyée par l'utilisateur le 15/10/2026 ; résumée le 15/10 par Gemini (gemini-3.1-flash-lite, via le relais)

### 1) Idée principale
La vidéo présente **ArtCraft**, une suite logicielle gratuite comprenant 12 outils qui imitent les interfaces et les fonctionnalités des logiciels payants leaders du marché (Adobe, Microsoft, Autodesk). L'idée est de montrer qu'il est désormais possible d'obtenir des outils professionnels équivalents sans payer d'abonnement, grâce au code généré par des agents d'IA (Claude Opus 5.5). L'auteur souligne toutefois qu'il s'agit d'une solution "early alpha" (en développement précoce), donc moins fiable pour une utilisation professionnelle intensive.

### 2) Liste des outils et dépôts cités
*   **ArtCraft** (Gratuit) : Suite de 12 logiciels imitant les outils Adobe, Microsoft et Autodesk.
*   **ArtCraft Launcher** (Gratuit) : Installateur unique pour les 12 applications de la suite.
*   **Site officiel (getartcraft.com)** (Gratuit) : Source unique et sécurisée pour télécharger les outils.
*   **GitHub (dépôt ArtCraft)** (Gratuit) : Source alternative officielle pour télécharger le code et vérifier l'intégrité des fichiers.

**Les 12 applications (toutes gratuites) :**
1.  **PhotoCraft** : Remplace Photoshop (retouche d'image).
2.  **VectorCraft** : Remplace Illustrator (dessin vectoriel).
3.  **LightCraft** : Remplace Lightroom (développement photo RAW).
4.  **DesignCraft** : Remplace InDesign (mise en page).
5.  **FilmCraft** : Remplace Premiere Pro (montage vidéo).
6.  **EffectCraft** : Remplace After Effects (effets spéciaux).
7.  **SoundCraft** : Remplace Pro Tools (montage audio).
8.  **WordCraft** : Remplace Word (traitement de texte).
9.  **DeckCraft** : Remplace PowerPoint (présentations).
10. **GridCraft** : Remplace Excel (tableurs).
11. **PdfCraft** : Remplace Acrobat Pro (gestion PDF).
12. **CADCraft** : Remplace AutoCAD (conception 3D).

### 3) Astuces concrètes et réutilisables
*   **Vérification de l'intégrité (Empreinte) :** Pour s'assurer qu'un logiciel gratuit n'est pas corrompu ou piégé, vérifiez son empreinte (hash). Sur **Mac**, utilisez la commande `shasum -a 256 [fichier.dmg]` dans le terminal et comparez le résultat avec l'empreinte affichée sur le site officiel. Sur **Windows**, utilisez `certutil -hashfile [fichier] SHA256`.
*   **Sécurité logicielle :** Ne désactivez jamais la protection de votre système pour forcer l'installation d'une application. Attendez une version signée ou officielle.
*   **Méthode de travail IA :** Utilisez des outils comme le *MCP (Model Context Protocol)* qui permet à une IA (comme Claude) de piloter directement un logiciel (ouvrir, appliquer des réglages, exporter en série sur des centaines de fichiers).
*   **Gestion des fichiers :** Travaillez toujours sur une copie de vos fichiers originaux, car certaines applications en "alpha" peuvent modifier les données directement.
*   **Interopérabilité :** Privilégiez les formats de fichiers standards (.psd, .docx, .xlsx, .svg) pour garantir que votre travail soit lisible par les logiciels professionnels classiques.

### 4) Chiffres et coûts (affirmés par l'auteur)
*   **Coût annuel évité pour la suite totale :** Plus de **2 000 € par an** (économies potentielles en remplaçant les abonnements payants).
*   **Coûts des solutions payantes (référence au 13/10/2026) :**
    *   Microsoft 365 Personnel : **99 €/an**.
    *   Photoshop + Premiere : **629 €/an**.
    *   Creative Cloud Pro + Microsoft 365 : **1 042,80 €/an**.
    *   Pack complet Adobe (7 applis) + Office : **2 134,92 €/an**.
    *   AutoCAD seul : **2 184 € HT/an**.
*   **Temps de développement par l'IA :** 140 à 220 heures de travail d'agents (soit 25 à 40 heures réelles) pour atteindre 95 % des fonctions d'un logiciel original.
*   **Performance (auto-évaluation) :** VectorCraft est estimé à **65 %** du chemin pour remplacer Illustrator ; FilmCraft à **56 %** pour Premiere Pro ; GridCraft à **50 %** pour Excel. 
*   *Note : Le revenu généré légalement avec ces outils n'est pas précisé dans la vidéo.*

## Tri DIG16 (15/10/2026)

**Écarté** : suite ArtCraft (12 copies gratuites d'Adobe, Microsoft et AutoCAD, en version « alpha » selon l'auteur lui-même). DIG16 ne paie aucun de ces logiciels : visuels, PDF et vidéos sont produits par nos propres scripts (Playwright, ffmpeg, `outils/marque/`) et le connecteur Canva ; aucun gain à installer des applications de bureau non signées. **Déjà en place** : vérifier un programme avant de l'installer (lecture complète, refus des programmes qui se mettent à jour seuls) ; travailler sur une copie (tout est versionné dans git). Prix des abonnements Adobe et Microsoft : affirmés par l'auteur, non vérifiés.

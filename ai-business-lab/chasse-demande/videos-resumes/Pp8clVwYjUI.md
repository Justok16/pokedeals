# Pp8clVwYjUI — « Stop les outils SEO hors de prix : ce plugin Claude est gratuit »

- Auteur : Melvynx ; lien : https://youtu.be/Pp8clVwYjUI
- Envoyée par l'utilisateur ; résumée le 13/11/2026 par Gemini (via le relais, modèle gemini-3.5-flash)
- Les chiffres ci-dessous sont « affirmés par l'auteur », non vérifiés.

## Tri pour DIG16 (13/11)

Court format : le plugin gratuit `claude-seo` (dépôt AgriciDaniel/claude-seo, licence MIT) présenté comme remplaçant d'outils de référencement payants.

- **Déjà chez nous** depuis le 26/10 (`connaissances/boite-a-outils.md`) : la partie utile à DIG16 est installée (skill `seo-local` : fiche Google, coordonnées identiques partout, avis, données locales). Le reste du plugin est en réserve.
- **Prix des outils payants cités** : affirmés par l'auteur, non vérifiés ; sans objet pour nous (budget 0 €, OpenSEO et OpenRush déjà branchés).
- **Écarté** : la plateforme et la bibliothèque de l'auteur (publicité pour ses contenus).

Conclusion : rien à installer.

## Résumé (Gemini)

Voici le résumé détaillé de la vidéo :

---

### 1) Idée principale
Économiser les frais mensuels d'outils SEO propriétaires en utilisant **Claude Code** et le plugin open source **`claude-seo`**. Cet outil gratuit déploie jusqu'à 17 agents IA en parallèle pour auditer un site web, établir un plan d'action priorisé, générer les fichiers techniques requis et optimiser le site pour la recherche par IA (GEO / AI Search) afin d'apparaître dans les réponses de ChatGPT, Claude et Gemini.

---

### 2) Outils, sites et dépôts GitHub cités

*   **Semrush**
    *   **Statut :** Payant (~139 $/mois)
    *   **Rôle :** Outil d'analyse SEO traditionnel (cité à titre de comparaison pour montrer les économies réalisables).
*   **Ahrefs**
    *   **Statut :** Payant (~129 $/mois)
    *   **Rôle :** Outil d'analyse de backlinks et SEO (cité à titre de comparaison).
*   **Claude Code**
    *   **Statut :** Gratuit / Inclus dans l'écosystème Anthropic (*modalités de prix exactes non précisées dans la vidéo*)
    *   **Rôle :** Interface en ligne de commande / terminal d'IA servant de support pour exécuter les agents et plugins.
*   **claude-seo** (Dépôt GitHub : `AgriciDaniel/claude-seo`)
    *   **Statut :** Gratuit (Licence MIT / Open Source)
    *   **Rôle :** Plugin regroupant 26 compétences (*skills*) et 19 agents IA pour automatiser les tâches SEO (audit de vitesse, contenu, backlinks, SEO technique, référencement local Google Maps).
*   **codelynx.dev**
    *   **Statut :** Gratuit (*selon l'affichage sur la plateforme*)
    *   **Rôle :** Interface / plateforme permettant de faire tourner les agents IA en parallèle pour analyser un site et générer les livrables SEO.
*   **mlv.sh/r**
    *   **Statut :** Gratuit
    *   **Rôle :** Lien de redirection vers la bibliothèque de ressources pour obtenir le plugin `claude-seo`.

---

### 3) Astuces concrètes et réutilisables

1.  **Installation rapide :**
    Dans Claude Code, tapez la commande suivante pour ajouter l'expert SEO :
    ```bash
    /plugin install claude-seo
    ```
2.  **Commandes ciblées par besoin :**
    *   `/seo page speed` : Analyse et optimisation des temps de chargement.
    *   `/seo content` : Analyse des pages et articles.
    *   `/seo backlinks` : Vérification des liens entrants.
    *   `/seo technical` : Vérification des balises HTML, erreurs d'en-tête HTTP et codes de statut.
3.  **Audits multi-agents en parallèle :**
    Lancer l'analyse d'un domaine pour activer jusqu'à 17 agents IA en même temps (Technique, Contenu, Schema, Vitesse, Backlinks, GEO).
4.  **Suivi par plan d'action priorisé :**
    Traiter les problèmes détectés selon le niveau d'urgence indiqué par l'outil (*Critique*, *Haute*, *Moyenne*), par exemple :
    *   Corriger en priorité les pages sans balise `<title>` ou l'absence de sitemap.
    *   Traiter ensuite le contenu dupliqué ou les images trop lourdes.
5.  **Génération automatique de fichiers et de briefs :**
    L'outil génère directement dans votre dossier projet :
    *   Le fichier `sitemap.xml`.
    *   Des pages de comparaison de concurrents en HTML (`comparatif.html`).
    *   Des briefs rédactionnels d'articles au format Markdown (`brief-article.md`).
6.  **Optimisation pour la recherche IA (GEO - Generative Engine Optimization) :**
    *   Créer un fichier `llms.txt` à la racine de votre site.
    *   Ajouter des données structurées valides (`JSON-LD`, comme `FAQPage`) pour inciter ChatGPT, Claude et Gemini à citer votre site en tant que source de référence.

---

### 4) Chiffres de revenus annoncés

*   **Chiffre d'affaires / Revenus directs :** *Non précisé* (aucun chiffre de gains financiers n'est mentionné dans la vidéo).
*   **Économies réalisées (affirmé par l'auteur) :** Économie estimée à **268 $/mois** (environ 139 $/mois pour Semrush + 129 $/mois pour Ahrefs) en remplaçant ces outils par le plugin gratuit.

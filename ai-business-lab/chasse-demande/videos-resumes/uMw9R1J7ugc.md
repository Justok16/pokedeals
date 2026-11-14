# uMw9R1J7ugc — « Créer un Site Web PREMIUM à +10’000€ Avec Claude Code (GUIDE ULTIME) »

- Auteur : WEB MARKETING TUTO ; lien : https://youtu.be/uMw9R1J7ugc
- Envoyée par l'utilisateur ; résumée le 14/11/2026 par Gemini (via le relais, modèle gemini-3.5-flash)
- Les chiffres ci-dessous sont « affirmés par l'auteur », non vérifiés.

## Tri pour DIG16 (14/11)

Guide pas à pas : créer un site « haut de gamme » avec Claude Code, des guides de style DESIGN.md, des animations GSAP, puis le mettre en ligne chez Hostinger. C'est notre métier : comparaison point par point.

- **Guides de style DESIGN.md (Refero Styles)** : déjà chez nous (skill `design-md-references`, Refero noté le 27/10). Notre règle reste plus stricte : s'en inspirer, ne jamais copier l'identité d'une marque.
- **Animations GSAP** : déjà installées (skills `gsap-*`), avec notre règle des animations qui marchent aussi sur PC.
- **Page d'accueil d'abord, puis les autres pages une fois l'accueil validé** : bonne pratique, proche de notre règle « validation d'abord », mais elle n'était écrite nulle part. AJOUTÉE à `connaissances/consignes-detaillees.md` le 14/11.
- **Contexte très détaillé pour éviter les textes génériques** : c'est le rôle de notre questionnaire client ; la règle « rien d'inventé » va plus loin.
- **Correction par capture d'écran, contrôle sur téléphone et tablette, adresses sans « .html »** : déjà faits (captures de l'utilisateur, `outils/test_pages.py` à 10 largeurs, adresses propres sur Cloudflare Pages).
- **Hostinger (payant) et son connecteur** : écarté ; nos sites sont sur Cloudflare Pages, au nom de chaque client, sans coût d'hébergement.
- **« Ignorer les permissions »** : écarté (contraire à nos règles de sécurité).
- **Photos de banques d'images** : seulement en complément ; notre règle met d'abord les photos et le logo du client.
- **Prix cités (site à plus de 10 000 €, forfaits Claude)** : affirmés par l'auteur, non vérifiés ; sans effet sur nos formules.

Conclusion : rien à installer ; une bonne pratique ajoutée à nos règles. La vidéo confirme que notre méthode est celle des sites « haut de gamme ».

## Résumé (Gemini)

Voici le résumé détaillé de la vidéo, structuré selon vos demandes :

---

### 1) Idée principale
La vidéo explique comment créer et publier en ligne un site web « ultra-premium » (valeur perçue de plus de 10 000 €) de manière 100 % autonome et sans coder, en utilisant **Claude Code** (l'assistant IA d'Anthropic). La méthode repose sur le couplage de Claude Code avec des **guides de style visuels réels (`DESIGN.md`)**, la génération étape par étape (page d'accueil puis déclinaison), et le déploiement automatique sur un hébergeur web via un connecteur MCP. 

Cette méthode permet à un indépendant ou une agence de vendre des sites web haut de gamme à forte valeur ajoutée.

---

### 2) Outils, sites ou dépôts GitHub cités

*   **Claude / Claude Code (par Anthropic)**
    *   **Statut :** Payant (Nécessite au minimum le forfait *Pro* à environ 18 €/mois ; option *Max* à 90 €/mois).
    *   **À quoi il sert :** Application de bureau qui exécute Claude Code. Elle accède directement à un dossier local sur l'ordinateur pour rédiger, structurer le code (HTML, CSS, JS), corriger les erreurs graphiques et déployer le site.
*   **Refero Design Styles (`styles.refero.design`)**
    *   **Statut :** Gratuit (accès libre).
    *   **À quoi il sert :** Répertoire de plus de 2 000 guides de style (`DESIGN.md`) extraits de sites web de grandes entreprises (Apple, Stripe, OpenAI, Craft, etc.). Il fournit à l'IA les règles exactes de design (typographies, couleurs, marges, composants) à reproduire.
*   **GSAP + ScrollTrigger**
    *   **Statut :** Gratuit (librairies JavaScript intégrées automatiquement par l'IA).
    *   **À quoi il sert :** Moteur d'animations haut de gamme permettant d'ajouter des effets fluides au survol, au scroll, du parallaxe et des micro-interactions.
*   **Unsplash / Pexels**
    *   **Statut :** Gratuit.
    *   **À quoi il sert :** Banques d'images libres de droits demandées dans le prompt pour servir d'images d'illustration (*placeholders*).
*   **Hostinger & Connecteur MCP (`@hostinger/mcp`)**
    *   **Statut :** Payant pour l'hébergement (environ 3,99 €/mois / ~52 €/an avec le code promo ; inclut un nom de domaine gratuit la 1re année). Le connecteur MCP en lui-même est gratuit.
    *   **À quoi il sert :** Hébergeur web. Grâce à son connecteur MCP (`claude mcp add hostinger`), Claude Code se connecte directement au serveur Hostinger pour mettre en ligne le site, configurer le nom de domaine et le certificat SSL (HTTPS).
*   **Notion**
    *   **Statut :** Gratuit.
    *   **À quoi il sert :** Support sur lequel l'auteur partage son modèle de prompt structuré.

---

### 3) Astuces concrètes et réutilisables

1.  **Configuration optimale de Claude Code :**
    *   Désigner un dossier spécifique sur votre ordinateur (ex: `Site Premium`) pour que l'IA y enregistre tous les fichiers.
    *   Régler le modèle sur la version la plus récente (ex: *Opus 5.5*) et l'Effort sur **« Élevé »** (*High*). Ne pas utiliser *Max* afin d'éviter de consommer inutilement ses crédits.
    *   Activer l'option **« Ignorer les permissions »** dans l'application pour que Claude Code puisse travailler en continu sans vous demander de confirmation à chaque écriture de fichier.
2.  **Technique de génération séquentielle :**
    *   Demander à l'IA de générer **uniquement la page d'accueil d'abord**.
    *   Une fois la page d'accueil validée visuellement sur votre navigateur (`localhost`), demandez-lui : *« Parfait, décline les autres pages »* (À propos, Services, Contact). Cela garantit une homogénéité graphique parfaite sur tout le site.
3.  **Éviter la « bouillie IA » (textes génériques) :**
    *   Fournir un contexte d'entreprise extrêmement détaillé dans le prompt (nom, secteur, description de l'activité, ville, cible). Plus le contexte est précis, moins l'IA inventera de faux contenus.
4.  **Correction visuelle par capture d'écran :**
    *   Si un élément est mal aligné ou dépasse (ex: du texte qui sort d'une carte/post-it), faites une capture d'écran du problème, glissez-la directement dans la fenêtre de Claude Code et indiquez simplement : *« Le texte dépasse du post-it »*. L'IA analyse l'image et corrige le CSS.
5.  **Remplacement d'images à la volée :**
    *   Pour changer une image, glissez le nouveau fichier image dans Claude Code et écrivez : *« Remplace l'image de la section [Nom de la section] par l'image ci-jointe »*.
6.  **Optimisation responsive (Mobile/Tablette) :**
    *   Inspectez votre site en mode mobile dans votre navigateur Chrome. Repérez les défauts d'alignement, puis donnez ce prompt à l'IA : *« Corrige la version mobile et tablette pour rendre le site 100% responsive et parfaitement optimisé. »*
7.  **Nettoyage des URL :**
    *   Avant la publication finale, demandez à Claude Code : *« Enlève les .html dans les URL »* pour obtenir des liens propres (ex: `site.com/services` au lieu de `site.com/services.html`).
8.  **Connexion simplifiée de l'hébergeur :**
    *   Pour lier Hostinger à Claude sans clé API complexe, demandez à Claude Code : *« Connecte-toi plutôt via une fenêtre OAuth »* pour valider la connexion en un clic dans votre navigateur.

---

### 4) Chiffres de revenus annoncés

*   **Prix d'un site générique (sans méthode) :** ~200 € *(affirmé par l'auteur)*.
*   **Valeur perçue du site produit avec cette méthode :** Plus de **10 000 €** (équivalent au travail d'une agence haut de gamme) *(affirmé par l'auteur)*.
*   **Budgets de référence cités pour les sites d'inspiration :** De 10 000 € à 300 000 € *(affirmé par l'auteur)*.
*   **Revenus personnels ou chiffre d'affaires direct de l'auteur :** Non précisé.

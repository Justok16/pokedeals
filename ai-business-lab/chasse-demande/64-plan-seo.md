# 64 — Plan d'action SEO de dig16.fr (09/10/2026)

Source envoyée par l'utilisateur le 09/10 : page Notion « SEO | Les 10 outils gratuits + le prompt qui les
transforme en plan d'action » (Maxence, @capitain.ai). Idée : Claude ne remplace pas les outils, il **croise
leurs données réelles** et en tire une liste d'actions classée. Le texte exact du prompt est masqué sur la page
publique ; la méthode est appliquée ci-dessous avec des données lues le 09/10.

## 1. Ce que disent les données (lues le 09/10/2026, OpenRush, France, langue française)

| Recherche | Volume mensuel | Lecture |
|---|---|---|
| création site internet artisan / creation site internet artisan | 140 / 170 | la plus utile au niveau national |
| site internet artisan | 110 | |
| création site internet charente-maritime | 110 | département voisin, hors zone principale |
| création site internet angoulême | 20 | |
| création site internet charente | 10 | |
| création site internet (générique) | 6 600 | dominée par les grandes plateformes (Wix…), hors de portée |

**Conclusion** : en Charente, très peu de gens cherchent un créateur de sites sur Google. Le référencement
naturel de dig16.fr sera **un canal secondaire** ; les clients viendront d'abord du **démarchage direct**, de la
**fiche Google** (Maps) et du **bouche-à-oreille**. On fait donc les réglages simples, sans écrire de pages en série.

## 2. Les 10 outils de la fiche, appliqués à DIG16

| Outil | Statut chez nous |
|---|---|
| Google Keyword Planner | **Remplacé** par OpenRush (connecteur gratuit déjà branché, mêmes volumes Google), sans compte Google Ads |
| Google Trends | À consulter pour la saisonnalité (pic des recherches « artisan » en mars et septembre d'après OpenRush) |
| AnswerThePublic | Facultatif : nos questions fréquentes viennent des entretiens (`57`) |
| Ubersuggest | Remplacé par OpenRush |
| **Google Search Console** | À brancher **à l'ouverture** (`63` § 3) ; seule vraie source des mots sur lesquels le site sort |
| **Google Business Profile** | **Levier n° 1** en local ; textes prêts (`63`, Drive « Créer les comptes réseaux, pas à pas ») |
| Screaming Frog | Remplacé par nos scripts `outils/test_pages.py` et `outils/audit_site.py` (liens, balises, erreurs, débordements) : propres le 09/10 |
| **PageSpeed Insights** | Service saturé sans clé ; remplacé par **Lighthouse** (le même moteur, gratuit, lancé depuis le conteneur) |
| Rich Results Test | Données structurées Organization + WebSite en place (08/10) ; test à faire en ligne à l'ouverture |
| Yoast | Pour WordPress seulement ; nos sites sont en HTML, réglages faits à la main et contrôlés par script |

## 3. Fait le 09/10

1. **Vitesse** (Lighthouse, téléphone, page d'accueil) : **63 → 81/100**. Cause : les pages n'étaient pas
   compressées (en-tête `no-transform`, mis pour bloquer le script de statistiques de Cloudflare refusé par la
   politique de sécurité). Correction : script de statistiques **autorisé** (mesure d'audience sans cookie,
   signalée dans les mentions légales) et `no-transform` retiré ; compression Brotli vérifiée en ligne.
   Temps de blocage : 1 350 ms → 0 ms. Accessibilité et bonnes pratiques : 100/100.
   Puis (09/10, nuit) : feuille des polices Google chargée **sans bloquer** le premier affichage (doublon bloquant
   retiré) et image principale préchargée. Sur 5 mesures : **médiane 84/100**, meilleure 94 (écarts dus à la
   simulation de Lighthouse et au relais réseau du conteneur, pas au site).
2. **Titre et description de l'accueil** avec les mots réellement cherchés : « Création de site internet pour
   artisans en Charente | DIG16 » (59 caractères) et une description de 148 caractères (Google coupe au-delà
   d'environ 60 et 160).
3. Défaut évité : la politique de sécurité aurait bloqué le formulaire de contact à l'ouverture (corrigé et
   testé par `outils/test_formulaire.py`).

## 4. Liste d'actions classée (priorité décroissante)

| # | Action | Quand | Qui |
|---|---|---|---|
| 1 | Créer et faire vérifier la **fiche Google** (zone desservie, adresse masquée, photos, services) | Jour de la validation | Utilisateur, guide prêt |
| 2 | Ouvrir le site (retrait du « noindex »), envoyer le sitemap à **Search Console** et **IndexNow** | Jour de l'ouverture | Claude (`ouverture_site.py`, `indexnow.py`) + utilisateur pour Search Console |
| 3 | Demander un **avis Google** à chaque client satisfait (jamais d'avis inventé ni acheté) | Dès le 1er client | Utilisateur |
| 4 | Inscriptions gratuites : Bing Places, Apple Business Connect, annuaire de la CCI | Semaine 1 | Utilisateur |
| 5 | Chaque site client porte « Site réalisé par DIG16 » en pied de page, avec lien (avec l'accord du client) | Chaque livraison | Claude |
| 6 | Mesurer chaque mois : Search Console (clics, positions), statistiques Cloudflare, fiche Google (appels) | Mensuel | Claude |
| 7 | Vitesse : médiane 84/100 atteinte le 09/10 ; re-mesurer avec PageSpeed Insights à l'ouverture (réseau réel, sans le relais du conteneur) | À l'ouverture | Claude |
| 8 | Pages par ville ou par métier : **non** tant que les volumes restent à 10-20 recherches par mois (contenu mince pénalisé) | À revoir dans 3 mois avec Search Console | Claude |

## 5. Le contrôle mensuel (consigne pour le point automatique, après l'ouverture)

> Croise les données réelles de Search Console (requêtes, clics, positions), des statistiques Cloudflare, de la
> fiche Google (appels, itinéraires) et de Lighthouse (vitesse téléphone de l'accueil et du test du pouce).
> N'invente rien : chaque recommandation cite son chiffre. Sors 5 actions au plus, classées par effet attendu sur
> les demandes de démo, avec pour chacune : quoi faire, qui le fait, en combien de temps.

Mesure de vitesse : `npm i lighthouse@12` dans un dossier temporaire, puis
`CHROME_PATH=/opt/pw-browsers/chromium-1194/chrome-linux/chrome npx lighthouse https://dig16.fr/ --only-categories=performance --chrome-flags="--headless=new --no-sandbox"`.

# 67 — Audit référencement complet du 18/10/2026 (site, réseaux, sites clients)

Demande de l'utilisateur (17/10 au soir) : « es-tu à ton maximum ? » puis « fais tout ça maintenant au maximum
de tes capacités ». Tout ce qui suit a été mesuré ou vérifié le 18/10/2026, outils cités à chaque ligne.

## 1. Ce qui a été mesuré

| Contrôle | Résultat | Outil |
|---|---|---|
| Note technique du site (5 pages) | **99,4 / 100**, 0 défaut grave ou moyen, 1 défaut léger : 6 images sans texte alternatif sur l'accueil | OpenRush `audit_site` |
| Titres (≤ 60 car.), descriptions (≤ 160), un seul H1, canonique, langue, Open Graph, données structurées valides | Tout conforme, sauf `le-projet` : titre 66 car., description 182 car. | script maison (lecture du HTML) |
| Redirections | `http` → `https` 301 ✅ ; `/prestige.html` → `/prestige` 308 ✅ ; **`www.dig16.fr` répondait en 200 sans redirection** (deux copies du site pour Google) ❌ | `curl` |
| Compression, en-têtes de sécurité, 404 | Brotli actif, en-têtes complets, page 404 en `noindex` ✅ | `curl` |
| robots.txt et robots des IA | Tout autorisé sauf `/m/` (maquettes privées) ; aucun robot d'IA bloqué (GPTBot, ClaudeBot, PerplexityBot, Google-Extended peuvent citer le site) ✅ | lecture du fichier |
| `llms.txt`, sitemap | Présents et à jour ✅ | lecture |
| Fiche Google | Validée, catégorie « Concepteur de sites Web », 8 photos, **0 avis**, **site indiqué `https://www.dig16.fr/`** (avec www) | OpenSEO `get_business_profile` |
| Recherches réelles en France (volumes mensuels) | « création site internet artisan » 140, « site internet artisan » 110, « creation site internet artisan » 110, « site internet pour artisan » 50 ; le reste < 30 | OpenRush `research_keywords` |
| Réseaux : YouTube | Présentation complète (sites internet, artisans, Charente, 49 €, 0 € de création, démo gratuite) ✅ | page publique lue |
| Réseaux : TikTok | Bio « Sites internet pour artisans et commerçants de Charente. Dès 49 €/mois. » ✅ ; **aucun lien** dans la bio (champ vide) | page publique lue |
| Réseaux : Instagram, Facebook, Threads, X | **Non lisibles depuis le conteneur** (Instagram 429, Facebook 400, Threads et X sans contenu sans connexion) → contrôle sur capture de l'utilisateur | `curl` |

## 2. Ce qui a été fait le 18/10 (mis en ligne, testé)

1. **Une seule adresse** : `site-dig/functions/_middleware.js` redirige `www.dig16.fr` vers `dig16.fr` (301). Le fichier
   `_redirects` de Cloudflare Pages ne sait pas rediriger un domaine entier (documentation Cloudflare lue le 18/10).
2. **6 textes alternatifs** ajoutés aux images de l'accueil (recherche d'images Google + accessibilité).
3. **`le-projet`** : titre ramené à 58 caractères, description à 156.
4. **Nouvelle page** `https://dig16.fr/site-internet-artisan/` : « Site internet pour artisan : le guide avant de
   choisir » (≈ 1 300 mots). Construite pour les recherches réelles (« site internet artisan », « création site
   internet artisan », « site internet pour artisan ») et pour les moteurs à IA : réponse en 40–60 mots en tête de
   chaque section, tableau comparatif, liste de vérification, 6 questions en données structurées `FAQPage`,
   `Article` daté, fil d'Ariane, sources citées en bas (documentation Google sur l'indexation mobile, règles Google
   sur les avis, lues le 18/10). Rien d'invérifié : les seuls chiffres sont ceux de DIG16.
   Contrôles : `test_pages.py` (ordinateur + téléphone) ✅, `audit_acces.py` 0 problème, `lisibilite.py` 0,
   `anti_generique.py` OK, orthographe (seules remarques : citation en anglais, balisée `lang="en"`), rendu relu sur
   capture à 320, 390 et 1 440 px (tableau en cartes sur téléphone), aucune erreur console.
5. **Maillage** : lien vers le guide dans le pied de page de l'accueil, de Prestige, du test du pouce, du projet ;
   lien dans le texte de « Le projet » ; sitemap et `llms.txt` mis à jour ; IndexNow envoyé après la mise en ligne.
6. **Kit « avis Google »** (`outils/kit_avis.py`) : carte A6 à 300 ppp avec QR code vers la page « Laisser un
   avis » de la fiche (lien direct `search.google.com/local/writereview?placeid=…`, testé 200), QR décodé sur
   l'image finale (OpenCV), polices du site incorporées ; messages SMS et email prêts ; réponses types aux avis.
   Fait pour DIG16 (`supports/avis/`) ; le même outil servira à chaque client de l'offre Visibilité
   (`65-seo-sites-clients.md`). Règles Google sur les avis rappelées dans l'outil : jamais payés, jamais
   inventés, jamais de tri des clients contents.

## 3. Ce qui reste, et pourquoi

| Levier | État | Pourquoi ce n'est pas fait par Claude |
|---|---|---|
| **Avis Google** (1er critère local) | 0 avis | Ils viennent des clients réels. Kit prêt ; à remettre à chaque client satisfait |
| **Liens entrants** | Quasi aucun | Ils viennent des organismes (25 contactés le 13/10, relance le 27/10), d'Atout Ruffec, de la presse (Charente Libre le 27/10), des sites clients (« Site réalisé par DIG16 ») |
| **Bios Instagram, Facebook, Threads, X** | Non vérifiables d'ici | Captures de l'utilisateur ; textes proposés au § 4 |
| **Lien dans la bio TikTok** | Vide | À ajouter par l'utilisateur si TikTok le permet sur ce compte (à vérifier sur l'écran, pas de parcours de mémoire) |
| **Site de la fiche Google** | `https://www.dig16.fr/` | La redirection règle le problème ; par propreté, l'utilisateur peut mettre `https://dig16.fr/` (facultatif) |
| **Statistiques réelles** (Search Console, Bing) | Site trop récent (ouvert le 09/10) | Premier point statistiques lundi 19/10 à 8 h 47, puis chaque lundi ; revue mensuelle le 1er |
| **Pages « par ville »** | Volontairement non faites | 10 à 20 recherches par mois par ville : pages minces pénalisées ; à revoir dans 3 mois avec les données réelles |

## 4. Présentations des réseaux : textes proposés (à coller si la capture montre autre chose)

Tous citent le métier, la cible, le département et le site ; aucune donnée personnelle, aucun parcours.

| Réseau | Texte court (bio) | Lien |
|---|---|---|
| Instagram `dig16fr` | Sites internet pour artisans et commerçants de Charente. 0 € de création, dès 49 €/mois, à votre nom. Votre page d'accueil refaite gratuitement 👇 | https://dig16.fr/ |
| Threads `dig16fr` | Sites internet pour artisans et commerçants de Charente. Dès 49 €/mois, à votre nom. Démo gratuite sur dig16.fr | https://dig16.fr/ |
| Facebook (présentation courte) | DIG16 crée des sites internet pour les artisans, commerçants et indépendants de Charente : modernes, rapides, pensés pour le téléphone, à votre nom. 0 € de création, dès 49 €/mois. Votre page d'accueil refaite gratuitement avant de décider. | https://dig16.fr/ |
| X `@dig16charente` | Sites internet pour artisans et commerçants de Charente. 0 € de création, dès 49 €/mois, à votre nom. Démo gratuite. | https://dig16.fr/ |
| TikTok `dig16fr` | Sites internet pour artisans et commerçants de Charente. Dès 49 €/mois. (déjà en place) | à ajouter si possible |
| YouTube `@dig16fr` | Présentation déjà complète (vérifiée le 18/10) | déjà en place |

Catégorie à vérifier sur chaque profil professionnel : « Concepteur de sites Web » / « Conception de sites web »,
la même que sur la fiche Google.

## 5. Pour les sites des clients (ajouté à `65-seo-sites-clients.md`)

- À la livraison : `python3 outils/kit_avis.py "<Nom>" <place_id> <dossier privé>` → carte à imprimer (A6) et
  messages ; le `place_id` se lit avec OpenSEO `get_business_profile` (nom ou cid de la fiche du client).
- Une seule adresse par site (www → sans www ou l'inverse, jamais les deux en 200) : même middleware.
- Texte alternatif sur chaque image, titre ≤ 60, description ≤ 160, une page par service, FAQ en données
  structurées quand il y a de vraies questions de clients.

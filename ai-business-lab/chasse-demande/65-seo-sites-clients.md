# 65 — Référencement des sites clients : la méthode DIG16 (12/10/2026)

Demande de l'utilisateur (12/10) : « je veux que le référencement des sites des clients soit au meilleur ».
Principe : un artisan est trouvé surtout **en local** (fiche Google, Maps, « plombier + ville »). Le site, la fiche
Google et les annuaires doivent dire **exactement la même chose** (nom, adresse ou zone, téléphone, horaires).
Rien d'inventé : jamais de faux avis, de fausses réalisations ni de pages en série sans contenu réel.

## 1. À la livraison (Claude, avant la mise en ligne)

| # | Point | Comment |
|---|---|---|
| 1 | Une page par service réellement proposé (pas de pages « ville » en série : contenu mince = pénalité) | maquette du site |
| 2 | Titre de chaque page : « Service + ville principale \| Nom » (30-60 caractères), description 70-160 caractères, un seul H1 | relu à la main |
| 3 | Données structurées « entreprise locale » au type exact du métier (Plumber, Electrician, RoofingContractor…) | `python3 outils/seo_client.py --schema fiche.json` (fiche privée, hors dépôt) |
| 4 | Adresse masquée si l'artisan se déplace chez ses clients (zone desservie à la place), comme sur sa fiche Google | champ `masquer_adresse` |
| 5 | Plan du site, robots.txt, liens internes sans redirection, canonique sur chaque page, images WebP avec texte alternatif, langue fr | gabarit DIG16 |
| 6 | Vitesse téléphone : Lighthouse ≥ 90 (méthode dans `64-plan-seo.md`) | mesuré |
| 7 | Email non masqué par Cloudflare (sinon lien `/cdn-cgi/` en 404 pour Google) : `<!--email_off-->` autour du contenu | gabarit DIG16 |
| 8 | **Contrôle final : `python3 outils/seo_client.py https://site-du-client.fr/` → 0 ALERTE**, puis `test_pages.py` adapté | obligatoire (`44`) |
| 9 | Signalement immédiat aux moteurs : IndexNow (Bing, Yandex…) | `outils/indexnow.py` adapté au domaine |

## 2. Les comptes du client (toujours à son nom ; DIG16 ajouté comme gestionnaire)

| Outil | Rôle | Qui |
|---|---|---|
| **Fiche Google** (levier n° 1 en local) | catégorie exacte, zone, horaires, photos réelles, lien vers le site, 1 publication par mois | client crée / valide, Claude prépare les textes |
| **Search Console** | propriété du site au nom du client, DIG16 utilisateur ; sitemap envoyé ; indexation demandée | Claude guide, client valide |
| Bing Webmaster | import depuis Search Console | client (2 min) |
| Bing Places, Apple Business, PagesJaunes (gratuit) | mêmes informations que la fiche Google | client, parcours dans `connaissances/parcours-verifies.md` |
| Annuaires sérieux du métier | Chambre de métiers, fédération (CAPEB, FFB…), mairie / communauté de communes, labels réels (RGE, Qualibat) | à vérifier un par un : gratuit, pas d'abonnement caché |

## 3. Avis et liens (ce qui fait vraiment monter)

- **Avis Google** : un lien court « laisser un avis » envoyé au client du client après chaque chantier ; répondre à
  chaque avis. Jamais d'avis acheté, échangé ou rédigé à la place du client (interdit et sanctionné par Google).
- **Liens** : page « réalisations » de dig16.fr vers le site du client (avec son accord) ; liens des fournisseurs,
  partenaires et associations locales quand ils existent vraiment.

## 4. Chaque mois (offre Visibilité)

1. `seo_client.py` sur le site : 0 ALERTE.
2. Search Console du client (projet OpenSEO à son nom, lecture gratuite) : recherches, clics, position ; 3 actions au plus.
3. Fiche Google : 1 publication, réponses aux avis, photos nouvelles.
4. Rapport court au client (ce qui a été fait, ce qui a changé, prochain pas), chiffres réels seulement.

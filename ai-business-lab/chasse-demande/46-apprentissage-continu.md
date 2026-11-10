# 46 — Apprentissage continu (règle permanente, demande de l'utilisateur du 28/09/2026)

> « Pour toutes les vidéos YouTube que j'ajoute […] je compte sur toi pour que tu te serves de
> ces outils pour t'améliorer et que tu gardes ça en mémoire. […] Je veux que ce soit
> systématique, cet apprentissage constant. »

## La marche à suivre, à chaque vidéo envoyée (sans attendre qu'on le demande)

1. **Résumer** la vidéo avec le relais (`/api/video`, clé Gemini gratuite, plusieurs modèles ;
   secours vidIQ `vidiq_video_transcript` si Gemini échoue) et enregistrer le résumé dans
   `videos-resumes/<identifiant>.md`.
2. **Trier chaque idée** : *appliquée*, *à faire* (gratuit, sûr, utile), *décision de
   l'utilisateur* (argent, prix, identité), *écartée* (payante, illégale, hors sujet), avec la
   raison. Les chiffres de revenus restent « affirmés par l'auteur ».
3. **Appliquer tout de suite** ce qui est gratuit, légal et sûr : outil ou skill (après lecture
   complète de son contenu), règle de contrôle qualité, amélioration des démos ou du site.
   **Skills (règle du 15/10, vidéo -9jiz-OmBos)** : n'installer un skill que s'il sert à une tâche réelle en cours ;
   un skill maison ne s'écrit qu'après avoir réussi la tâche une fois, à partir des étapes réelles et des problèmes rencontrés.
4. **Connecteurs** : si une vidéo cite un connecteur ou un MCP utile, le chercher dans le
   catalogue et proposer à l'utilisateur de le brancher (lui seul peut se connecter).
5. **Mettre à jour le registre** (`46-registre-videos.md`, ajout **à la fin**), relancer
   `python3 outils/catalogue_outils.py`, et répondre à l'utilisateur en français simple : ce qu'on applique, ce qui
   attend sa décision.
6. Le point automatique du matin (07:34 UTC) reprend la liste « À faire » ci-dessous tant qu'elle n'est pas vide.

## Où est rangé quoi (découpage du 10/11/2026, rien n'a été supprimé)

- Marche à suivre, actions encore ouvertes, veille : cette fiche, `46-apprentissage-continu.md`.
- Registre de tous les envois (vivant, ajouts à la fin) : `46-registre-videos.md`.
- Actions terminées et décisions tranchées : `archives/46-a-faire-termines.md`.
- Catalogue classé par besoin (automatique) : `connaissances/boite-a-outils-catalogue.md`.

## À faire (gratuit et sûr) — repris à chaque point automatique

Seules les lignes **encore ouvertes** restent ici (numéros d'origine) ; les 14 terminées sont dans `archives/46-a-faire-termines.md`.

| # | Action | Source | État |
|---|---|---|---|
| 4 | Chercher avec vidIQ les questions les plus demandées sur les sites d'artisans (vidéos « outliers ») : preuve de demande, idées de contenus | MROM3p3CPZU | **fait le 01/10 (soir)**, résultat négatif et cohérent avec OpenRush : sur YouTube France, « site internet artisan » et toutes ses variantes (création, plombier, électricien, prix, devis…) font **moins de 750 recherches par mois** chacune (vidIQ, données du 18/07/2026) ; seul « agence web » atteint 4 345. Les vidéos « qui percent » sur ce sujet (6 derniers mois, titres en français) sont du bruit, sauf 3 tutoriels de création de site avec Claude Code (A9E7gUrO5YQ, GgDhVLK6VbM, gwKurw7tk7g) **à résumer au prochain lot** pour comparer leurs méthodes aux nôtres. Conclusion : les artisans ne cherchent pas ce sujet sur YouTube ; pas de contenu vidéo à produire pour attirer des clients, la prospection directe reste la voie. Le mode « questions » de vidIQ n'existe pas en français. Coût : 10 crédits sur 150/mois |
| 6 | Page d'arrivée alignée mot pour mot sur le message de prospection | oBw_BDIZIqc | à appliquer aux prochains messages |
| 10 | Référencement des clients : OpenSEO (gratuit ?), GEO Optimizer, fichier `llms.txt`, fiche Google ; vérifier l'offre gratuite à la source, puis chiffrer avec l'utilisateur | reel Ddr5n7-OOcm, tarifs Durable | **fait le 29/09** : OpenSEO écarté (logiciel gratuit mais données DataForSEO payantes à l'usage ; OpenRush gratuit suffit). GEO Optimizer (MIT, 58 000 lignes : pas installé) : sa grille « préparation aux IA » est devenue `outils/prospects/pack_visibilite.py` (données structurées « entreprise locale », partage, `robots.txt` ouvert aux assistants IA, `sitemap.xml`, `llms.txt`, uniquement à partir de la fiche client vérifiée), à lancer sur chaque site client publié. À proposer dans l'offre (chiffrage avec l'utilisateur) |
| 16 | Site **deviensdev.fr** (guides Claude Code, hébergement gratuit, freelance) envoyé le 02/10 : lu en entier. Appliqué : hébergement des clients confirmé sur Cloudflare (fichiers statiques « free and unlimited », doc officielle) et jamais sur Vercel gratuit (non commercial) ; Acre micro 25 % depuis le 01/07/2026 et règle ARE / création (cumul, ARCE, « activité conservée ») ajoutées dans `36-aides-creation.md`, relues sur Service Public et France Travail ; site ajouté à la veille quotidienne (`veille_sources.py`, guides nouveaux ou mis à jour). **Reste à faire avant le premier client payant** : déplacer le relais (aujourd'hui sur Vercel gratuit) vers Cloudflare Workers (100 000 requêtes/jour gratuites, à vérifier à la source), car un usage pour une activité payée devient commercial. | deviensdev.fr | **fait le 02/10**, sauf le relais (à faire) |
| 17 | Site **buildyoursaas.tech** envoyé le 02/10 (accompagnement payant pour apprendre Claude Code aux dirigeants de plus de 500 000 € de chiffre d'affaires ; aucun prix affiché ; chiffres et clients cités non vérifiés). Retenu pour Dig, sur la forme de vente : (a) écrire les problèmes **avec les mots exacts des clients** entendus au téléphone (« on nous a vendu du vent », agence dont on ne peut rien reprendre) → noter ces phrases mot pour mot à chaque appel, pour les réutiliser sur le site, sans nom et avec accord ; (b) une rubrique honnête « C'est pour vous si / ce n'est pas pour vous si » sur le site de Dig, à écrire **après** les premiers appels réels (rien d'inventé) ; (c) déjà en place sur notre site : site et domaine au nom du client, départ possible avec son site, démo offerte avant tout engagement. Piste « former des dirigeants à Claude Code » : non retenue (aucune preuve de demande de notre côté, cible très éloignée de la nôtre ; grille `00-grille-anti-digcost.md`). | buildyoursaas.tech | **lu le 02/10** ; (a) et (b) à faire au premier appel |

## Décisions qui appartiennent à l'utilisateur

Aucune en attente dans cette fiche au 10/11/2026 : les décisions ouvertes sont suivies dans la LISTE UNIQUE (`64-mise-en-ordre-administrative.md` § 0).
Les anciennes décisions (parrainage, UI UX Pro Max, Firecrawl et Similarweb : toutes tranchées) sont dans `archives/46-a-faire-termines.md` ;
les anciens tris du 28/09 au 01/10 sont à la fin de `46-registre-videos.md`.

## Veille quotidienne sur les sources de l'utilisateur (depuis le 28/09/2026)

`outils/veille_sources.py` (lancé une fois par jour par le point automatique) :
- **Chaînes YouTube** (`connaissances/*/liste-videos.json`) : Finary, Fintales, Melvynx,
  Matt Wolfe. Nouvelles vidéos en tête de liste ; pour Melvynx et Matt Wolfe, seules celles
  dont le titre touche au projet (filtre dans `liste-videos.json`) vont dans `prio.json`.
- **Annuaires d'outils** : nosignups.net (268), futuretools.io (environ 4 300), free-for.dev
  (1 367 offres gratuites), mrfreetools.com (1 913). Mémoire cumulée dans `veille/etat/`.
- **moneyradar.org** (envoyé le 05/10) : comparatifs banque, bourse, épargne, comptes pros et logiciels de
  compta ; plan du site lu chaque jour (543 pages, clé = adresse + date de mise à jour). Site d'affiliation
  (liens de parrainage) : ne sert qu'à repérer des pistes ; tout chiffre ou règle est revérifié à la source
  officielle. Premier apport : la règle du compte bancaire dédié (10 000 € deux années de suite), confirmée
  sur Service Public (F35991) et ajoutée au kit 31.
- **Rapport** : `veille/<date>.md`. Chaque nouveauté utile est évaluée (offre gratuite vérifiée à
  la source, légalité, utilité pour Dig ou pour la chasse aux pistes), puis appliquée ou écartée
  ici, avec la raison.
- **Facebook** : une page Facebook ne se liste pas sans connexion ; **réflexe** : chercher la chaîne
  YouTube du même créateur. Reels « gabzermp4 » = YouTube **@gabzer.mp4** (547 vidéos courtes,
  246 retenues sur leur titre), ajoutée à la veille (`connaissances/gabzer/`).

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
4. **Connecteurs** : si une vidéo cite un connecteur ou un MCP utile, le chercher dans le
   catalogue et proposer à l'utilisateur de le brancher (lui seul peut se connecter).
5. **Mettre à jour ce registre** (tableau ci-dessous) et répondre à l'utilisateur en français
   simple : ce qu'on applique, ce qui attend sa décision.
6. Le point automatique toutes les 3 h reprend la liste « À faire » tant qu'elle n'est pas vide.

## À faire (gratuit et sûr) — repris à chaque point automatique

| # | Action | Source | État |
|---|---|---|---|
| 1 | Lire puis installer, s'ils sont sûrs, les skills **Impeccable** (contrôle visuel des marges, alignements, couleurs) et **vibe-security** (failles de sécurité) | LCwT00LrPZg, _SVU3oC4JX8 | **fait autrement** : Impeccable télécharge et lance un programme tiers, donc non installé ; ses règles d'audit sont reprises dans `outils/audit_acces.py` (site et 12 démos corrigés, 0 défaut). **vibe-security installé le 28/09** (lu en entier : texte seul, licence MIT) et passé sur tout le projet : aucune faille grave ; en-têtes de sécurité ajoutés au site, règle `.env` ajoutée |
| 2 | Tester le skill `motion-graphics` pour une vidéo de lancement de Dig (après relecture du dépôt) | 6Ij9-f2T2Ck | à faire |
| 3 | Contrôle qualité : toute animation vérifiée à 0, 25, 50, 75 et 100 % de sa durée | HOXrLsVqinY | **fait** (ligne déjà présente dans `44-controle-qualite.md`) |
| 4 | Chercher avec vidIQ les questions les plus demandées sur les sites d'artisans (vidéos « outliers ») : preuve de demande, idées de contenus | MROM3p3CPZU | à faire |
| 5 | Ressources gratuites de design (polices Fontshare, icônes, composants) pour les démos | _SVU3oC4JX8 | à évaluer |
| 6 | Page d'arrivée alignée mot pour mot sur le message de prospection | oBw_BDIZIqc | à appliquer aux prochains messages |
| 7 | Passer chaque document important dans `/api/avis` (second avis) avant de l'envoyer | _9ZGlLWr6UE | **appliqué le 28/09** sur les textes des 7 démos du lot 2 (gemini-3.5-flash-lite) : 4 corrections retenues (phrase répétée non vérifiée, « petits prix », « à la minute ») ; suggestions juridiques non fondées écartées après vérification |
| 8 | Vérifier les photos fournies par les clients avec `outils/verif_metadonnees.py` (position GPS) | nosignups.net | **fait** (outil prêt ; 22 images du site : propres) |

## Décisions qui appartiennent à l'utilisateur

| Sujet | Source | Question |
|---|---|---|
| **Parrainage client** | vKat0aTuEbo | **Validé (variante A) et appliqué le 28/09** : site, guide, `47-parrainage.md` |
| Connecteurs **Firecrawl** et **Similarweb** | HOXrLsVqinY, inventaire du 28/09 | À brancher sur claude.ai (voir `33-outils.md`) |

### Chaînes YouTube envoyées le 28/09 (soir)

- **@melvynxdev** (Melvynx, 1 027 vidéos, français : Claude Code, Codex, skills, création et
  vente de SaaS, série « Lumail to 10k MRR » sur le marketing et la prospection à froid).
- **@mreflow** (Matt Wolfe, 800 vidéos, créateur de futuretools.io : outils d'IA gratuits,
  actualités).

Tout résumer prendrait des semaines de quota gratuit (partagé avec Finary). Première sélection :
**15 vidéos par chaîne**, choisies sur le titre pour ce qui sert Dig (vente, prospection à froid,
emails, skills, belles interfaces, sites, outils gratuits). Fiches : `connaissances/melvynx/`
et `connaissances/mreflow/`. Élargissement proposé à l'utilisateur une fois ces 30 vidéos
triées et appliquées.

## Veille quotidienne sur les sources de l'utilisateur (depuis le 28/09/2026)

`outils/veille_sources.py` (lancé une fois par jour par le point automatique) :
- **Chaînes YouTube** (`connaissances/*/liste-videos.json`) : Finary, Fintales, Melvynx,
  Matt Wolfe. Nouvelles vidéos en tête de liste ; pour Melvynx et Matt Wolfe, seules celles
  dont le titre touche au projet (filtre dans `liste-videos.json`) vont dans `prio.json`.
- **Annuaires d'outils** : nosignups.net (268), futuretools.io (environ 4 300), free-for.dev
  (1 367 offres gratuites), mrfreetools.com (1 913). Mémoire cumulée dans `veille/etat/`.
- **Rapport** : `veille/<date>.md`. Chaque nouveauté utile est évaluée (offre gratuite vérifiée à
  la source, légalité, utilité pour Dig ou pour la chasse aux pistes), puis appliquée ou écartée
  ici, avec la raison.
- **Facebook** : une page Facebook ne se liste pas sans connexion ; **réflexe** : chercher la chaîne
  YouTube du même créateur. Reels « gabzermp4 » = YouTube **@gabzer.mp4** (547 vidéos courtes,
  246 retenues sur leur titre), ajoutée à la veille (`connaissances/gabzer/`).

## Registre de toutes les vidéos envoyées

Synthèses détaillées : `37-videos-synthese.md` (13 vidéos du 25/09), `43-videos-26-09.md`
(vidéos du 26/09), résumés complets : `videos-resumes/`.

### Vidéos du 28/09

| Vidéo | Sujet | Verdict |
|---|---|---|
| MROM3p3CPZU | Question populaire → réponse avec Claude → YouTube | Méthode = notre règle n° 1 (demande prouvée) ; action n° 4 |
| kYNwdRnb4ks | Claude en 4 niveaux (connecteurs, projets, skills, tâches planifiées) | Déjà appliqué presque entièrement |
| LCwT00LrPZg | 15 skills gratuits pour Claude | Action n° 1 ; « caveman » écarté (réponses trop sèches pour l'utilisateur) |
| hImo2S4HOGI | Motion design avec Claude Design | Plus tard (vidéo de présentation Dig), consomme des crédits |
| 7RVf25Rg0Mc | Paperclip : plusieurs agents IA organisés en entreprise | Écarté : demande un serveur allumé en permanence ; nos routines font l'essentiel |
| skOBL2Yc35I | TikTok à 10 000 €/mois | **Écarté** : son « repost amélioré » est de la contrefaçon |
| e7t6YTrqznM | Appli mobile en 30 jours avec Claude Code | Hors piste actuelle (on reste sur les sites) |
| is3XYKl2bpI | 8 conseils officiels pour Opus 5.5 | Appliqué : vérifier tout le contexte avant d'agir, effort adapté |
| TWhoNLkUXKY | Site d'affiliation Amazon fait avec l'IA | Piste à passer à la grille ; marché encombré |
| YuOSyRj3sXg | « Cerveau numérique » personnel | Déjà en place (`.claude/CLAUDE.md` + dossier) |
| PLGnXz9_dTY | Connecteur TradingView | Écarté (trading, hors projet) |
| _SVU3oC4JX8 | Vendre des sites faits avec Claude Design | Actions n° 1 et 5 |
| vKat0aTuEbo | Agence vidéo : parrainage 10 % / 30 %, marché américain | Décision parrainage |
| ucer2chlfM8 | Claude + Codex en tandem | Écarté (abonnement OpenAI payant) |
| _9ZGlLWr6UE | Claude Code + Codex (délégation, relecture croisée en lecture seule) | Codex payant : écarté ; **appliqué** en gratuit : `/api/avis` (second avis Gemini) |
| 05ody6JKf1Y | Podcast : IA générale, emploi, « zone de génie » | Réflexion générale ; vente en direct sans intermédiaire = déjà le modèle de Dig |
| 5 reels Facebook | Sites gratuits, Manychat, annuaire, Klap, LightPDF | Détail : `videos-resumes/reels-facebook-28-09.md` ; Klap **écarté** (contrefaçon) |
| rWbVgBdl-0I (Melvynx) | Marketing d'un SaaS en public (Lumail, annuaire mcpservers.org, affiliation) | Hors piste Dig pour l'instant ; idée gardée : se faire lister dans les annuaires gratuits de son secteur |
| 5QMtCBkjvkY, JmNfV3GhVUU (gabzer) | Pubs vidéo et boutique générées par IA (Atoms, Higgsfield, bibliothèque de pubs Meta) | Bibliothèque de pubs Meta (gratuite) utile pour voir ce que font les concurrents d'un prospect ; copier la pub d'un autre : **écarté** (contrefaçon) ; outils payants non retenus |

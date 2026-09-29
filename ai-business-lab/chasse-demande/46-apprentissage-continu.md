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
| 9 | Skills de design gratuits pour des démos moins « génériques » : Taste Skill, Impeccable, Awesome DESIGN.md (et Humanizer pour les textes) ; lire tout le code avant installation | reels DcRIZ_5DSCd, vidéo 3fdb_giOrLo | **fait le 29/09** : Taste Skill (MIT) et Impeccable (Apache 2.0) récupérés et examinés. Taste Skill vise React et les installations de paquets et utilise des images de remplissage : pas installé tel quel ; ses règles « anti-IA » sont devenues `outils/anti_generique.py` (46 démos contrôlées : aucun défaut bloquant ; la rangée de 3 étapes égales du générateur est passée en escalier pour les prochaines démos). Impeccable contient un programme de 13 500 lignes : pas installé ; ses grilles de critique en texte restent à lire (`reference/critique.md`, `audit.md`). Humanizer : à examiner |
| 10 | Référencement des clients : OpenSEO (gratuit ?), GEO Optimizer, fichier `llms.txt`, fiche Google ; vérifier l'offre gratuite à la source, puis chiffrer avec l'utilisateur | reel Ddr5n7-OOcm, tarifs Durable | **fait le 29/09** : OpenSEO écarté (logiciel gratuit mais données DataForSEO payantes à l'usage ; OpenRush gratuit suffit). GEO Optimizer (MIT, 58 000 lignes : pas installé) : sa grille « préparation aux IA » est devenue `outils/prospects/pack_visibilite.py` (données structurées « entreprise locale », partage, `robots.txt` ouvert aux assistants IA, `sitemap.xml`, `llms.txt`, uniquement à partir de la fiche client vérifiée), à lancer sur chaque site client publié. À proposer dans l'offre (chiffrage avec l'utilisateur) |
| 11 | Petit outil gratuit sans inscription sur le site de Dig (« votre entreprise est-elle trouvable sur Google et dans les IA ? »), pour attirer des artisans et prouver le savoir-faire (« engineering as marketing ») ; à passer à la grille avant de construire | Melvynx HLCurWw88bM | à évaluer |

## Décisions qui appartiennent à l'utilisateur

| Sujet | Source | Question |
|---|---|---|
| **Parrainage client** | vKat0aTuEbo | **Validé (variante A) et appliqué le 28/09** : site, guide, `47-parrainage.md` |
| Connecteurs **Firecrawl** et **Similarweb** | HOXrLsVqinY, inventaire du 28/09 | À brancher sur claude.ai (voir `33-outils.md`) |

### Tri Melvynx du 29/09 (26 fiches lues sur 1 027)

| Idée ou outil | Verdict |
|---|---|
| Kit de skills de design `jakubkrehel/skills` (MIT, texte seul, relu le 29/09) | Non installé (des consignes de relecture, pas un outil). Ses règles mesurables ont été contrôlées sur les démos : champs de formulaire ≥ 16 px sur téléphone (17 px), lignes de 60 à 75 caractères (64-65), interlignes (1,7 pour le texte, 1,1 pour les titres) : conformes. Seul manque corrigé : retour à la ligne équilibré des titres et sans mot isolé en fin de paragraphe (`text-wrap`), ajouté au générateur pour les prochaines démos |
| Envoi d'e-mails : sous-domaine dédié pour protéger le domaine principal, test de délivrabilité gratuit (SPF, DKIM, DMARC) avant tout envoi | À appliquer le jour où Dig aura son domaine et enverra des e-mails de prospection |
| Consignes courtes pour les skills (le modèle sait déjà faire) | Déjà le cas pour nos skills |
| Tarif « forfait + usage » ; ne pas miser sur le SEO au démarrage d'un logiciel | Pas pour Dig aujourd'hui (offre de sites à prix fixe) |
| Tests de modèles d'IA (Gemini, GPT, Grok…) | Information générale, rien à appliquer |

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

### Envois du 29/09 (nuit)

| Vidéo ou source | Sujet | Verdict |
|---|---|---|
| Capture « Les outils IA qui te rendent inarrêtable » (reel Instagram) | 36 outils d'IA | Détail : `videos-resumes/outils-ia-instagram-29-09.md`. **Durable** est un concurrent direct (site gratuit, puis 25 $/mois) : on garde ses bonnes idées gratuites (fiche Google, annuaires locaux, demandes d'avis, `llms.txt`). **DoNotPay** écarté (sanction de la FTC en 2025). Les autres outils sont payants ou sans usage pour Dig. |
| @melvynxdev : **toute la chaîne** (demande du 29/09) | 1 027 vidéos | Lecture complète lancée ; elle passe **avant** la suite de Finary (demande la plus récente). Environ 150 vidéos par jour avec le quota gratuit : 7 à 10 jours. Fiches : `connaissances/melvynx/` |
| 12 vidéos YouTube | Voir `videos-resumes/` | 2 déjà traitées (kYNwdRnb4ks, Uh9A_E4ik-0), 10 en cours de résumé |
| 6 reels Instagram (enfin lus le 29/09 : yt-dlp + ffmpeg + Gemini) | Fiches `videos-resumes/reel-*.md` | **Design des démos** : Taste Skill, Impeccable, Awesome DESIGN.md (gratuits et libres selon les vidéos) : à évaluer, avec lecture complète du code avant toute installation (action n° 9). **SEO pour les clients** : OpenSEO (présenté comme une alternative gratuite à Semrush), GEO Optimizer (être recommandé par les assistants IA), GSC MCP (Search Console) : à évaluer pour l'offre (action n° 10). **Écartés** : OmniRoute (fait tourner les quotas gratuits de 200 fournisseurs : conditions d'utilisation à risque), Headroom et Task Observer (inutiles ici), Perplexity (payant). Claude Mem : notre mémoire (`.claude/CLAUDE.md`) suffit. Le 7e reel (DVolgosjH7u) est freiné par Instagram (429) : nouvel essai plus tard |
| Pages Facebook **IA Boss** (@iabossai) et **Unefille.ia** : toutes les vidéos (demande du 29/09) | Retrouvées sur TikTok : @ia.boss (688 vidéos) et @unefille.ia (630 vidéos) | Collecte des légendes et sous-titres lancée (texte privé, hors dépôt), puis fiches par lots de 15 dans `connaissances/iaboss/` et `connaissances/unefille/` |
| 5gifZmpc99g | Appli mobile pour les pubs LinkedIn | Écarté : pas de publicité payante (budget 0 €) |
| dw4rYWy8nLw | 15 créations faites avec Opus 5.5 | Déjà appliqué : nos démos tiennent en un seul fichier HTML, sans bibliothèque externe |
| 2jZBhsLpe1o | 1 TikTok par jour pendant 30 jours (programme de rémunération TikTok, 10 000 abonnés requis selon la vidéo) | Hors piste pour l'instant (visage et audience nécessaires) ; gardé de côté |
| Juhkw0tL-L0 | Montage automatique de vidéos courtes (FFmpeg, HyperFrames) | Plus tard, pour une vidéo de présentation de Dig ; FFmpeg est déjà disponible gratuitement (imageio-ffmpeg) |
| s7QXxRvylrs, aBPAmYi1FfU | Sortie de Sonnet 5.5 (moins cher qu'Opus selon les vidéos) | Information générale ; rien à appliquer (pas d'API payante) |
| e2EgglFl7MQ | 30 jours de publications en 60 minutes | Idée d'offre gardée de côté : publications mensuelles pour les artisans clients (à passer à la grille avant tout) |
| HCZ3-Scx704 | 7 conseils de consignes (effort adapté, tâche entière, langage simple, « ne pas toucher », éditer sans tout réécrire) | Déjà appliqués pour l'essentiel ; rappel : phrases courtes et simples pour l'utilisateur |

### Tri TikTok du 29/09 (Unefille.ia et IA Boss)

Unefille.ia : 630 vidéos lues (42 lots). IA Boss : 40 lots sur 46 (la fin tourne). Synthèse des outils cités : `connaissances/tri-tiktok-29-09.md` (affirmations des créateurs, non vérifiées).

| Outil ou idée | Verdict |
|---|---|
| Générateurs de sites par IA (Durable, Emergent, Lovable, DeepSite, Qwen) | Concurrents ou doublons de notre générateur ; rien à installer. `same.dev` (copie d'interfaces existantes) **écarté** : risque de contrefaçon |
| n8n (automatisation) | Version « Community » gratuite en auto-hébergement (docs.n8n.io, lu le 29/09 : « Without a license key, n8n runs as the free Community edition ») mais il faut un serveur ; nos scripts Python + la routine couvrent déjà le besoin. Gardé de côté |
| IA en local (Ollama, LM Studio) | Pas de carte graphique ici ; Gemini gratuit via le relais suffit |
| Visuels par IA (Nano Banana, Krea, Recraft, Ideogram, Napkin, Canva en masse) | Pas pour les démos : photos réelles libres de droits, plus honnêtes. Napkin (schémas) et Recraft (logos) : à évaluer seulement si un client en demande |
| Wappalyzer (technologie d'un site) | Déjà couvert par notre détection de sites pour la prospection |
| NotebookLM, Perplexity, Gamma | Utiles à l'utilisateur, rien à installer ici |
| openalternative.co, OpenSourceAlternative.com (alternatives gratuites) | À ajouter à la veille si leur liste se lit automatiquement (réflexe « outil payant → équivalent gratuit ») |
| Textes par métier pour le contenu des sites clients | Déjà fait dans le générateur (thèmes par métier, textes neutres et vrais) |

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
| Second avis Gemini (lot 4 de démos, 29/09) | Légende « Façades bois » héritée du modèle peinture, fausse pour 6 artisans | **Appliqué** : légendes et textes surchargés par prospect ; règle : relire chaque texte hérité d'un modèle contre le métier réel |
| rWbVgBdl-0I (Melvynx) | Marketing d'un SaaS en public (Lumail, annuaire mcpservers.org, affiliation) | Hors piste Dig pour l'instant ; idée gardée : se faire lister dans les annuaires gratuits de son secteur |
| 5QMtCBkjvkY, JmNfV3GhVUU (gabzer) | Pubs vidéo et boutique générées par IA (Atoms, Higgsfield, bibliothèque de pubs Meta) | Bibliothèque de pubs Meta (gratuite) utile pour voir ce que font les concurrents d'un prospect ; copier la pub d'un autre : **écarté** (contrefaçon) ; outils payants non retenus |

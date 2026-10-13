# Boîte à outils DIG16 — tout ce que l'utilisateur a envoyé, classé par besoin

Créé le 12/10/2026 à la demande de l'utilisateur (« apprends toutes les compétences et outils que je t'ai envoyés,
on ne sait jamais si un jour on peut en avoir besoin »). **À consulter avant toute nouvelle tâche** : si un outil
déjà trié répond au besoin, l'utiliser ; ne pas re-trier ce qui est écarté sans fait nouveau.

- Partie 1 (écrite à la main) : **par besoin, quoi utiliser tout de suite** (déjà installé, gratuit, sûr).
- Partie 2 (automatique) : catalogue complet de chaque envoi, régénéré par `python3 outils/catalogue_outils.py`
  à partir des registres (`46-apprentissage-continu.md`, `connaissances/technologybrief-sites.md`).
- Règles qui s'appliquent à tout : budget 0 € (jamais de crédits achetés), lecture complète avant installation,
  gratuité vérifiée à la source datée, rien d'invérifié affirmé.

## Partie 1 — Par besoin : quoi utiliser

| Besoin | Prêt à l'emploi (installé et vérifié) | Plus tard / à vérifier avant usage |
|---|---|---|
| **Créer ou refaire un site client** | Skills `frontend-design`, `taste-design`, `taste-redesign`, `impeccable`, `ui-ux-pro-max`, `design-md-references`, `emil-design-eng`, `make-interfaces-feel-better`, `better-*` ; méthode du brief en 5 parties (objectif, fonctions, ressenti, contraintes, livrable) ; photos renommées avant de les donner à l'IA | Resend (formulaires par e-mail, gratuité annoncée « 3 000/mois » à vérifier) en secours de FormSubmit |
| **Animer un site** | `animate`, `motion-foundations`, `motion-patterns`, `find-animation-opportunities`, `improve-animations`, `review-animations` ; contrôle à 0/25/50/75/100 % | — |
| **Contrôler la qualité avant envoi** | `outils/test_pages.py`, `audit_site.py`, `audit_acces.py`, `qa_site.py`, `orthographe.py`, `typo_fr.py`, `lisibilite.py`, `nettete.py`, `anti_generique.py` ; skills `browser-qa`, `break-ui`, `click-path-audit`, `verification-loop`, `accessibility` ; `44-controle-qualite.md` | — |
| **Sécurité** | Hooks detect-secrets (avant commit) et ruff ; `outils/audit_securite.py` ; skills `vibe-security`, `production-audit` ; `outils/verif_metadonnees.py` (GPS des photos clients) | — |
| **Référencement (SEO, IA)** | `outils/seo_client.py` (contrôle SEO de tout site, 0 ALERTE avant livraison ; `--schema` écrit les données structurées du métier) et méthode `65-seo-sites-clients.md` ; audit OpenSEO (projet par site, gratuit sans rendu JavaScript) ; skills `seo`, `seo-audit`, `ai-seo`, `schema`, `site-architecture`, `directory-submissions` ; `outils/indexnow.py` ; OpenRush (volumes de recherche) ; Search Console, Bing Webmaster, fiche Google, Bing Places, PagesJaunes, Apple Business (12/10) | OpenSEO écarté (données payantes) |
| **Textes et vente** | Skills `copywriting`, `copy-editing`, `humanizer`, `better-writing`, `cold-email`, `offers`, `pricing`, `referrals`, `prospecting`, `brand-voice`, `brand-discovery` ; mots exacts des clients dans les textes | — |
| **Trouver et vérifier des prospects** | `outils/verif_entreprises.py` (annuaire officiel + BODACC), `radar_fermetures.py`, `suivi_siren.py`, `avis_negatifs.py` ; connecteurs Contract-Factory (SIREN), Firecrawl (crédits presque épuisés) | Vibe Prospecting, Similarweb : payants à l'usage |
| **Réseaux sociaux** | Metricool (Facebook, Instagram, Threads, TikTok, YouTube, fiche Google) ; `outils/marque/visuels_reseaux.py` ; skills `content-engine`, `marketing-campaign` | X relié à Metricool : payant (non) |
| **Vidéo et voix** (en pause jusqu'au 1er client) | Skill `motion-broll` (testé), ffmpeg, faster-whisper (transcription locale), yt-dlp ; méthode « dossier de rushes + consigne écrite » | Fish Audio / clonage de voix : identité de l'utilisateur, accord nécessaire ; générateurs vidéo IA : gratuité à vérifier |
| **Résumer des vidéos et apprendre** | Relais Vercel + Gemini gratuit (`resumer_*`, `toutes_videos.py`, `resumer_video_longue.py`) ; vidIQ en secours (crédits limités) ; veille `outils/veille_sources.py` ; ce fichier | — |
| **Gestion et argent** | Indy (compta, à ouvrir), GoCardless (prélèvements, après Indy) ; `45-impayes-se-proteger.md` ; skills `small-business:*` (factures, trésorerie) | Tableau de bord Pennylane : seulement si Pennylane est choisi |
| **Claude, agents, automatisation** | Routines 2×/jour, `outils/controle_global.py`, connecteurs (Gmail, Drive, Calendar, Metricool, Vercel, GitHub…), Jev (`typesafe-ai`), skills `search-first`, `market-research`, `product-lens` ; bonnes pratiques : une conversation par grand sujet, CLAUDE.md court servant d'aiguillage | Greffons tiers non relus (ex. claude-obsidian) : jamais sans lecture complète |
| **Statistiques de l'entreprise** | Tableau de bord DIG16 (page privée claude.ai, créé le 12/10) : Instagram, Facebook, TikTok, YouTube, Threads et fiche Google et visites du site dig16.fr (compteur Metricool sans cookie, `site-dig/mesure.js`, installé le 12/10) en direct depuis Metricool, et recherches Google (Search Console via OpenSEO, projet DIG16, lecture gratuite ; OpenRush écarté car 2 crédits payants par lecture), avec forces et faiblesses calculées sur la période choisie | Bing Webmaster (pas de connecteur), X (Metricool payant), PagesJaunes, Bing Places, Apple (fiches à valider) |
| **Documents et présentations** | Skills `anthropic-skills:pdf`, `docx`, `pptx`, `xlsx` ; `outils/documents_commerciaux.py`, `campagne_pdf.py`, `pdf_pages.py` ; connecteurs Canva, Gamma (offres gratuites) | — |

### Écartés par principe (ne pas reproposer sans fait nouveau)

- Outils qui **retirent les garde-fous** d'une IA (ex. Heretic) : refusés.
- Visages ou voix de synthèse se faisant passer pour une vraie personne (D-ID…), faux avis, fausses réalisations.
- Tout ce qui exige d'**acheter des crédits** ou une carte graphique tant que rien ne rapporte.
- Pistes abandonnées par l'utilisateur : Atlassian, LinkedIn, Bluesky, Pinterest.

<!-- catalogue-auto:debut -->

## Catalogue complet (généré automatiquement par `outils/catalogue_outils.py`)

Légende : ✅ en place · ⏳ plus tard ou à vérifier · ⛔ écarté (raison indiquée) · · simple information.

### Vidéo, voix et montage (50)

| État | Envoi / outil | Décision et usage |
|---|---|---|
| ✅ | Tester le skill motion-graphics pour une vidéo de lancement de Dig (après relecture du dépôt) | installé et testé le 01/10 (soir) : dépôt Barty-Bart/motion-graphics (skill motion-broll, MIT ; polices Geist sous licence OFL) lu en entier : moteur JavaScript pur (res… |
| ✅ | Site deviensdev.fr (guides Claude Code, hébergement gratuit, freelance) envoyé le 02/10 : lu en entier. Appli… | fait le 02/10, sauf le relais (à faire) |
| ✅ | Juhkw0tL-L0 | Plus tard, pour une vidéo de présentation de Dig ; FFmpeg est déjà disponible gratuitement (imageio-ffmpeg) |
| ✅ | Reel Facebook 2154884288767524 (01/10) | Vérifié et appliqué le 01/10 : poids publiés (Hugging Face MiniMaxAI/MiniMax-H3, 33 Md de paramètres, licence communautaire : usage commercial permis sous 20 M$/an, ment… |
| ✅ | 3ziCXSiZcTc (résumé : connaissances/sergeichyrkov/3ziCXSiZcTc.md, Sergei Chyrkov, envoyée le 07/10) | Même piste que rscb1DgJtNg (vidéos animées), donc en attente : vidéos en pause jusqu'au premier client. Le jour venu : préférer la méthode Canvas + FFmpeg (déjà installé… |
| ✅ | ySLnUg8xNcg (résumé : connaissances/melvynx/ySLnUg8xNcg.md, Melvynx, envoyée le 07/10) | Confirme notre choix (rscb1DgJtNg, 3ziCXSiZcTc) : le jour où des vidéos seront faites, moteur léger Playwright + FFmpeg, déjà installé et gratuit. En attente : vidéos et… |
| ✅ | WaOkvUNisN4 (résumé : connaissances/colinblain1/WaOkvUNisN4.md, Colin Blain, envoyée le 07/10) | Même piste que rscb1DgJtNg et 3ziCXSiZcTc : vidéos en pause jusqu'au premier client. Le jour venu : méthode Canvas + FFmpeg (déjà disponible) ou HyperFrames, après lectu… |
| ✅ | YKFpSe28mlg (30/09) | Appliqué gratuitement : filme une démo de site au format téléphone (défilement complet, ~30 s, MP4 lisible sur iPhone) pour l'envoyer au prospect par SMS ou email ; test… |
| ✅ | Reel Instagram DeKKVtGtjFx (compte « madameb0nplan », envoyé le 08/10 ; légende lue sur la page d'intégration… | Rien à installer : le connecteur Gamma est déjà branché ici (102 thèmes disponibles). Usage possible plus tard : présentations ou fiches à montrer en rendez-vous. Le sit… |
| ✅ | Page Notion « 7 GitHub Repos That Make You Wonder Why They're Free » (envoyée le 08/10 ; lue en visiteur, lic… | Rien à installer. Les quatre premiers et Magnitude demandent un ordinateur puissant (carte graphique) ou une clé d'IA payante, sans lien avec la demande prouvée (règle n… |
| ✅ | Demande du 10/10 : « installe tous les outils, skills et dépôts que je t'ai donnés » (accord général de l'uti… | Installé le 10/10 dans .claude/skills/ (tout relu ou contrôlé avant : texte seul, licences MIT, aucune commande cachée) : 13 skills de Jakub Krehel (better-*, interface-… |
| ✅ | Reel Instagram DeR5e83kV1C (compte « _eazyclick », envoyé le 10/10 ; vidéo transcrite en local, connaissances… | Déjà en place : Impeccable, Taste (taste-design, taste-redesign), Playwright (connecteur + outils/test_pages.py). Appliqué le 10/10 : règles d'animation d'Emil Kowalski… |
| ✅ | Carrousel Instagram Dd2tZCCDofx (compte « aitechorigin », envoyé le 09/10 ; légende et 10 images lues depuis… | Mixpost (licence MIT) et Shoutrrr (licence Apache 2.0, lues sur leurs dépôts le 09/10) : solution de secours de Metricool, notée dans 63-kit-branchement-reseaux.md § 4 :… |
| ✅ | Vidéo YouTube DBQqB8eqpFI (envoyée le 09/10) | Déjà en place chez nous : la vidéo de présentation DIG16 (33 s) est faite exactement ainsi, animation en HTML enregistrée, voix de synthèse Google (Algieba), musique et… |
| ✅ | Vidéo YouTube rkK8ZyzYyEA (envoyée le 09/10) | Déjà installés chez nous : Impeccable et les skills marketing (copywriting, cold-email, prospecting, offers…) sont dans .claude/skills ; « grill-me » ≈ notre skill brain… |
| ✅ | Vidéo YouTube gyVqYy5yDK8 (envoyée le 12/10) : un créateur solo délègue son montage vidéo à Claude | Noté : vidéos en pause jusqu'au 1er client ; quand elles reprendront, même méthode (dossier de rushes + consigne écrite) avec nos outils gratuits (ffmpeg, faster-whisper… |
| ⏳ | 96G4KDnEFyI (Anthony Shoosh) | Piste d'option à valider, pas à construire. Vérifié le 01/10 : Retell (retellai.com/pricing) offre 10 $ de crédits gratuits, puis environ 0,07 à 0,31 $/minute (exemple :… |
| ⏳ | O_4l1rPsWTM (Système Gagnant) | Hors piste, rien à construire. Vérifié le 01/10 sur flick.art/pricing : offre gratuite « 300 credits to start + 100 every week », formules payantes Casual (500 crédits/m… |
| ⏳ | vqMhGnep1H0 (Jornada Digital, 10 min, en portugais) | Noté, à vérifier à la source avant usage (quota et licence affichés sur theresanaiforthat.com le jour J) ; piste pour de courts visuels animés des démos Dig, sans achat.… |
| ⏳ | hImo2S4HOGI | Plus tard (vidéo de présentation Dig), consomme des crédits |
| · | Pages Facebook IA Boss (@iabossai) et Unefille.ia : toutes les vidéos (demande du 29/09) | Collecte des légendes et sous-titres lancée (texte privé, hors dépôt), puis fiches par lots de 15 dans connaissances/iaboss/ et connaissances/unefille/ |
| · | Outil créé | Testé le 30/09 sur ces 4 reels : fonctionne |
| · | 0m0FJJjAWyE (Lucas Montano, 18 min) | Rien à changer. Cohérent avec la règle Dig : budget 0 € tant que rien ne rapporte, puis l'outil se paie avec les premiers clients. Résumé : videos-resumes/0m0FJJjAWyE.md |
| · | 7XTYaVrt4QM (podcast « opensource », Léo Grindars, 1 h 49, envoyé le 02/10, résumé en 6 morceaux) | Conforte la piste principale, rien de nouveau à construire. Le second axe (reprendre un logiciel qui a déjà des utilisateurs plutôt que partir de zéro) est exactement la… |
| · | 05ody6JKf1Y | Réflexion générale ; vente en direct sans intermédiaire = déjà le modèle de Dig |
| · | Vidéo courte pour les réseaux | Montage gratuit en 1080p, sous-titres automatiques |
| ⛔ | Skills de design gratuits pour des démos moins « génériques » : Taste Skill, Impeccable, Awesome DESIGN.md (e… | fait le 29/09 : Taste Skill (MIT) et Impeccable (Apache 2.0) récupérés et examinés. Taste Skill vise React et les installations de paquets et utilise des images de rempl… |
| ⛔ | Petit outil gratuit sans inscription sur le site de Dig (« votre entreprise est-elle trouvable sur Google et… | écarté le 01/10 (grille) : OpenRush (France, 01/10) ne trouve aucune recherche pour « tester visibilité google entreprise » ; « audit fiche google gratuit » ne remonte q… |
| ⛔ | Ajout n°14 de prospects (nouveaux numéros à partir de 350) | passage du 01/10 (soir) : les 13 derniers candidats du vivier RGE vérifiés un par un (domaines, web, téléphone, registre, BODACC, Pappers) : 0 retenu, tous avaient un si… |
| ⛔ | 6 reels Instagram (enfin lus le 29/09 : yt-dlp + ffmpeg + Gemini) | Design des démos : Taste Skill, Impeccable, Awesome DESIGN.md (gratuits et libres selon les vidéos) : à évaluer, avec lecture complète du code avant toute installation (… |
| ⛔ | x.com/chesny 2105326525239415230 (12 min) | Écarté pour l'instant selon la grille : pas de demande prouvée pour nous, outils payants (ElevenLabs, Midjourney), et risque réel vérifié à la source : les règles de mon… |
| ⛔ | x.com/chesny 2104152789446459811 (13 min, envoyée le 30/09) | Écarté, mêmes raisons que la vidéo ci-dessus (règles YouTube vérifiées, outils payants, pas de demande prouvée). Idée retenue : Claude Code peut piloter une série d'imag… |
| ⛔ | Message transmis le 30/09 (auteur : formation Agentic Academy) : « Jarvis + Fish Audio » | Vérifié, non installé : Jarvis exige un ordinateur local (micro, Chrome, Claude Code connecté) → inutilisable dans notre environnement distant ; code sérieux (contrôle d… |
| ⛔ | 68v_T0jrysM (YouTube, 30/09, Albert Olgaard) | Retenu pour plus tard (quand Dig fera ses propres vidéos ou des vidéos pour les artisans) : équivalent gratuit de la transcription = Whisper en local (logiciel libre), p… |
| ⛔ | Contrôle de tous les liens envoyés depuis le début (01/10) | 2 oubliés rattrapés : EpUH6g6GUDE (short animalier, rien à appliquer) et reel Ddi-RfYAATK (formation à 247 € créée avec Claude et TinyPages ; TinyPages à 24 €/mois, paya… |
| ⛔ | rscb1DgJtNg (résumé : connaissances/chaseai/rscb1DgJtNg.md, Chase AI, envoyée le 07/10) | Constaté : tout le nécessaire gratuit est déjà dans le conteneur (Playwright + Chromium, FFmpeg). En attente (vidéos et réseaux en pause jusqu'au premier client, décisio… |
| ⛔ | reel DeMO5D0AUBq (résumé : connaissances/reels/DeMO5D0AUBq.md, henriexploria, envoyé le 07/10) | Écarté : même famille que l'essai 3D jugé laid le 07/10 ; effets lourds sur téléphone et contraires à « Facile à appeler » ; aucun artisan ne l'a demandé. Outil amélioré… |
| ⛔ | YZXyFlSvLgo | Non résumé : direct sans sous-titres lisibles (Gemini refuse, transcription vidIQ en erreur ; seules les informations publiques de la vidéo ont été lues). Écarté par pru… |
| ⛔ | IWA9LCvNW8g (Alejavi Rivera, 27 min) | Noté, rien à construire. Offres gratuites à revérifier à la source le jour où un client demande une courte vidéo de présentation ; deux pratiques écartées (retrait de fi… |
| ⛔ | 1hkTJ8wg9bY (Adrián Sáenz, podcast de 1 h 37 avec Jordi Segués, résumé en 5 morceaux) | Noté, rien à construire : la piste « contenu YouTube/Reels » a déjà été écartée par la grille (aucune demande mesurée, 01/10). Deux idées gardées pour Dig : répondre aux… |
| ⛔ | 7RVf25Rg0Mc | Écarté : demande un serveur allumé en permanence ; nos routines font l'essentiel |
| ⛔ | 5 reels Facebook | Détail : videos-resumes/reels-facebook-28-09.md ; Klap écarté (contrefaçon) |
| ⛔ | Publication Instagram DeMr4aFiCvy (compte « futuretech », 07/10, envoyée le 08/10 ; légende lue sur la page p… | Rien à installer. Poe : inutile ici (Claude fait déjà le travail). Learn-Anything, Delphi, Turbo : sans lien avec la demande prouvée (règle n° 1). ViralityAI : piste pou… |
| ⛔ | Carrousel Instagram DeCV78sETMT (compte « esc8pe.reality », 03/10, envoyé le 08/10 ; 16 images lues depuis la… | Rien à installer. openalternative.co : déjà dans la veille quotidienne. DownSub : piste de secours gratuite pour les vidéos que Gemini ne lit pas (avant vidIQ, qui conso… |
| ⛔ | Reel Instagram DeRhu46NmhK (compte « kingarms.ai », envoyé le 09/10 ; résumé : connaissances/reels/DeRhu46Nmh… | Écarté : copier le fonctionnement ou l'apparence d'un logiciel ou d'un site existant expose à la contrefaçon (droit d'auteur, dessins et modèles) et viole souvent les co… |
| ⛔ | Carrousel Instagram DeGDWLNDm86 (compte « aitechorigin », envoyé le 09/10 ; légende et 10 images lues depuis… | Rien à installer : ce sont des outils pour développeurs qui font tourner leurs propres agents sur leur ordinateur ; nos sessions tournent dans le cloud et ont déjà leur… |
| ⛔ | Vidéo YouTube sGt1ACELN4k (envoyée le 09/10) | Rien à installer maintenant : il faut un ordinateur avec le logiciel de montage (nos sessions tournent dans le cloud) et les vidéos courtes (TikTok, Shorts) ne viennent… |
| ⛔ | Vidéo YouTube Fuo1i_-9Frc (envoyée le 09/10) | Rien à installer maintenant : nos besoins d'images, de PDF et de vidéo sont déjà couverts par des outils éprouvés (Pillow, Playwright, PyMuPDF, ffmpeg) ; logiciel très j… |
| ⛔ | Vidéo YouTube 4aUVjc7ttko (envoyée le 09/10) | Rien à installer (pas de podcast ; Riverside payant). Conseils retenus pour la future vidéo verticale « Le test du pouce » (15 s) : démarrer directement sur la phrase fo… |
| ⛔ | Vidéo YouTube 1RqsrzT9-CI (12/10) : clonage de voix et traduction avec Fish Audio | Écarté : vidéos en pause ; cloner la voix de l'utilisateur toucherait à son identité (accord nécessaire) ; gratuité de l'API à vérifier. Idée « plusieurs variantes à tes… |

### Images et visuels (38)

| État | Envoi / outil | Décision et usage |
|---|---|---|
| ✅ | Vérifier les photos fournies par les clients avec outils/verif_metadonnees.py (position GPS) | fait (outil prêt ; 22 images du site : propres) |
| ✅ | Skills UI UX Pro Max et agent-skills (code externe relu, licence MIT) | UI UX Pro Max installé le 30/09 après accord de l'utilisateur |
| ✅ | Image « prompt équipe d'agents IA » | Appliqué : prompts/equipe-agents-ia.md (prompt recopié + équipe de Dig décrite) ; manque repéré : mesurer le résultat des appels → colonne « Résultat de l'appel » propos… |
| ✅ | Liste public-apis (GitHub, 30/09) | Appliqué : ajoutée à la veille quotidienne ; pistes retenues dans 33-outils.md (marchés publics BOAMP = preuve de demande payante, gardée pour après la création ; simula… |
| ✅ | Consigne de l'utilisateur (30/09, permanente) | Appliqué aussitôt : skills UI UX Pro Max + 12 skills marketingskills installés (lus en entier, MIT) ; méthode de prospection enrichie (outils/prospects/LISEZMOI.md) ; au… |
| ✅ | pZgw2WNOcHE (YouTube, 30/09, Codesistency, 3 h 42, résumé en 12 morceaux le 01/10) | Appliqué : 2 règles de sécurité ajoutées à 44-controle-qualite.md (webhooks signés, mode sandbox, .env.local hors Git, limite d'appels IA ; intégrations depuis la doc of… |
| ✅ | Reel Instagram DdoWZFCOhPZ (sadie.ontech, 01/10) | Appliqué : skills taste-design, taste-redesign (MIT, leonxlnx/taste-skill) et impeccable (Apache 2.0, pbakaus/impeccable) installés dans .claude/skills après lecture, pa… |
| ✅ | dFdULRWj_Qs (résumé : connaissances/gustens/dFdULRWj_Qs.md, Gusten Sun, envoyée le 07/10) | Déjà appliqué : modèle réutilisable d'un client à l'autre (démos DIG16), couleur de la démo tirée du logo du client, tout fait avec Claude Code, hébergement gratuit (pas… |
| ✅ | Vidéo YouTube we6zrIsVovw (envoyée le 12/10) : site d'artisan de A à Z avec Claude Code + GitHub + Vercel + R… | Trié : rien de nouveau à installer ; Resend (formulaires par e-mail, gratuité annoncée « 3 000 e-mails/mois » à vérifier à la source) noté comme solution de rechange à F… |
| ⏳ | Nano Banana (images Gemini) | Possible pour des visuels neutres avec la mention « image générée par IA », jamais pour de fausses réalisations ; offre gratuite à vérifier avant usage |
| ⏳ | Zsky AI | inconnu jusqu'ici : à vérifier (sérieux, droits d'usage commercial) avant essai |
| · | Visuels par IA (Nano Banana, Krea, Recraft, Ideogram, Napkin, Canva en masse) | Pas pour les démos : photos réelles libres de droits, plus honnêtes. Napkin (schémas) et Recraft (logos) : à évaluer seulement si un client en demande |
| · | Image « Les outils IA qui te rendent inarrêtable » (35 outils) | Aucune offre gratuite affirmée sans vérification à la source. Déjà couverts : Gamma et Canva (connecteurs), Claude Artifacts, Playwright pour les vidéos de démo. Durable… |
| · | Hedra, Hailuo, Vista, Ideogram, Open Design | Pas de besoin immédiat ; offres gratuites non vérifiées, à revoir si une vidéo ou un visuel Dig est décidé |
| · | Photos d'un client trop lourdes | Compresser/convertir dans le navigateur, rien n'est envoyé (complète nos scripts Pillow) |
| · | Photos d'un client floues ou anciennes | Netteté de vieilles photos de devanture ou de réalisations — seulement avec l'accord du client |
| · | Détourer un produit, une enseigne | Fond retiré (aperçu gratuit ; Photoroom gratuit avec filigrane) |
| · | Retouche sans logiciel | Éditeur type Photoshop dans le navigateur (gratuit avec publicité) |
| · | Couleurs d'un site client | Palette à partir de la couleur du logo (règle des démos : couleur tirée du logo) |
| · | QR code, conversions d'images hors ligne | Outils locaux, open source, sans compte |
| · | Vérifier qu'une photo n'est pas une photo de banque d'images ou d'un tiers | Recherche d'image inversée (gratuit, usage non commercial) : complète marque_stock.py avant de mettre une photo dans une démo |
| · | Légendes de publications | Idées de légendes à partir d'une photo (à réécrire selon la charte) |
| · | Anciennes versions d'un site prospect | Déjà utilisé (photos_archives.py) ; bloqué depuis le conteneur, à ouvrir sur le téléphone de l'utilisateur |
| ⛔ | Lire puis installer, s'ils sont sûrs, les skills Impeccable (contrôle visuel des marges, alignements, couleur… | fait autrement : Impeccable télécharge et lance un programme tiers, donc non installé ; ses règles d'audit sont reprises dans outils/audit_acces.py (site et 12 démos cor… |
| ⛔ | Image « Top 10 skill repos » (classement par étoiles, chiffres non vérifiés) | Superpowers : déjà actif. Impeccable : déjà écarté le 29/09 (programme tiers téléchargé au lancement). UI UX Pro Max (MIT, script Python local sans réseau, relu) et agen… |
| ⛔ | Reel Instagram DdzfOd_Dd9h (30/09) | Taste Skill : déjà examiné le 29/09 (règles dans anti_generique.py) ; Playwright : installé le 30/09 (MCP). Appliqué : règles de Vercel lues à la source (vercel.com/desi… |
| ⛔ | flL6i2L2Oks (résumé : connaissances/zeynebmadi/flL6i2L2Oks.md, Zeyneb Madi, envoyée le 07/10) | Appliqué le 07/10 sur demande de l'utilisateur (« je veux que mes sites puissent ressembler à ça ») : étude complète dans 59-site-immersif.md (analyse image par image, s… |
| ⛔ | 7-sLfX-K8K4 (résumé : connaissances/summiajamshed/7-sLfX-K8K4.md, Summia Jamshed, envoyée le 07/10) | Appliqué dans 58-fiche-google-mensuelle.md. Corrigé : la vidéo dit « 750 mots » pour la description, il s'agit d'une limite en caractères (à vérifier dans l'interface) ;… |
| ⛔ | tKHcz5SGN9o (résumé : connaissances/kyleslyf/tKHcz5SGN9o.md, Kyle (kyleslyf), envoyée le 07/10) | Déjà appliqué : sites DIG16 faits avec Claude Code, hébergés gratuitement sur Cloudflare, retouches contrôlées par captures (44-controle-qualite.md). Écarté : Higgsfield… |
| ⛔ | Colonne « payant » (Midjourney, HeyGen, Cursor, ElevenLabs, Canva Pro…) | Écartée : budget 0 € |
| ⛔ | Carrousel Instagram Dde3xh9EYkM (compte « information.ia », envoyé le 08/10 ; 12 images lues depuis la page d… | Pomelli : retenu pour la publicité de DIG16 (61-plan-publicite.md) : à essayer sur dig16.fr le jour de l'ouverture pour des visuels de publications ; la France figure su… |
| ⛔ | Captures du 10/10 : liste de cours Udemy gratuits par coupons (« tant qu'il reste des places » ; adresse de l… | Trié : 12 utiles à DIG16 retenus pour l'utilisateur (fiche Google et référencement local, référencement dans les réponses des IA, prospection, emailing, LinkedIn, IA pou… |
| ⛔ | Vidéo YouTube fq3wx-AR6B0 (envoyée le 09/10 ; résumé Gemini via le relais) | Déjà appliqué pour l'essentiel : références et boucle de critiques = nos skills de design et les contrôles automatiques (marges, chevauchements, rendu téléphone) de camp… |
| ⛔ | Vidéo YouTube lDrAZ1wAyVs (envoyée le 09/10) | Rien à installer (mêmes raisons que xvy40dHyAmw : session dans le cloud). Idée retenue de Reflect : chaque correction de l'utilisateur devient une règle écrite pour ne p… |
| ⛔ | Vidéo YouTube xWuLotc8zjE (envoyée le 09/10) | Déjà appliqué : l'utilisateur pilote depuis l'application ; connecteurs Gmail, Drive, Metricool déjà utilisés ; un dossier par sujet (chasse-demande/, connaissances/, su… |
| ⛔ | Liste « websites » de technologybrief.io (envoyée le 11/10, 148 sites) | Appliqué : 23 retenus pour DIG16 avec leur moment dusage, 3 concurrents notés pour largumentaire, le reste écarté (hors sujet ou payant) → connaissances/technologybrief-… |
| ⛔ | Vidéo YouTube hRr-yUSM0_A (envoyée le 12/10) : « cloner Higgsfield » avec Claude Code et revendre des générat… | Écarté pour l'instant : API et crédits payants (budget 0 €), hors cœur DIG16 ; idée « visuel IA avant/après » gardée comme option future pour les clients artisans (cuisi… |
| ⛔ | D-ID | écarté : visage de synthèse, contraire à la règle « pas de promesse invérifiable » et à l'image locale de DIG16 |

### Création de sites et design (59)

| État | Envoi / outil | Décision et usage |
|---|---|---|
| ✅ | Contrôle qualité : toute animation vérifiée à 0, 25, 50, 75 et 100 % de sa durée | fait (ligne déjà présente dans 44-controle-qualite.md) |
| ✅ | Chercher avec vidIQ les questions les plus demandées sur les sites d'artisans (vidéos « outliers ») : preuve… | fait le 01/10 (soir), résultat négatif et cohérent avec OpenRush : sur YouTube France, « site internet artisan » et toutes ses variantes (création, plombier, électricien… |
| ✅ | Ressources gratuites de design (polices Fontshare, icônes, composants) pour les démos | fait le 01/10 : licence Fontshare (ITF Free Font License, lue sur fontshare.com) = gratuite, usage commercial permis pour ses propres sites, mais interdit de la fournir… |
| ✅ | Fiche Notion « La config Claude Code du gagnant du hackathon Anthropic » envoyée le 04/10 (présente le dépôt… | fait le 04/10 : AgentShield 1.6.0 lancé avec l’accord de l’utilisateur ; note D (53/100) → C (67/100) : liste d’interdictions ajoutée (force-push, reset --hard, rebase,… |
| ✅ | Parrainage client | Validé (variante A) et appliqué le 28/09 : site, guide, 47-parrainage.md |
| ✅ | Consignes courtes pour les skills (le modèle sait déjà faire) | Déjà le cas pour nos skills |
| ✅ | dw4rYWy8nLw | Déjà appliqué : nos démos tiennent en un seul fichier HTML, sans bibliothèque externe |
| ✅ | Textes par métier pour le contenu des sites clients | Déjà fait dans le générateur (thèmes par métier, textes neutres et vrais) |
| ✅ | Reel DdwPRaOCTZI (30/09) | Tous = code externe : installation bloquée par la sécurité automatique → décision de l'utilisateur (même cas qu'UI UX Pro Max). OmniRoute : écarté (fait transiter nos re… |
| ✅ | Reel Da5njFZMGCK (30/09) | UI UX Pro Max : déjà installé le 30/09. Magic MCP (devenu « 21st AI ») : écarté, page tarifs lue le 30/09 : offre gratuite sans crédits d'IA mensuels (« Monthly AI credi… |
| ✅ | UcvD53jqHRU (résumé : connaissances/markkashef/UcvD53jqHRU.md, Mark Kashef, envoyée le 07/10) | Déjà en place : travail en parallèle (sous-agents avec le modèle choisi), auto-vérification (controle_global.py, audit_site.py, contrôle 44). Écarté : Codex et pilotage… |
| ✅ | 3d_M6knAKZw (résumé : connaissances/bluewiremedia/3d_M6knAKZw.md, Bluewire Media, envoyée le 07/10) | Déjà en place : Gmail, Google Drive, GitHub, Vercel et Cloudflare branchés ; publication du site par push ; CLAUDE.md sert de « cerveau ». Composio : à regarder seulemen… |
| ✅ | KFYihErgHEk (résumé : connaissances/lukefinance100/KFYihErgHEk.md, Luke (lukefinance100), envoyée le 07/10) | Déjà en place : points automatiques planifiés, règle « aucun chiffre inventé ». Noté pour plus tard : un tableau de bord à adresse fixe (clients, paiements) quand il y a… |
| ✅ | 1a5HxU52vCQ (Greg Isenberg, 54 min, résumé en 3 morceaux de 20 min) | Méthode retenue, pas de nouveau produit. Appliqué le 01/10 : deux questions « chiffrer ce que ça lui coûte » ajoutées au questionnaire de découverte (41, questions 21 et… |
| ✅ | gwKurw7tk7g (9 min) « Claude Opus 5 m'a créé un site à 10.000€ en un prompt ! » | Déjà appliqué pour l'essentiel : les skills ui-ux-pro-max et impeccable sont installés et imposés sur chaque démo (routine, point 5). Magic UI est une bibliothèque React… |
| ✅ | Page Obsidian Publish de Loucash, lue le 02/10 ; chaque dépôt vérifié sur GitHub (README ; Task Observer : SK… | 2 déjà installés (Superpowers, Impeccable), 3 écartés : Skills CLI (programme npm non relisible ; SearchSkills et chercher_skills.py font déjà le travail), Claude Mem (d… |
| ✅ | kYNwdRnb4ks | Déjà appliqué presque entièrement |
| ✅ | Second avis Gemini (lot 4 de démos, 29/09) | Appliqué : légendes et textes surchargés par prospect ; règle : relire chaque texte hérité d'un modèle contre le métier réel |
| ✅ | Vidéo YouTube UJtjPXpuOcY (envoyée le 09/10, « Beginner to First Million with AI in 2026 », Albert Olgaard, 1… | Déjà en place : skills Claude dans .claude/skills/, plugin Superpowers installé, plan avant construction (grille 00), vidéo courte « Le test du pouce » faite le 09/10 (v… |
| ✅ | Vidéo YouTube S8sQeFy9VbQ (12/10) : la « zone grise », fabriquer ses propres petits outils avec Claude Code | Appliqué : c'est notre façon de faire (outils/ maison) ; le modèle en 5 parties est retenu pour les demandes de sites clients (brief). |
| ✅ | Reel Instagram DeYKx9fgENd (13/10, compte openrushdata) : « Turn Claude into your SEO analyst. Live rankings,… | Déjà en place : OpenRush est branché depuis le 28/09 (33-outils.md), utilisé pour les volumes de recherche, l'analyse des sites et des résultats Google. Search Console d… |
| ⏳ | Site buildyoursaas.tech envoyé le 02/10 (accompagnement payant pour apprendre Claude Code aux dirigeants de p… | lu le 02/10 ; (a) et (b) à faire au premier appel |
| ⏳ | CL7EINYSoKw | Idée notée pour Dig, non construite (règle n° 1) : plus tard, proposer aux clients artisans des modules en plus du site, par exemple un assistant de devis pour le bâtime… |
| · | Page d'arrivée alignée mot pour mot sur le message de prospection | à appliquer aux prochains messages |
| · | Tarif « forfait + usage » ; ne pas miser sur le SEO au démarrage d'un logiciel | Pas pour Dig aujourd'hui (offre de sites à prix fixe) |
| · | Wappalyzer (technologie d'un site) | Déjà couvert par notre détection de sites pour la prospection |
| · | Reel DdoriFMjS-t (30/09) | Pas nécessaire : Firecrawl (connecteur), le relais et nos scripts couvrent déjà ce besoin |
| · | Guide « Pennylane : ton dashboard de gestion en un prompt » (0xloucash, envoyé le 01/10) | Pas pour maintenant : Pennylane payant (budget 0 €, et Dig n'a pas encore d'entreprise). Repris : (1) la facturation électronique (réception 01/09/2026, émission 01/09/2… |
| · | oMw4JdxoX_A (résumé : connaissances/hrishikeshroyofficial/oMw4JdxoX_A.md, Hrishikesh Roy, envoyée le 07/10) | Déjà notre modèle : skills, CLAUDE.md, aucun envoi sans accord de l'utilisateur. Rien de nouveau à appliquer |
| · | e7t6YTrqznM | Hors piste actuelle (on reste sur les sites) |
| · | TWhoNLkUXKY | Piste à passer à la grille ; marché encombré |
| · | _SVU3oC4JX8 | Actions n° 1 et 5 |
| · | Traduction (démo Prestige FR/EN) | Texte et documents (gratuit plafonné) |
| · | Tester le formulaire du site | Boîte jetable pour essayer FormSubmit sans polluer la vraie boîte |
| · | Forums où des artisans parlent de leur site | Repérer les plaintes et besoins réels (preuve de la demande) |
| ⛔ | Passer chaque document important dans /api/avis (second avis) avant de l'envoyer | appliqué le 28/09 sur les textes des 7 démos du lot 2 (gemini-3.5-flash-lite) : 4 corrections retenues (phrase répétée non vérifiée, « petits prix », « à la minute ») ;… |
| ⛔ | Référencement des clients : OpenSEO (gratuit ?), GEO Optimizer, fichier llms.txt, fiche Google ; vérifier l'o… | fait le 29/09 : OpenSEO écarté (logiciel gratuit mais données DataForSEO payantes à l'usage ; OpenRush gratuit suffit). GEO Optimizer (MIT, 58 000 lignes : pas installé)… |
| ⛔ | Synthèse des 30 vidéos prioritaires Melvynx + Matt Wolfe (promise au 25 %) | fait le 01/10 : affirmations relues dans les fiches, offres gratuites vérifiées à la source (Wispr Flow confirmé, Relume écarté) ; skill officiel frontend-design install… |
| ⛔ | Réaudit des 285 prospects déjà remis (282 annoncés à tort avant le contrôle croisé du 01/10) (question de l'u… | terminé le 01/10 (soir) pour toutes les fiches « sans site » (91 fiches contrôlées) : 4 erreurs (4 entreprises avaient un site actif) → retirées, mêmes numéros ; 9 fiche… |
| ⛔ | Kit de skills de design jakubkrehel/skills (MIT, texte seul, relu le 29/09) | Non installé (des consignes de relecture, pas un outil). Ses règles mesurables ont été contrôlées sur les démos : champs de formulaire ≥ 16 px sur téléphone (17 px), lig… |
| ⛔ | Capture « Les outils IA qui te rendent inarrêtable » (reel Instagram) | Détail : videos-resumes/outils-ia-instagram-29-09.md. Durable est un concurrent direct (site gratuit, puis 25 $/mois) : on garde ses bonnes idées gratuites (fiche Google… |
| ⛔ | Générateurs de sites par IA (Durable, Emergent, Lovable, DeepSite, Qwen) | Concurrents ou doublons de notre générateur ; rien à installer. same.dev (copie d'interfaces existantes) écarté : risque de contrefaçon |
| ⛔ | Reel DdeuDY-gSjX (30/09) | Idée déjà appliquée à notre échelle (prompts/equipe-agents-ia.md : 4 rôles suffisent). Contenu externe non installé (même règle de sécurité) ; à relire seulement si un b… |
| ⛔ | agentic-academy.fr (page gratuite d'une formation payante : 47 €/mois ou 147 €, 30/09) | Appliqué sans rien installer : l'annuaire a une recherche publique en lecture seule → outils/chercher_skills.py (à utiliser lors de la recherche quotidienne de skills).… |
| ⛔ | TuiF6yIeLG4 (résumé : connaissances/webmarketingtuto/TuiF6yIeLG4.md, 18 min) | Déjà appliqué : DIG16 est déjà fait avec Claude Code, hébergé gratuitement sur Cloudflare Pages (0 € ; moins cher que Hostinger), avec compte propre au nom du client (dé… |
| ⛔ | vwzV-YsVswA (résumé : connaissances/jonocatliff/vwzV-YsVswA.md, Jono Catliff, envoyée le 07/10) | Appliqué : procédure écrite 58-fiche-google-mensuelle.md (l'offre promettait un suivi mensuel de la fiche Google sans procédure). Écarté : le « filtre » qui n'envoie ver… |
| ⛔ | Lien envoyé le 07/10 (message automatique ManyChat du reel DeMO5D0AUBq ; lien de suivi non recopié) | Déjà évalué le 02/10 (33-outils.md, guide Loucash) : non installé, car il copie des skills sans lecture préalable ; on garde la méthode actuelle : recherche dans skills.… |
| ⛔ | kS6xCG6oljU | Déjà appliqué : connecteurs Gmail, Drive, GitHub, Vercel ; skill Impeccable installée ; pages partagées par artefact. Ajouté : skills.sh (répertoire de plus de 10 000 sk… |
| ⛔ | WD4cCugw0Y0 | Écarté : YouMind (crédits, sponsor). Appliqué en méthode : un seul document de contexte de marque avant toute création (pour Dig : 39-business-plan-sites.md et le site)… |
| ⛔ | MDZoiwPl2QU (Alejavi Rivera, 32 min) | Noté, rien à construire. Stitch : à tester seulement si une maquette rapide est demandée par un client (nos skills de design couvrent déjà le besoin). VPN : écarté (idem… |
| ⛔ | Page Notion d'ExplorIA (Henri), lue le 02/10 ; chaque dépôt vérifié sur GitHub | 1 installé, 4 écartés. Installé : diagram-design (MIT) en texte seul dans .claude/skills/diagram-design/ — schémas propres pour les supports et le site. Écartés : agent-… |
| ⛔ | LCwT00LrPZg | Action n° 1 ; « caveman » écarté (réponses trop sèches pour l'utilisateur) |
| ⛔ | _To3N8UTh94 (30/09) | Déjà notre modèle (service propulsé par l'IA, règle n° 1, listes de prospects, textes d'appel). Nouveau : débriefing après appel (l'utilisateur dicte ou colle ses notes,… |
| ⛔ | Veille du 10/10 (reprise à la demande de l'utilisateur : « je veux que tu t'améliores constamment », après 5… | Trié : rien à installer en urgence. Noté comme solution de secours : Formgong (réception de formulaires, offre gratuite de 300 messages par mois selon l'annuaire free-fo… |
| ⛔ | Vidéo YouTube xvy40dHyAmw (envoyée le 09/10) | Rien à installer ici : nos sessions tournent dans le cloud, pilotées depuis le téléphone, et les mods modifient l'interface du terminal ou de l'application de bureau. Le… |
| ⛔ | Vidéo YouTube 58MtToM79w4 (envoyée le 09/10) | Rien à installer : le formulaire du site part par FormSubmit (gratuit) à contact@dig16.fr et le suivi des demandes est le tableau privé de 50 § 8 ; Replit est payant (bu… |
| ⛔ | Carrousel Instagram @choly.ai « Hidden websites » (envoyé le 12/10) | Trié : rien à installer (vidéos en pause jusqu'au 1er client) ; gratuités à vérifier à la source ; D-ID écarté (visage de synthèse) → connaissances/technologybrief-sites… |
| ⛔ | Veille du 11/10 (veille/2026-10-11.md) | Trié : rien à installer. Noté pour plus tard : OpenRegistry (registres officiels de 80 pays dont la France, en secours de verif_entreprises.py) et Brevo (secours e-mail… |
| ⛔ | Veille du 13/10 (veille/2026-10-13.md) | Trié : rien à installer. Relvato (surveillance de site) = doublon de controle_global.py ; Domain Info / QR LifeStep = déjà couverts par nos outils ; Master Setter (API c… |

### Référencement et visibilité (5)

| État | Envoi / outil | Décision et usage |
|---|---|---|
| ✅ | S9n8vPvoHFk (YouTube, 30/09, chaîne « AI Master ») | Écarté (payant). Équivalents gratuits déjà en place : routage = OmniRoute (installé) et l'aiguilleur de Jev ; comparaison = second avis Gemini via /api/avis ; tâches pla… |
| ✅ | g68Rxhg-W1s | Déjà appliqué (aiguilleur jev_trier_reponses.py). Idée notée, non construite (règle n° 1 : vérifier l'argent avant) : un service d'analyse en masse des avis clients des… |
| · | rWbVgBdl-0I (Melvynx) | Hors piste Dig pour l'instant ; idée gardée : se faire lister dans les annuaires gratuits de son secteur |
| ⛔ | Reel DdmcP6BlU6u (30/09) | Écarté : extraction de profils sur des réseaux qui l'interdisent dans leurs conditions, et données personnelles (cadre CNIL, 35-demarchage-cadre-legal.md) ; nos sources… |
| ⛔ | _9ZGlLWr6UE | Codex payant : écarté ; appliqué en gratuit : /api/avis (second avis Gemini) |

### Prospection et vente (16)

| État | Envoi / outil | Décision et usage |
|---|---|---|
| ✅ | Reel Instagram DVolgosjH7u (danyltn, enfin lu le 01/10) | Le connecteur est déjà branché sur cette session. Recherche possible, mais chaque export est payé en crédits (« one-time purchases ») : non utilisé (budget 0 €). Nos pro… |
| ✅ | 7M3yVIyWUQ0 (résumé : connaissances/theecomking/7M3yVIyWUQ0.md, THE ECOM KING, envoyée le 07/10) | Noté, pas lancé : c'est un autre métier (vente en ligne à des particuliers, publicité payante, Shopify payant), hors priorité des 30 jours (preuve de la demande DIG16) e… |
| ✅ | 6yuGG_vKKXQ | Pour plus tard (quand Dig aura ses premiers clients) : témoignages de clients et avant/après comme preuve sociale ; une vente à plusieurs centaines d'euros se conclut av… |
| ✅ | 3xAIQ9UM2zA (30/09) | Keyword Planner demande un compte Google Ads et le modèle HubSpot un formulaire (identité) : remplacés par OpenRush research_keywords (gratuit, volumes par ville en Fran… |
| ✅ | Vidéo YouTube rVhitJk6KRU (12/10) : Claude Projects (Desktop, offres Pro/Max), tâches en parallèle, routines | Déjà en place : nos routines (points 2×/jour, contrôle global) ; HelloBro.ai (sponsor) non retenu. |
| ⏳ | Steve AI | à garder pour plus tard (vidéos « comment ça marche » après le 1er client), gratuité à vérifier |
| · | Envoi d'e-mails : sous-domaine dédié pour protéger le domaine principal, test de délivrabilité gratuit (SPF,… | À appliquer le jour où Dig aura son domaine et enverra des e-mails de prospection |
| · | e2EgglFl7MQ | Idée d'offre gardée de côté : publications mensuelles pour les artisans clients (à passer à la grille avant tout) |
| · | V8xsYJvbRpc (résumé : connaissances/shanehummus/V8xsYJvbRpc.md, Shane Hummus, envoyée le 07/10) | En pause : réseaux sociaux et vidéos jusqu'au premier client payant (décision du 05/10). Idée gardée pour ce jour-là : un chantier filmé par semaine, décliné en posts |
| · | golzvOVmXB4 (Coben, direct de 3 h 17 animé par Jean Philamand ; Gemini ne lisait pas la vidéo → transcription… | Hors piste (impression 3D), rien à construire. Deux astuces reprises : finir chaque prompt technique par « pose-moi tes questions avant de commencer et n'invente rien »… |
| · | vKat0aTuEbo | Décision parrainage |
| · | Envoyer un gros fichier à un client | Pair à pair, sans compte |
| · | Schémas, explications à un client | Croquis partagé en direct |
| · | Guide pas à pas pour un client | Captures annotées automatiques (« comment modifier vos horaires sur Google ») |
| ⛔ | 3iDiWTt8lok (résumé : videos-resumes/3iDiWTt8lok.md) | Déjà appliqué : outils/jev_trier_reponses.py (auto / Claude / humain selon la confiance). Ajouté : ShipWithJev.com à la veille quotidienne (799 cas d'usage, veille_sourc… |
| ⛔ | 5QMtCBkjvkY, JmNfV3GhVUU (gabzer) | Bibliothèque de pubs Meta (gratuite) utile pour voir ce que font les concurrents d'un prospect ; copier la pub d'un autre : écarté (contrefaçon) ; outils payants non ret… |

### Gestion, finance et administratif (4)

| État | Envoi / outil | Décision et usage |
|---|---|---|
| ✅ | e2JSCYig10g (YouTube, 30/09, Kasper) | Écarté : risque de perte d'argent, VPS payant (budget 0 €), 24 h de résultats ne prouvent rien. Deux principes repris, déjà en place : garde-fous écrits d'avance (chez n… |
| · | FOlebMS2MFA (résumé : connaissances/thenextbigshit/FOlebMS2MFA.md, The Next Big Shit, envoyée le 07/10) | Noté, pas lancé : autres métiers, hors priorité et hors budget. Règle n° 1 : demande à prouver avant toute construction. L'idée « adapter localement ce qui marche ailleu… |
| ⛔ | 5gifZmpc99g | Écarté : pas de publicité payante (budget 0 €) |
| ⛔ | Dépôt GitHub p-e-w/heretic (envoyé le 12/10, lien technologybrief ; jeton de suivi non conservé) | Écarté : aucun usage pour DIG16, budget 0 € (GPU), et un modèle sans garde-fous est un risque (contenus, réputation) ; rien installé. |

### Claude, agents et automatisation (21)

| État | Envoi / outil | Décision et usage |
|---|---|---|
| ✅ | Listes « meilleurs connecteurs, MCP, tools, tasks, hooks et dépôts GitHub gratuits pour Claude Code » envoyée… | fait le 03/10 |
| ✅ | Connecteurs Firecrawl et Similarweb | Branchés (Firecrawl utilisé le 01/10 pour lire les sources officielles) |
| ✅ | 5cb8pdJk0ZE (résumé : connaissances/juliangoldie/5cb8pdJk0ZE.md, Julian Goldie, envoyée le 07/10) | Déjà en place : garde-fous équivalents au mod « Blast Radius » (règles qui interdisent les commandes dangereuses, contrôle des secrets avant chaque commit, crochet de dé… |
| ✅ | eUfK8Eh9bTo (résumé : connaissances/calvinweischeslischt/eUfK8Eh9bTo.md, chaîne @calvinweischeslischt, envoyé… | Même sujet que 5cb8pdJk0ZE (déjà traitée) : garde-fous équivalents déjà en place, rien de plus utile au projet |
| ✅ | Claude Code, Gemini, MiniMax | Déjà en place (Claude Code, relais Gemini, guide MiniMax H3) |
| ✅ | Open Code, Cline | Inutiles : Claude Code fait déjà ce travail |
| ✅ | YuOSyRj3sXg | Déjà en place (.claude/CLAUDE.md + dossier) |
| ✅ | Vidéo YouTube gvESqM6s0kM (12/10) : 23 erreurs avec Claude 5.5 / Claude Code | Appliqué : CLAUDE.md fait 201 lignes → à alléger en renvoyant les détails vers des fichiers (à faire en douceur, sans perdre de règle) ; garde-fous déjà en place (pas de… |
| · | Tests de modèles d'IA (Gemini, GPT, Grok…) | Information générale, rien à appliquer |
| · | n8n (automatisation) | Version « Community » gratuite en auto-hébergement (docs.n8n.io, lu le 29/09 : « Without a license key, n8n runs as the free Community edition ») mais il faut un serveur… |
| · | IA en local (Ollama, LM Studio) | Pas de carte graphique ici ; Gemini gratuit via le relais suffit |
| · | x.com/huxlab (lien tronqué, retrouvé : message 2105145194756854053) | Culture générale sur les modèles, rien d'applicable directement à Dig. Leçon : les titres des republications sur X sont souvent faux → toujours identifier l'original. Ré… |
| · | 6W3E3ia-fK0 (EDteam, 40 min) | Noté, rien à construire. Notre base de connaissances est déjà en fichiers Markdown dans le dépôt, lisibles par Claude ; pas besoin d'un outil de plus. Résumé : videos-re… |
| · | A9E7gUrO5YQ, GgDhVLK6VbM | Gemini renvoie des réponses vides (2 essais chacun) ; même sujet que la vidéo ci-dessus : non repris, sauf si un besoin précis apparaît (alors vidIQ, 5 crédits chacun) |
| · | n8n, Obsidian, Google Meet | Inutiles pour l'instant : nos routines et le dépôt couvrent le besoin |
| · | MROM3p3CPZU | Méthode = notre règle n° 1 (demande prouvée) ; action n° 4 |
| · | Recherche avec sources citées | Recherche rapide ; tout chiffre reste revérifié à la source officielle |
| ⛔ | dHe2sHKvLFc (YouTube, 30/09) | Appliqué : le point automatique (routine) se déclenchait toutes les heures en relisant toute la conversation alors que sa consigne dit « toutes les 3 h » → recalé sur 34… |
| ⛔ | PLGnXz9_dTY | Écarté (trading, hors projet) |
| ⛔ | ucer2chlfM8 | Écarté (abonnement OpenAI payant) |
| ⛔ | Vidéo YouTube Tk5cgoGY1PU (12/10) : « deuxième cerveau » avec le greffon claude-obsidian (Obsidian + Claude C… | Pas installé : notre base connaissances/ + 46 + CLAUDE.md joue déjà ce rôle ; dépôt introuvable depuis le conteneur (accès GitHub limité à ce dépôt), donc impossible à l… |

### Divers (20)

| État | Envoi / outil | Décision et usage |
|---|---|---|
| ✅ | Veille du 01/10 (veille/2026-10-01.md) : 14 nouvelles vidéos Melvynx/Matt Wolfe (dont « Opus 5.5 remplace Aft… | trié le 01/10 |
| ✅ | HCZ3-Scx704 | Déjà appliqués pour l'essentiel ; rappel : phrases courtes et simples pour l'utilisateur |
| ✅ | is3XYKl2bpI | Appliqué : vérifier tout le contexte avant d'agir, effort adapté |
| · | Idée ou outil | Verdict |
| · | Vidéo ou source | Verdict |
| · | @melvynxdev : toute la chaîne (demande du 29/09) | Lecture complète lancée ; elle passe avant la suite de Finary (demande la plus récente). Environ 150 vidéos par jour avec le quota gratuit : 7 à 10 jours. Fiches : conna… |
| · | 12 vidéos YouTube | 2 déjà traitées (kYNwdRnb4ks, Uh9A_E4ik-0), 10 en cours de résumé |
| · | 2jZBhsLpe1o | Hors piste pour l'instant (visage et audience nécessaires) ; gardé de côté |
| · | s7QXxRvylrs, aBPAmYi1FfU | Information générale ; rien à appliquer (pas d'API payante) |
| · | Outil ou idée | Verdict |
| · | openalternative.co, OpenSourceAlternative.com (alternatives gratuites) | À ajouter à la veille si leur liste se lit automatiquement (réflexe « outil payant → équivalent gratuit ») |
| · | Quand | Pour quoi faire chez DIG16 |
| · | PDF : fusionner, compresser, signer, OCR | Formulaires administratifs (CFE 1447-C-SD), devis signés, PDF trop lourds pour le Drive |
| · | Nom disponible sur les réseaux | Réserver le même identifiant partout (a servi pour dig16fr) |
| · | Outil payant ou bloqué → équivalent gratuit | Réflexe du 28/09 : chercher l'équivalent gratuit et open source |
| · | Sécurité de contact@dig16.fr | Alerte si l'adresse fuit dans une base piratée |
| ⛔ | NotebookLM, Perplexity, Gamma | Utiles à l'utilisateur, rien à installer ici |
| ⛔ | LanguageTool | Installé le 01/10 : correcteur libre (LGPL) hors ligne, bibliothèques téléchargées depuis Maven Central avec empreintes vérifiées ; l'API publique en ligne est écartée c… |
| ⛔ | skOBL2Yc35I | Écarté : son « repost amélioré » est de la contrefaçon |
| ⛔ | Pictory | déjà écarté le 11/10 (payant, essai seulement) |

_213 entrées, registres : 46-apprentissage-continu.md, connaissances/technologybrief-sites.md._

<!-- catalogue-auto:fin -->

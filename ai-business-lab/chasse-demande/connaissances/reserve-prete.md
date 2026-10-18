# Réserve prête à l'emploi : tous les outils envoyés et gardés pour plus tard

Créée le 17/10/2026 à la demande de l'utilisateur : « je veux qu'ils soient prêts à être disponibles à la
moindre question ». Ce sont les outils **pas utiles aujourd'hui mais gardés**. Pour chacun : ce qu'il fait,
quand le ressortir, comment l'activer et ce qu'il coûte.

**Comment s'en servir :** à toute question ou tout nouveau besoin, chercher d'abord ici. Ce fichier est classé
par besoin. Ensuite, regarder le catalogue complet (`boite-a-outils.md`) et le résumé d'origine
(`videos-resumes/` ou `connaissances/`). Une gratuité marquée « à revérifier » doit être relue sur la page
officielle, et datée, le jour où l'outil sert. Avant d'installer quoi que ce soit, lire le code en entier.

Ne figurent pas ici les outils refusés par principe (piratage, contrefaçon, IA sans garde-fous, faux visages,
extraction de profils interdite). Ils sont marqués ⛔ dans `boite-a-outils.md`.

## Clients, suivi et vente

| Outil (envoi d'origine) | Sert à | Le ressortir quand… | Comment l'activer / coût |
|---|---|---|---|
| CRM « for agents » (carrousel Ddytkf2gBEj, 17/10) | Fichier clients tenu à jour par une IA (fiches, relances, suivi) | À partir de 3 à 5 clients, quand les tableaux privés ne suffisent plus | Dépôt GitHub open source, à installer après lecture ; gratuit (auto-hébergé) |
| Pin Feed (veille 16/10, free-for.dev) | Le client clique sur sa maquette en ligne pour laisser ses corrections | **Dès le 1er client**, pendant les allers-retours sur la maquette | Gratuit jusqu'à 3 projets, sans compte côté client (à revérifier le jour J) |
| Cal.com (carrousel DeekQtwk30w) | Lien de prise de rendez-vous en ligne | Quand les rendez-vous se multiplient | Gratuit, open source (à revérifier) ; équivalent libre de Calendly |
| Chatwoot (DeekQtwk30w) | Boîte unique des messages clients (site, Facebook, mail) | Si un client veut un chat sur son site | Open source, auto-hébergé |
| Agent `discovery-coach` (DeguteFBRO2, 17/10) | Préparer et débriefer un appel avec un artisan (questions, structure, objections) | **Installé le 17/10**, prêt : avant l'appel de Pauline et chaque entretien | `.claude/agents/discovery-coach.md` ; gratuit (MIT) |
| Autres agents « The Agency » : ventes, marketing, design (DeguteFBRO2) | Fiches d'experts prêtes à copier | Si une skill manque pour un besoin précis | Copier le fichier voulu depuis github.com/msitarzewski/agency-agents dans `.claude/agents/` après lecture ; gratuit (MIT) |
| Débriefing après appel (_To3N8UTh94) | L'utilisateur dicte ses notes, Claude dit quoi améliorer | **Dès les premiers appels**, déjà possible sans outil | Gratuit (Claude) |
| Retell AI (96G4KDnEFyI) | Standardiste téléphonique IA pour un client | Si un artisan demande qu'on réponde à ses appels | 10 $ offerts puis ~0,07 à 0,31 $/min (lu le 01/10) : option payante à refacturer |
| Google Forms (DeekQtwk30w) | Formulaires et questionnaires | Questionnaire client, sondage | Gratuit |
| Granola (DegsO8likZa, 17/10) | Notes de réunion transformées en résumés | Entretiens d'étude de marché ou rendez-vous clients en visio | Offre Basic gratuite annoncée (historique 30 jours, à revérifier) ; enregistrer seulement avec l'accord de la personne |

## Sites des clients (design, contenu, fonctions)

| Outil | Sert à | Le ressortir quand… | Comment l'activer / coût |
|---|---|---|---|
| Galeries d'inspiration : httpster.net, recent.design, dark.design, nicelydone.club, minimal.gallery, designspiration.com, ui.live, screensdesign.com (DeYzjEXgWa2) | Trouver une direction visuelle | Au 1er site client, avant la maquette | Gratuit (les 8 adresses répondaient le 15/10) |
| Google Stitch (MDZoiwPl2QU) | Maquette d'interface décrite en français | Si un client veut voir une maquette très vite | Gratuit (Google Labs, à revérifier) |
| Effets visuels : React Three Fiber, Liquidglass.js, Shader Gradient, Liquid Logo (DeMO5D0AUBq) ; img2threejs (Ddytkf2gBEj) | 3D, effets « verre », dégradés animés | Seulement sur une demande explicite d'un client « vitrine » (Prestige) ; ces effets alourdissent le site sur téléphone | Bibliothèques libres ; tester la vitesse (LCP) avant et après |
| Visuel IA « avant / après » (hRr-yUSM0_A) | Montrer une cuisine ou une salle de bain refaite | Client cuisiniste ou rénovation qui le demande | API payante : chercher d'abord un équivalent gratuit |
| Penpot (DegsO8likZa, 17/10) | Maquettes d'écrans partagées (alternative à Figma) | Client qui veut valider une maquette détaillée avant le site | Offre gratuite annoncée (à revérifier) ; en ligne, sans installation |
| Anydoc (Ddytkf2gBEj) | Convertir les documents du client (Word, Excel, PDF) en texte | **Installé le 17/10**, prêt | `python3 -c "import anydoc; print(anydoc.to_markdown('fichier'))"` ; gratuit (sans l'OCR « hosted », payant) |
| 10Web, Durable, Lovable… (Dde3xh9EYkM, reels du 29/09) | Sites générés par IA | Veille concurrence seulement : savoir ce que propose la concurrence | Payants ou concurrents directs |

## Vidéo, voix et contenus (en pause jusqu'au 1er client payant)

| Outil | Sert à | Le ressortir quand… | Comment l'activer / coût |
|---|---|---|---|
| OBS Studio (DegsO8likZa, 17/10) | Enregistrer l'écran (démo du site, tutoriel pour un client) | Tutoriel « comment modifier vos horaires » ou démo à distance | Logiciel libre et gratuit, à installer sur le PC de l'utilisateur |
| Editor de Diffusion Studio (Ddytkf2gBEj) | Montage vidéo piloté par un agent | Si un client commande des vidéos régulières | Open source, appli de bureau ; aujourd'hui : ffmpeg suffit |
| Skill `cbh991/animate`, méthode Canvas + Playwright + FFmpeg (rscb1DgJtNg) | Vidéos animées en code | Vidéo de démo ou de lancement | Gratuit, déjà dans le conteneur |
| Générateur vidéo de There's An AI For That, ArtPlayer (vqMhGnep1H0) | Clips de 8 s avec son | Petits visuels animés des démos | « 100 par jour » annoncé : quota et licence à revérifier le jour J |
| Google Vids, Flow, voix Gemini TTS (IWA9LCvNW8g) | Vidéos et voix gratuites | Vidéo de présentation d'un client | Offres gratuites à revérifier ; jamais de retrait de filigrane ni de VPN |
| Higgsfield + connecteur MCP (DekeJLyxVT9) | Montage et plans générés depuis Claude | Seulement si un client paie des vidéos et que le gratuit ne suffit pas | Payant (crédits à chaque génération, aide officielle lue le 16/10) |
| Fish Audio (1RqsrzT9-CI) | Voix clonée, pubs en plusieurs langues | Publicités multilingues | Clonage de la voix de l'utilisateur : son accord ; gratuité à vérifier |
| Riverside + méthode des clips (4aUVjc7ttko) | Découper un long enregistrement en clips verticaux | Si DIG16 fait un podcast ou des interviews | Riverside payant ; la méthode (30-50 s, couper les 2 premières secondes) est gratuite |
| Pictory, Steve AI, Zsky AI (@choly.ai) | Article transformé en vidéo | Si besoin de vidéos en volume | Pictory : essai seulement ; les autres à vérifier |
| Flick.art (O_4l1rPsWTM) | Films IA complets | Hors piste aujourd'hui | 300 crédits puis 100 par semaine (lu le 01/10) |
| Méthode « une vidéo par semaine déclinée en posts » (V8xsYJvbRpc) ; formats, accroches, « batching » (1hkTJ8wg9bY) | Stratégie de contenu | À la reprise des réseaux après le 1er client | Gratuit (méthode) |
| BandLab (DeCV78sETMT) | Musique de fond | Musique libre pour une vidéo | Gratuit (licence à vérifier) |
| Suno (Dde3xh9EYkM) | Musique générée | Idem | Offre gratuite à vérifier ; usage commercial souvent payant |

## Marketing et visibilité

| Outil | Sert à | Le ressortir quand… | Comment l'activer / coût |
|---|---|---|---|
| Pomelli de Google Labs (Dde3xh9EYkM) | Analyse un site et propose des idées de campagne avec visuels | Campagne de publicité DIG16 ou client | Gratuit (Labs, à revérifier) |
| Bibliothèque de publicités Meta (gabzer) | Voir les pubs des concurrents d'un prospect | Avant de proposer une pub à un client | Gratuit ; s'en inspirer, ne jamais copier |
| Variantes de publicités à tester (1RqsrzT9-CI) | Plusieurs versions d'une même pub | Première publicité payante | Méthode gratuite |
| ViralityAI (DeMr4aFiCvy) | Idées de contenus et tendances | Reprise des réseaux | Gratuité non précisée |
| Mixpost, Shoutrrr (Dd2tZCCDofx) | Secours de Metricool pour programmer les publications | Si Metricool devient payant ou tombe en panne | Libres (MIT, Apache 2.0) ; noté dans `63` § 4 |

## Administratif, données d'entreprises, sécurité

| Outil | Sert à | Le ressortir quand… | Comment l'activer / coût |
|---|---|---|---|
| Jsonpage (veille 14/10) | Données d'entreprises françaises (SIREN, SIRET, TVA) | Si `verif_entreprises.py` ou l'annuaire officiel tombe | 1 000 requêtes/jour gratuites sans carte (annoncé, à revérifier) |
| OpenRegistry (veille 11/10) | Registres officiels de 80 pays | Secours de la vérification d'un client | À vérifier |
| MailSenpai DNS Check (veille 15/10) | Vérifie SPF, DKIM et DMARC | **Le 21/10**, après l'activation de DKIM | Gratuit, sans clé |
| Brevo (veille 11/10) | Envoi de mails automatiques | Si FormSubmit ou les envois saturent | Offre gratuite à revérifier |
| VirusTotal (DeCV78sETMT) | Vérifier un fichier ou un lien suspect | Un client envoie une pièce jointe douteuse | Gratuit |
| Temp-Mail (DeCV78sETMT) | Adresse jetable pour tester un formulaire | Tests du site | Gratuit |
| Open-kritt (Ddytkf2gBEj) | Recherche de failles par des agents | Si un client a un site avec comptes ou paiements | Open source, auto-hébergé ; aujourd'hui CodeQL suffit |
| Bitwarden (DeekQtwk30w) | Coffre-fort de mots de passe (comptes clients) | **Dès 2 ou 3 clients** (comptes Cloudflare, domaines) | Gratuit pour un utilisateur (à revérifier) |
| Obsidian (DegsO8likZa, 17/10) | Notes personnelles reliées, gardées sur l'appareil | Si l'utilisateur veut un carnet de notes hors ligne | Gratuit en local (Sync payant, inutile) |
| Nextcloud, Baserow, Vikunja, PostHog, n8n (DeekQtwk30w, revus dans DegsO8likZa) | Fichiers, tableaux, tâches, statistiques, automatisations | Si un service gratuit actuel devient payant | Libres, auto-hébergés |

## Claude, agents et automatisation

| Outil | Sert à | Le ressortir quand… | Comment l'activer / coût |
|---|---|---|---|
| Openworker (Ddytkf2gBEj) | Assistant IA sur ordinateur (fichiers, applis) | Si l'utilisateur veut un assistant installé sur son PC Windows | Appli libre (Mac, Windows) |
| Graft (Ddytkf2gBEj), HydraDB (Ddytkf2gBEj), PageIndex, Hindsight, Orca, Magpie, Brigade, IFixAi, fframes (DeGDWLNDm86) | Outils de développeurs pour agents (gros code, mémoire, plusieurs agents) | Si les outils DIG16 deviennent gros, ou pour chercher dans de très longs documents (PageIndex) | Open source |
| Paperclip (7RVf25Rg0Mc, DeGDWLNDm86) | Équipe d'agents organisée en entreprise | Si l'activité exige des agents permanents | Serveur allumé en permanence (coût) |
| Mods de Claude Code : Reflect, Blast Radius, Cache Tax… (xvy40dHyAmw, lDrAZ1wAyVs) | Extensions de l'interface | Si l'utilisateur travaille sur ordinateur avec Claude Code | Gratuits ; l'idée de Reflect est déjà appliquée (`ameliorer_systeme.py`) |
| UI UX Pro Max, agent-skills d'Addy Osmani (« Top 10 skill repos ») | Skills de design et de développement | UI UX Pro Max : déjà installé depuis ; agent-skills : sur besoin | MIT |
| ArtCraft (Fuo1i_-9Frc) | Suite type Adobe libre, pilotable par agent | Quand PhotoCraft sera stable (« alpha » le 09/10) | Libre (MIT ou Apache-2.0 d'après les articles) |
| Poe, NotebookLM, Perplexity, Gamma, Elicit, Consensus, Wolfram Alpha | Outils d'IA à utiliser soi-même | L'utilisateur peut s'en servir directement | Gratuits ou en partie gratuits |
| DownSub (DeCV78sETMT) | Sous-titres d'une vidéo YouTube en texte | Secours si Gemini et vidIQ ne lisent pas une vidéo | Gratuit |
| Excalidraw (DeekQtwk30w) | Schémas faits à la main | Expliquer une offre en rendez-vous | Gratuit (connecteur disponible) |
| Obsidian (DeekQtwk30w, Tk5cgoGY1PU) | Notes en « second cerveau » | Si l'utilisateur veut ses notes hors de Claude | Gratuit |

## Pistes de revenus gardées (sans construction)

| Piste | Source | Statut |
|---|---|---|
| Racheter de petits logiciels sous-exploités | 7XTYaVrt4QM | Idée notée, chiffres de l'auteur non vérifiés |
| Chaînes vidéo « sans visage » | x.com/chesny | Écartée pour l'instant : outils payants et règles YouTube vérifiées |
| Standardiste IA pour artisans | 96G4KDnEFyI | Option à proposer si un client le demande |
| Visuels avant/après pour cuisinistes | hRr-yUSM0_A | Option future |

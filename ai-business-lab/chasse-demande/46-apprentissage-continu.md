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
| 1 | Lire puis installer, s'ils sont sûrs, les skills **Impeccable** (contrôle visuel des marges, alignements, couleurs) et **vibe-security** (failles de sécurité) | LCwT00LrPZg, _SVU3oC4JX8 | en cours |
| 2 | Tester le skill `motion-graphics` pour une vidéo de lancement de Dig (après relecture du dépôt) | 6Ij9-f2T2Ck | à faire |
| 3 | Contrôle qualité : toute animation vérifiée à 0, 25, 50, 75 et 100 % de sa durée | HOXrLsVqinY | **fait** (ligne déjà présente dans `44-controle-qualite.md`) |
| 4 | Chercher avec vidIQ les questions les plus demandées sur les sites d'artisans (vidéos « outliers ») : preuve de demande, idées de contenus | MROM3p3CPZU | à faire |
| 5 | Ressources gratuites de design (polices Fontshare, icônes, composants) pour les démos | _SVU3oC4JX8 | à évaluer |
| 6 | Page d'arrivée alignée mot pour mot sur le message de prospection | oBw_BDIZIqc | à appliquer aux prochains messages |

## Décisions qui appartiennent à l'utilisateur

| Sujet | Source | Question |
|---|---|---|
| **Parrainage client** (ex. un mois offert par artisan recommandé) | vKat0aTuEbo | Quelle récompense ? (engage les prix) |
| Connecteurs **Firecrawl** et **Similarweb** | HOXrLsVqinY, inventaire du 28/09 | À brancher sur claude.ai (voir `33-outils.md`) |

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

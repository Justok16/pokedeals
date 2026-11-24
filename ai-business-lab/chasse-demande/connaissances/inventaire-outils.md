# Inventaire des outils DIG16 (tenu à jour automatiquement)

Fichier régénéré par `outils/veille_outils.py` à chaque veille, depuis `inventaire-outils.json` (demande de l'utilisateur du 28/10 : garder tous les outils fiables à portée et à jour). Statut : **en place** (utilisé), **installé** (prêt dans Claude), **réserve** (vérifié, à sortir au bon moment, voir `reserve-prete.md`).

| Domaine | Outil | Statut | Usage | Version (date) | Licence | Étoiles |
|---|---|---|---|---|---|---|
| Animation (Prestige) | Skill horizontal-scroll-scenes | installé | Chapitres qui défilent de gauche à droite pendant le défilement vertical, état dérivé du scroll, accessible et sans mouvement réduit ; MIT, lu en entier et installé le 04/11/2026 (.claude/skills/horizontal-scroll-scenes) | — | — | — |
| Animation (Prestige) | Skill threejs-animation | installé | Compagnon de threejs-web : animations Three.js indépendantes du nombre d'images, liées au défilement, mouvement réduit ; MIT, lu en entier et installé le 04/11/2026 | — | — | — |
| Animations | GSAP | en place | Moteur d'animation des sites (site-dig/moteur/anim/gsap-3.15.0.min.js et ScrollTrigger, mis à jour le 28/10) | 3.15.1 (2026-11-04) | Standard 'no charge' license: https://gsap.com/standard-license. | 31157 |
| Animations | GSAP Skills officiels | installé | .claude/skills/gsap-* (core, timeline, scrolltrigger, plugins, utils, performance) | — | MIT | 18471 |
| Animations | Lenis | en place | Défilement fluide (site-dig/moteur/anim/lenis-1.3.27.min.js, mis à jour le 28/10) | 1.3.28 (2026-11-23) | MIT | 17296 |
| Animations | Motion | réserve | Micro-interactions légères | 14.14.0 (2026-11-13) | MIT | — |
| Animations | Three.js | réserve | 3D légère pour un client Prestige | 0.187.0 (2026-10-30) | MIT | 118786 |
| Animations | dotLottie web | réserve | Icônes animées vectorielles | 0.83.2 (2026-11-12) | MIT | 953 |
| Animations | swup | réserve | Transitions entre pages d'un site statique | 4.10.0 (2026-09-03) | MIT | 5253 |
| Clients et administratif | Documents client (documents_client.py) | en place | Devis, CGV, facture, questionnaire, accord gracieux | — | — | — |
| Clients et administratif | Kit client complet (kit_client.py) | en place | 12 documents d'un nouveau client en une commande (devis, CGV, facture, PV, mode d'emploi…), 72 | — | — | — |
| Clients et administratif | Remplir un PDF (remplir_pdf.py) | en place | Cerfa et formulaires remplis automatiquement | — | — | — |
| Clients et administratif | Vérification d'entreprise (verif_entreprises.py + connecteur Contract-Factory SIREN) | en place | SIREN, état, BODACC avant signature (45) | — | — | — |
| Communication et organisation | Gmail + Google Drive + Google Agenda (connecteurs) | en place | Courrier DIG16, archives privées « Dig », rendez-vous | — | — | — |
| Design | Anthropic skills | installé | frontend-design et skills officiels | — | — | 194524 |
| Design | Emil Kowalski skills | installé | emil-design-eng, mobile-native, review-animations, break-ui | — | MIT | 56835 |
| Design | Fontsource | réserve | Polices libres à héberger | 5.3.0 (2026-07-19) | MIT | 6285 |
| Design | Impeccable | installé | Skill impeccable | — | Apache-2.0 | 110111 |
| Design | Leonardo (Adobe) | réserve | Palettes à contraste garanti | 1.1.0 (2026-02-18) | Apache-2.0 | 2188 |
| Design | Open Props | réserve | Variables CSS prêtes | 1.7.23 (2026-01-31) | MIT | — |
| Design | Taste skill | installé | taste-design, taste-redesign | — | MIT | 115918 |
| Design | UI UX Pro Max | installé | Skill ui-ux-pro-max (attention : liens Google Fonts, contrôle polices_locales) | — | MIT | 150022 |
| Design | awesome-design-md | installé | Skill design-md-references | — | MIT | 127661 |
| Design | google-webfonts-helper | réserve | Télécharger une police Google pour l'héberger | — | MIT | 13083 |
| Design | unslop (skill Claude Code, heydamir/unslop) | installé | Contrôle anti-aspect-IA des démos et sites avant de les montrer ; scripts snapshot/story seulement si Playwright est présent ; aucune vidéo publiée sans accord (crédit @heydamir incrusté) | — | — | — |
| Facturation et paiement | GoCardless (prélèvement SEPA) | en place | Mandats SEPA des formules mensuelles | — | — | — |
| Facturation et paiement | Indy (facturation, plateforme agréée, compte pro) | en place | Factures, facturation électronique, livre des recettes | — | — | — |
| Hébergement et sécurité | Cloudflare Pages + Web Analytics + Turnstile | en place | Hébergement, mesure sans cookie, anti-robots | — | — | — |
| Marketing | Humanizer | installé | Retirer les tics d'écriture d'IA | — | MIT | 69506 |
| Marketing | marketingskills | installé | copywriting, seo-audit, schema, ai-seo… | — | MIT | 60609 |
| Photos | LightCraft (ArtCraft) | réserve | Retouche de séries de photos | — | — | — |
| Photos | PhotoCraft (ArtCraft) | réserve | Retouche type Photoshop, pilotable par Claude | — | Apache-2.0 | 79871 |
| Photos | SVGO | réserve | Alléger les logos SVG | 4.1.0 (2026-08-24) | MIT | 22606 |
| Photos | eleventy-img | réserve | Balises <picture> complètes | 7.1.1 (2026-10-21) | MIT | 469 |
| Photos | rembg | réserve | Détourage local | 2.0.87 (2026-11-06) | MIT | 25460 |
| Photos | sharp | réserve | WebP/AVIF et tailles multiples | 0.35.5 (2026-09-27) | Apache-2.0 | 32858 |
| Photos | sharp-cli | réserve | sharp en ligne de commande | 6.1.0 (2026-09-01) | MIT | 229 |
| Prospection | Fiche d'appel prospect (outils/prospects/fiche_appel.py) | en place | Fiche d'appel revérifiée en direct | — | — | — |
| Prospection | Trouver un contact (trouver_contact.py) | en place | Pages contact d'un organisme | — | — | — |
| Publicité | Google Ads MCP | réserve | Lecture des campagnes Google Ads | — | Apache-2.0 | 1180 |
| Qualité | Chrome DevTools MCP | réserve | Performance réelle, console, réseau | 1.13.0 (2026-11-11) | Apache-2.0 | 55268 |
| Qualité | Context7 | réserve | Documentation à jour des bibliothèques | 4.7.3 (2026-11-17) | MIT | 64883 |
| Qualité | Contrôle global du site (controle_global.py, test_pages.py, seo_client.py, test_formulaire.py) | en place | Santé du site et des sites clients avant livraison | — | — | — |
| Qualité | Linkinator | installé | Liens cassés d'un site entier (outils/liens/verifier.sh) ; MIT, 8.1.0 vérifiée le 03/11/2026 | 8.1.0 (2026-08-29) | MIT | — |
| Qualité | Playwright MCP | en place | Navigateur piloté (.mcp.json) | 0.0.86 (2026-11-18) | Apache-2.0 | 39659 |
| Qualité | Traces d'un autre client (traces_autre_client.py) | en place | Aucune trace d'un autre client dans un site livré | — | — | — |
| Qualité | Unlighthouse | installé | Audit vitesse, accessibilité, bonnes pratiques et référencement de toutes les pages (outils/unlighthouse/audit.sh) ; MIT, 0.19.1 vérifiée le 03/11/2026 | 0.20.0 (2026-11-20) | MIT | — |
| Qualité | axe-core | réserve | Moteur d'accessibilité | 4.14.1 (2026-11-16) | non-standard | 7818 |
| Qualité | html-validate | réserve | Validation HTML | 11.21.1 (2026-11-12) | MIT | — |
| Qualité | lychee | réserve | Liens cassés | — | Apache-2.0 | 4141 |
| Qualité | pa11y | réserve | Accessibilité en une commande | 10.0.0 (2026-08-28) | LGPL-3.0 | 4602 |
| Qualité des documents | Contrôle qualité des documents (orthographe.py, typo_fr.py, lisibilite.py, pdf_pages.py) | en place | Contrôle 44 avant tout envoi | — | — | — |
| Réseaux sociaux | Metricool (connecteur) | en place | Programmation et statistiques des réseaux | — | — | — |
| Réseaux sociaux | Zapier / Buffer (connecteur) | en place | Stories et Shorts quand Metricool est plein | — | — | — |
| Réseaux sociaux | vidIQ (connecteur) | en place | YouTube : vidéos, transcriptions | — | — | — |
| SEO | Claude SEO | réserve | Audit SEO complet (MIT) | — | — | — |
| SEO | Google Analytics MCP | réserve | GA4 d'un client | — | Apache-2.0 | 3793 |
| SEO | Lighthouse | en place | Audit performance, SEO, accessibilité | 13.6.0 (2026-10-27) | Apache-2.0 | 31083 |
| SEO | OpenSEO (connecteur) | en place | Fiche Google, Search Console, audits | — | — | — |
| SEO | Unlighthouse | réserve | Lighthouse sur tout un site | 0.20.0 (2026-11-20) | MIT | — |
| SEO | critical | réserve | CSS du premier écran | 9.0.0 (2026-09-13) | Apache-2.0 | 10305 |
| SEO | mcp-gsc | réserve | Search Console dans Claude | — | MIT | 2195 |
| Signature électronique | Modèles DocuSeal (modeles_docuseal.py + connecteur DocuSeal) | en place | 4 modèles prêts (6628706 à 6628709), envoi send_documents | — | — | — |
| Sécurité | ALTCHA | réserve | Anti-spam sans tiers | 3.7.0 (2026-11-20) | MIT | 2917 |
| Sécurité | Gitleaks | réserve | Secrets oubliés dans le dépôt | v8.30.1 (2026-02-21) | MIT | 31050 |
| Sécurité | OSV-Scanner | réserve | Dépendances vulnérables | v2.7.1 (2026-11-09) | Apache-2.0 | 11517 |
| Sécurité | Semgrep | réserve | Analyse du code serveur | 1.186.0 (2026-11-18) | LGPL-2.1 | 17761 |
| Sécurité | security-guidance (Anthropic) | réserve | Extension officielle ; revues IA à chaque fin de tour et commit = gros quota | — | Apache-2.0 | 47399 |
| Sécurité | tarteaucitron.js | réserve | Bandeau cookies CNIL | 1.37.0 (2026-10-15) | MIT | 1059 |
| Veille | Réserve à proposer (reserve_a_proposer.py) | en place | Ressort l'outil gardé au bon moment | — | — | — |
| Veille | Veille presse (veille_presse.py) et veille des sources (veille_sources.py) | en place | Presse locale, chaînes, annuaires d'outils | — | — | — |
| Vidéo | Hyperframes | réserve | Vidéo depuis HTML/GSAP | — | Apache-2.0 | 83272 |
| Vidéo | OpenMontage | réserve | Montage par agent (AGPL-3.0) | — | AGPL-3.0 | 81000 |
| Vidéo | Remotion | réserve | Vidéos en code (gratuit tant que DIG16 ≤ 3 personnes, livraison MP4 seule) | 4.0.546 (2026-11-23) | non-standard | 73903 |
| Vidéo | Remotion Agent Skills | réserve | npx skills add remotion-dev/skills | — | — | 7286 |
| Vidéo | Revideo | réserve | Vidéos en code, MIT | 0.11.0 (2026-07-10) | MIT | — |
| Vidéo | auto-editor | réserve | Couper les silences | 29.3.1 (2025-11-04) | non-standard | 5995 |
| Vidéo | faster-whisper | en place | Transcription et sous-titres locaux | 1.2.1 (2025-10-31) | MIT | 26875 |

Dernière veille : 2026-11-24.

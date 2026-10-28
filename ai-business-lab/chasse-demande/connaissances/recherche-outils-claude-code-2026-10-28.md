# Recherche : meilleurs outils gratuits pour Claude Code (28/10/2026)

Faite par Claude à partir du prompt `supports/prompt-ia-outils-claude-code.md` (l'utilisateur l'a collé ici le 28/10).

## Méthode de vérification
Toutes les vérifications ont été faites le 28/10/2026.
- **Étoiles et licence GitHub** : API publique deps.dev (Google).
- **Dernière version** : registres officiels npm, PyPI et proxy Go.
- **Pages de prix et de licences** : extraites par Tavily ou lues directement (curl), citées entre guillemets.

Limites :
- Tavily a bloqué les requêtes (trop nombreuses) en fin de recherche.
- Quelques points restent donc « à vérifier », et c'est écrit.
- Rien n'a été installé : chaque outil sera lu en entier avant installation (règle `CLAUDE.md`).

Légende de la colonne « Vérifié » :
- **oui** : page ou dépôt ouvert aujourd'hui.
- **partiel** : existence et licence vérifiées, mais un détail (étoiles, date) n'a pas pu être lu.
- **à vérifier** : rien de sûr.

---

## 1. Design de sites d'exception

| Nom | Lien officiel | Apport pour un site d'artisan | Type | Gratuité | Licence | Mise à jour / étoiles | Installation | Risques | Vérifié |
|---|---|---|---|---|---|---|---|---|---|
| Utopia (échelles fluides) | https://utopia.fyi/ | Titres et espacements qui s'adaptent sans à-coups du téléphone au grand écran : rendu « haut de gamme » | Outil web (génère du CSS) | « There's no program or dependency to install, although we are developing some free tools » | — | Site actif | Aucune : Claude écrit les variables `clamp()` | Aucun | oui |
| Fontsource | https://github.com/fontsource/fontsource | Polices libres **hébergées sur le site** (fin de Google Fonts), versions variables | Bibliothèque npm | Libre | MIT (outil) ; chaque police a sa licence (souvent OFL) | `@fontsource-variable/inter` 5.3.0 (19/07/2026) ; ★6 228 | `npm i @fontsource-variable/<police>` | Vérifier la licence de chaque police | oui |
| google-webfonts-helper | https://github.com/majodev/google-webfonts-helper | Télécharger une police Google en WOFF2 pour l'héberger soi-même (RGPD) | Outil web / dépôt | Libre | MIT | ★13 070 | Aucune (site web) | Peu actif : à vérifier | partiel |
| Leonardo (Adobe) | https://github.com/adobe/leonardo | Palette tirée du logo du client avec des contrastes lisibles garantis (accessibilité) | Bibliothèque npm | Libre | Apache-2.0 | 1.1.0 (18/02/2026) ; ★2 161 | `npm i @adobe/leonardo-contrast-colors` | Aucun | oui |
| Open Props | https://open-props.style/ | Jeu de variables CSS prêtes (ombres, dégradés, courbes) cohérentes | Bibliothèque CSS | Libre | MIT (à vérifier sur le dépôt) | 1.7.23 (31/01/2026) ; étoiles à vérifier | `npm i open-props` | Aucun | partiel |
| Fontshare (Indian Type Foundry) | https://www.fontshare.com/ | 100 polices de caractère (Satoshi, Clash Display…) | Banque de polices | Licence « ITF Free Font License » | ITF FFL : **page non lisible aujourd'hui** | — | Téléchargement manuel | Usage commercial à confirmer sur la licence | à vérifier |

## 2. Photos et images

| Nom | Lien | Apport | Type | Gratuité | Licence | Mise à jour / étoiles | Installation | Risques | Vérifié |
|---|---|---|---|---|---|---|---|---|---|
| sharp | https://github.com/lovell/sharp | Conversion automatique en WebP/AVIF, tailles multiples pour images responsives, très rapide | Bibliothèque Node | Libre | Apache-2.0 | 0.35.5 (27/09/2026) ; ★32 786 | `npm i sharp` | Aucun | oui |
| Pexels (photos et vidéos) | https://www.pexels.com/license/ | Photos et vidéos de qualité en complément des photos du client | Banque + API | « All photos and videos on Pexels can be downloaded and used for free. Attribution is not required » | Licence Pexels | — | API gratuite avec clé (variable d'environnement) | « Identifiable people may not appear in a bad light » ; interdit de revendre la photo telle quelle | oui |
| Pixabay (photos, vidéos, **musiques, bruitages**) | https://pixabay.com/service/license-summary/ | Images et sons libres pour sites et vidéos | Banque + API | Usage gratuit, attribution non requise | Pixabay Content License | — | API gratuite avec clé | Interdit : revente telle quelle, usage commercial de contenus montrant des marques ou logos | oui |
| rembg | https://github.com/danielgatis/rembg | Détourage automatique (photo d'un produit ou d'un artisan sur fond propre), sur la machine | CLI / Python | Libre | MIT | 2.0.86 (21/10/2026) ; ★25 144 | `pip install "rembg[cli]"` | Télécharge un modèle d'IA au premier usage | oui |
| @11ty/eleventy-img | https://github.com/11ty/eleventy-img | Génère le `<picture>` complet (AVIF, WebP, JPEG, largeurs multiples) | Bibliothèque Node | Libre | Licence non lue (à vérifier) | 7.1.1 (21/10/2026) ; ★470 | `npm i @11ty/eleventy-img` | Aucun | partiel |
| Upscayl | https://github.com/upscayl/upscayl | Agrandir une photo trop petite fournie par l'artisan | Appli de bureau | Libre | AGPL-3.0 | ★50 938 | Sur ordinateur (pas dans Claude Code) | Lourd (carte graphique) | partiel |
| Déjà chez nous | Unsplash (connecteur), suite ArtCraft (LightCraft) | | | | | | | | |

## 3. Animations

| Nom | Lien | Apport | Type | Gratuité | Licence | Mise à jour / étoiles | Installation | Risques | Vérifié |
|---|---|---|---|---|---|---|---|---|---|
| **GSAP Skills (officiel GreenSock)** | https://github.com/greensock/gsap-skills | Apprend à Claude le bon usage de GSAP : timelines, ScrollTrigger, plugins, **performance** ; c'est exactement notre moteur | Skills + plugin Claude Code | « GSAP is 100% free — including every plugin » | MIT | ★16 850 | `/plugin marketplace add greensock/gsap-skills` | Copie non officielle repérée : `takoukam/gsap-skills-claude` (ne pas utiliser) | oui |
| GSAP (licence) | https://gsap.com/standard-license/ | SplitText, MorphSVG, etc. désormais gratuits | Bibliothèque | « Can I really use GSAP in commercial projects without paying anything? Yes, really! » | Licence « Standard No Charge » (Webflow) | 3.15.0 (13/04/2026) ; ★29 802 | Déjà installé (`/moteur/`) | Interdit seulement dans un outil concurrent de Webflow (constructeur visuel d'animations) : pas notre cas | oui |
| Lenis | https://github.com/darkroomengineering/lenis | Défilement fluide (déjà utilisé) | Bibliothèque | Libre | MIT | 1.3.27 (15/10/2026) ; ★16 809 | Déjà installé | — | oui |
| swup | https://github.com/swup/swup | Transitions animées entre pages d'un site statique, sans framework | Bibliothèque | Libre | MIT | 4.10.0 (03/09/2026) ; ★5 248 | `npm i swup` | Aucun | oui |
| View Transitions API (navigateur) | https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API | Transitions entre pages en CSS natif, sans bibliothèque | Fonction du navigateur | Gratuit | — | — | Rien à installer | Prise en charge selon le navigateur (prévoir sans effet) | à vérifier (page non rouverte aujourd'hui) |
| Motion (motion.dev) | https://github.com/motiondivision/motion | Micro-interactions légères en JavaScript simple | Bibliothèque | Libre | Licence (LICENSE.md) à lire | 14.7.1 (27/10/2026) ; ★33,8 k | `npm i motion` | Doublon partiel de GSAP | partiel |
| Three.js | https://github.com/mrdoob/three.js | 3D légère (logo en relief, objet du métier) pour un client Prestige | Bibliothèque | Libre | MIT | 0.186.1 (24/09/2026) ; ★116 492 | `npm i three` | Poids : à charger seulement si utile | oui |
| dotLottie web | https://github.com/LottieFiles/dotlottie-web | Petites animations vectorielles (icônes animées) | Bibliothèque | Libre | MIT | 0.81.0 (06/10/2026) ; ★928 | `npm i @lottiefiles/dotlottie-web` | Licence de chaque animation téléchargée à vérifier | oui |

## 4. Vidéos de haute volée

| Nom | Lien | Apport | Type | Gratuité | Licence | Mise à jour / étoiles | Installation | Risques | Vérifié |
|---|---|---|---|---|---|---|---|---|---|
| **Remotion + Remotion Agent Skills** | https://www.remotion.dev/license ; https://www.remotion.dev/docs/ai/skills | Vidéos de présentation de sites, Shorts, sous-titres, rendus en MP4 par Claude | Bibliothèque + skills officiels | « You are eligible to use Remotion for free if you are: an individual · a for-profit organization with up to 3 employees » | Licence Remotion (gratuite jusqu'à 3 salariés) | 4.0.539 (26/10/2026) ; ★66 749 ; skills ★5 531 | `npx skills add remotion-dev/skills` | Devient payant au-delà de 3 salariés | oui |
| Revideo | https://github.com/redotvideo/revideo | Équivalent libre de Remotion (vidéos en code) | Bibliothèque | Libre | MIT | 0.11.0 (10/07/2026) ; ★4,1 k | `npm i @revideo/core` | Communauté plus petite | oui |
| faster-whisper | https://github.com/SYSTRAN/faster-whisper | Sous-titres automatiques en français, sur la machine (déjà utilisé) | Bibliothèque Python | Libre | MIT | 1.2.1 (31/10/2025) ; ★26 119 | Déjà installé | Dernière version il y a 12 mois, mais reste la référence | oui |
| auto-editor | https://github.com/WyattBlue/auto-editor | Coupe automatiquement les silences d'une vidéo filmée | CLI | Libre | Unlicense | 29.3.1 (04/11/2025) ; ★5 610 | `pip install auto-editor` | Aucun | oui |
| Freesound (bruitages) | https://freesound.org/help/faq/ | Bruitages par milliers | Banque de sons | Gratuit | CC0, CC-BY ou **CC-BY-NC** selon le son | — | Téléchargement / API avec clé | « Some sounds you cannot use commercially » : ne prendre que CC0 ou CC-BY (créditer) | oui |
| Mixkit (musiques, bruitages) | https://mixkit.co/license/ | Musiques et bruitages | Banque | « Stock Music Free License », « Sound Effects Free License » | Licences Mixkit | — | Téléchargement manuel | Texte exact de chaque licence non lu (fenêtre dynamique) | à vérifier |
| Déjà chez nous | Hyperframes (★73 742, Apache-2.0), OpenMontage, Huashu Motion (réserve) | | | | | | | | |

## 5. Marketing

| Nom | Lien | Apport | Type | Gratuité | Licence | Mise à jour / étoiles | Installation | Risques | Vérifié |
|---|---|---|---|---|---|---|---|---|---|
| Brevo (offre gratuite) | https://www.brevo.com/pricing/ | Emailing B2B (relances, lettre d'information) depuis un vrai service d'envoi | Service + API | « Free forever, no credit card needed » ; « up to 300 emails per day » | Service | — | API avec clé | Données des contacts chez un tiers (registre RGPD) ; règles CNIL de `35` | oui |
| Postiz | https://github.com/gitroomhq/postiz-app | Programmation des réseaux (alternative libre à Metricool) | Appli à héberger | Libre | AGPL-3.0 | ★37 554 | À héberger soi-même (serveur) | Hébergement non gratuit en pratique ; Metricool suffit | partiel |
| listmonk | https://github.com/knadh/listmonk | Gestion de lettres d'information auto-hébergée | Appli à héberger | Libre | AGPL-3.0 | ★24 000 | Serveur requis | Idem | partiel |
| Déjà chez nous | coreyhaines31/marketingskills, série `ig-*`, cold-email, content-engine, Metricool | | | | | | | | |

## 6. Référencement (SEO)

| Nom | Lien | Apport | Type | Gratuité | Licence | Mise à jour / étoiles | Installation | Risques | Vérifié |
|---|---|---|---|---|---|---|---|---|---|
| **Claude SEO** | https://github.com/AgriciDaniel/claude-seo | Audit SEO complet en 10 à 15 min (26 sous-skills), plan d'action, visibilité IA | Plugin Claude Code | « Yes. MIT licensed, fully open source, no per-domain pricing, no telemetry » | MIT | Étoiles à vérifier | `/plugin marketplace add AgriciDaniel/claude-seo` | Installe son propre environnement Python et un navigateur ; recoupe nos skills `seo-*` | oui |
| Unlighthouse | https://github.com/harlan-zw/unlighthouse | Lighthouse sur **toutes** les pages d'un site d'un coup (Core Web Vitals) | CLI | Libre | Licence (LICENSE.md) à lire | 0.19.1 (03/10/2026) ; ★4,9 k | `npx unlighthouse --site https://…` | Aucun | partiel |
| Lighthouse | https://github.com/GoogleChrome/lighthouse | Audit performance, accessibilité, SEO page par page | CLI | Libre | Apache-2.0 | 13.6.0 (27/10/2026) ; ★30 922 | `npx lighthouse <url>` | Aucun | oui |
| PageSpeed Insights API | https://developers.google.com/speed/docs/insights/v5/get-started | Mesure Google officielle, scriptable | API | « can be used with or without an API key » | Service Google | — | curl | Données réelles annoncées « soon to be discontinued » | oui |
| IndexNow | https://www.indexnow.org/documentation | Prévenir Bing et Yandex à chaque mise à jour (déjà utilisé) | API | Gratuit ; « up to 10,000 URLs per post » | Protocole ouvert | — | Déjà en place | — | oui |
| mcp-gsc (Search Console) | https://github.com/AminForou/mcp-gsc | Claude lit les données Search Console (requêtes, clics, indexation) | MCP | Libre | MIT | ★1 994 | Suivre le README (identifiants Google) | Accès au compte Google du client : uniquement avec son accord | partiel |
| Google Analytics MCP (officiel) | https://github.com/googleanalytics/google-analytics-mcp | Lire les statistiques GA4 d'un client | MCP | Libre | Apache-2.0 | ★3 532 | Suivre le README | Inutile si on reste sur Cloudflare Web Analytics (sans cookies) | partiel |
| Déjà chez nous | seo, seo-audit, seo-local, ai-seo, schema, OpenSEO | | | | | | | | |

## 7. Sécurité et RGPD

| Nom | Lien | Apport | Type | Gratuité | Licence | Mise à jour / étoiles | Installation | Risques | Vérifié |
|---|---|---|---|---|---|---|---|---|---|
| **tarteaucitron.js** | https://github.com/AmauriC/tarteaucitron.js | Bandeau cookies **français**, conforme CNIL, Consent Mode v2 | Bibliothèque | Libre | MIT | 1.37.0 (15/10/2026) ; ★1 059 | `npm i tarteaucitronjs` (ou fichiers hébergés) | Aucun ; inutile si le site n'a aucun traceur | oui |
| Cloudflare Turnstile | https://www.cloudflare.com/application-services/products/turnstile/ | Formulaires protégés contre les robots, sans CAPTCHA pénible | Service | « a simple snippet of free code that eliminates CAPTCHAs » | Service | — | Clé de site Cloudflare | Script tiers Cloudflare (mention dans la politique de confidentialité) | oui |
| Gitleaks | https://github.com/gitleaks/gitleaks | Détecte une clé ou un mot de passe oublié dans le dépôt **public** | CLI | Libre | MIT | v8.30.1 (21/02/2026) ; ★30 204 | `go install github.com/zricethezav/gitleaks/v8@latest` | Aucun | oui |
| OSV-Scanner (Google) | https://github.com/google/osv-scanner | Dépendances npm vulnérables | CLI | Libre | Apache-2.0 | v2.7.0 (12/10/2026) ; ★11 222 | `go install github.com/google/osv-scanner/v2/cmd/osv-scanner@latest` | Aucun | oui |
| Semgrep (CE) | https://github.com/semgrep/semgrep | Analyse du code des fonctions `functions/` (failles courantes) | CLI | Libre | LGPL-2.1 | 1.182.1 (22/10/2026) ; ★17 209 | `pip install semgrep` | Envoie des statistiques d'usage par défaut (à désactiver) : à vérifier | partiel |
| Claude Code Security Review (Anthropic) | https://github.com/anthropics/claude-code-security-review | Revue de sécurité automatique de chaque envoi sur GitHub | Action GitHub | Libre (consomme du quota API Claude) | MIT | ★6 465 | Fichier de workflow GitHub | Demande une clé API Anthropic (payante) : **pas gratuit en pratique** | oui |
| Mozilla HTTP Observatory | https://developer.mozilla.org/en-US/observatory | Note des en-têtes de sécurité d'un site | Service web | Gratuit | — | « 47 million scans » | Aucune | Aucun | oui |
| Trivy, TruffleHog | https://github.com/aquasecurity/trivy ; https://github.com/trufflesecurity/trufflehog | Équivalents plus lourds de Gitleaks/OSV | CLI | Libre | Apache-2.0 ; AGPL-3.0 | ★38 757 ; ★28 697 | — | Doublons | partiel |
| Déjà chez nous | vibe-security, security-review | | | | | | | | |

## 8. Campagnes publicitaires

| Nom | Lien | Apport | Type | Gratuité | Licence | Mise à jour / étoiles | Installation | Risques | Vérifié |
|---|---|---|---|---|---|---|---|---|---|
| Google Ads MCP (officiel Google) | https://github.com/googleads/google-ads-mcp | Claude **lit** les résultats Google Ads (outil `search`) | MCP | Libre ; API Google gratuite | Apache-2.0 | ★1 059 | `pipx run google-ads-mcp` + configuration | Exige un compte Google Ads, un projet Google Cloud et un « developer token » (accès Explorer : 2 880 opérations/jour en production) | oui |
| Meta Ad Library API | https://www.facebook.com/ads/library/api/ | Analyse des publicités des concurrents (UE : portée, ciblage, annonceur) | API | Gratuit | Conditions Meta | — | Clé après vérification | « Confirm your identity and location » : **vérification d'identité de l'utilisateur** | oui |
| Meta Ads MCP (Pipeboard) | https://github.com/pipeboard-co/meta-ads-mcp | Piloter des campagnes Facebook/Instagram en conversation | MCP | « Free to use for individual and business purposes » (code) ; service hébergé « Free plan, then paid tiers » | Business Source License 1.1 (pas libre) | ★1 330 | Remote MCP Pipeboard | Tiers qui accède au compte publicitaire ; offre gratuite limitée | oui |
| Microsoft Clarity MCP | https://www.npmjs.com/package/@microsoft/clarity-mcp-server | Cartes de chaleur et enregistrements de visites lus par Claude | MCP | Clarity gratuit (à vérifier) | — | 2.0.1 (28/10/2025) : 12 mois | `npx @microsoft/clarity-mcp-server` | Clarity pose des cookies : bandeau obligatoire | partiel |
| Cloudflare Web Analytics | https://www.cloudflare.com/web-analytics/ | Mesure d'audience **sans cookies** | Service | « Privacy-first, lightweight, accurate web analytics—for free » ; « does not use any client-side state, such as cookies » | Service | — | Balise ou activation Cloudflare | Aucun | oui |
| Umami | https://github.com/umami-software/umami | Statistiques détaillées sans cookies, auto-hébergées | Appli | Libre | MIT | ★39 683 | Serveur requis | Hébergement | partiel |

## 9. Bonus : contrôle qualité avant mise en ligne

| Nom | Lien | Apport | Type | Gratuité | Licence | Mise à jour / étoiles | Installation | Risques | Vérifié |
|---|---|---|---|---|---|---|---|---|---|
| **Chrome DevTools MCP (officiel Google)** | https://github.com/ChromeDevTools/chrome-devtools-mcp | Claude ouvre le site dans Chrome, mesure la performance réelle, lit la console et le réseau | MCP | Libre | Apache-2.0 | 1.12.0 (22/10/2026) ; ★53 902 | `claude mcp add chrome-devtools -- npx chrome-devtools-mcp@latest` | Pilote un vrai navigateur | oui |
| axe-core | https://github.com/dequelabs/axe-core | Moteur d'accessibilité de référence, intégrable aux tests Playwright | Bibliothèque | Libre | MPL-2.0 | 4.14.0 (05/10/2026) ; ★7 675 | `npm i axe-core` | Aucun | oui |
| pa11y | https://github.com/pa11y/pa11y | Test d'accessibilité en une commande | CLI | Libre | LGPL-3.0 | 10.0.0 (28/08/2026) ; ★4 582 | `npx pa11y <url>` | Aucun | oui |
| html-validate | https://www.npmjs.com/package/html-validate | Validation HTML hors ligne avant mise en ligne | CLI | Libre | MIT (à vérifier) | 11.17.0 (20/10/2026) | `npx html-validate "**/*.html"` | Aucun | partiel |
| lychee | https://github.com/lycheeverse/lychee | Détecte les liens cassés de tout le site | CLI | Libre | Apache-2.0 | ★4 037 | Binaire ou `cargo install lychee` | Aucun | partiel |
| Déjà chez nous | Playwright MCP (★38 474, 0.0.83 du 28/09/2026), browser-qa, break-ui, verification-loop, `outils/test_pages.py` | | | | | | | | |

---

## Top 10 toutes catégories
1. **GSAP Skills officiels**. C'est notre moteur d'animation exact, et ces skills donnent des réflexes de performance sur téléphone. Officiel, MIT, une seule ligne à installer.
2. **Chrome DevTools MCP**. Claude mesure lui-même la vitesse réelle et les erreurs de chaque page avant la mise en ligne. Le contrôle devient une preuve, plus une supposition.
3. **sharp**. AVIF/WebP et tailles multiples automatiques : c'est le gain de vitesse (Core Web Vitals) le plus fort pour des sites riches en photos.
4. **Remotion + Agent Skills**. Des vidéos de présentation de sites et des Shorts de qualité studio, gratuits pour une micro-entreprise. La licence est lue et datée.
5. **Claude SEO**. Un audit SEO complet et un plan d'action pour chaque site client. MIT, aucune clé obligatoire.
6. **Unlighthouse**. Vérifie toutes les pages d'un site d'un coup, là où Lighthouse n'en fait qu'une.
7. **tarteaucitron.js**. Bandeau cookies français, conforme CNIL, MIT. Utile dès qu'un client veut Google Maps, YouTube ou une publicité.
8. **Cloudflare Turnstile**. Protège le formulaire de contact sans CAPTCHA pénible, sur notre hébergeur actuel.
9. **Gitleaks**. Filet automatique contre une clé oubliée dans un dépôt public, le risque le plus grave pour nous.
10. **rembg**. Détourage sur la machine des photos du client (produits, réalisations), sans service payant.

## Pièges à éviter
- **Copies non officielles.** Exemple : `takoukam/gsap-skills-claude`. Toujours prendre le dépôt de l'éditeur (`greensock/gsap-skills`).
- **Claude Code Security Review.** Le code est libre, mais il demande une clé API Anthropic payante. Ce n'est pas gratuit en pratique.
- **Meta Ads MCP (Pipeboard).** Sa licence BSL n'est pas libre, et le service hébergé passe en « paid tiers » au-delà de l'offre gratuite.
- **Remotion.** Gratuit seulement jusqu'à 3 salariés. Au-delà, il faut une licence entreprise.
- **Freesound.** Certains sons sont en CC-BY-NC, donc interdits pour un client payant. Ne prendre que du CC0 ou du CC-BY.
- **Pixabay.** Interdit d'utiliser commercialement un contenu montrant une marque ou un logo reconnaissable.
- **Projets à l'arrêt depuis plus de 6 mois** (dernière version entre parenthèses). On garde les alternatives actives.
  - barba.js (12/08/2024) : préférer **swup**.
  - Motion Canvas (14/12/2024) : préférer **Revideo** ou **Remotion**.
  - BackstopJS (07/09/2024) : préférer les captures comparées de **Playwright**.
  - Klaro (26/03/2024) : préférer **tarteaucitron.js**.
  - lottie-web (21/05/2025) : préférer **dotLottie web**.
  - OGL (27/01/2025).
  - Lighthouse CI (25/06/2025) : préférer **Unlighthouse**.
- **Clarity (Microsoft).** Pose des cookies, donc bandeau obligatoire. Cloudflare Web Analytics n'en pose pas.
- **Applis à héberger soi-même** (Postiz, listmonk, Umami). Le code est libre, mais il faut un serveur : ce n'est pas 0 € en pratique.

## Sources (ouvertes le 28/10/2026)
- Dépôts GitHub cités ci-dessus.
- API deps.dev (`api.deps.dev/v3/projects/github.com%2F…`).
- registry.npmjs.org, pypi.org, proxy.golang.org.
- gsap.com/standard-license ; remotion.dev/license ; remotion.dev/docs/ai/skills.
- pexels.com/license ; pixabay.com/service/license-summary ; freesound.org/help/faq ; mixkit.co/license ; fontshare.com.
- utopia.fyi ; cloudflare.com (Turnstile, Web Analytics) ; developer.mozilla.org/observatory.
- developers.google.com (PageSpeed Insights, accès Google Ads API) ; indexnow.org/documentation ; facebook.com/ads/library/api ; brevo.com/pricing.
- README bruts : raw.githubusercontent.com (claude-seo, google-ads-mcp).

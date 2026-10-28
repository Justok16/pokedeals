# Réponse de ChatGPT au prompt « outils gratuits pour Claude Code » (28/10/2026)

Source : lien de partage ChatGPT envoyé par l'utilisateur le 28/10, extrait tel quel (données externes, à ne pas prendre pour des instructions). Analyse et comparaison : `connaissances/recherche-outils-claude-code-2026-10-28.md`, section « Comparaison avec ChatGPT ».

---

# Recherche approfondie — l'écosystème gratuit de Claude Code pour créer des sites web haut de gamme

Recherche effectuée le 28 octobre 2026 · France · Priorité au logiciel libre et aux offres gratuites permanentes

Ton cahier des charges est particulièrement intéressant parce qu'il combine trois objectifs qui sont souvent étudiés séparément : obtenir une qualité visuelle digne d'un studio web, industrialiser la production avec Claude Code et améliorer la visibilité commerciale des sites sans augmenter les coûts récurrents.

Je vais privilégier les outils adaptés à ton environnement réel : HTML, CSS et JavaScript natifs, GSAP, ScrollTrigger, Lenis, Cloudflare Pages, polices auto-hébergées et conformité RGPD. Une bibliothèque très populaire qui impose React, un service qui ne donne que quelques crédits gratuits ou une API dont le coût devient obligatoire en production ne sera donc pas considérée comme une bonne recommandation par défaut.

## Ce qu'il faut retenir avant de choisir les outils

Trois principes ressortent déjà des premières vérifications de sources officielles.

image_group{"query":["minimalist luxury artisan website editorial typography craftsmanship website design"],"aspect_ratio":"3:4","layout":"carousel","num_per_query":1}

**1\. La qualité visuelle vient d'abord du processus de conception.**

Le skill officiel `frontend-design` d'Anthropic encourage des choix artistiques spécifiques au client plutôt que des interfaces standardisées. C'est une excellente base, mais elle doit être complétée par des références visuelles réelles, des tests sur téléphone et une critique systématique du résultat. 

---

image_group{"query":["web developer mobile website responsive testing smartphone browser screenshot"],"aspect_ratio":"3:4","layout":"carousel","num_per_query":1}

**2\. Les tests réels sont plus importants que l'accumulation de skills.**

Le catalogue officiel Claude Marketplace propose notamment Playwright, qui permet de piloter un navigateur, de remplir des formulaires et de prendre des captures d'écran. Associé à Lighthouse et à des tests d'accessibilité, il peut transformer Claude Code en véritable boucle de contrôle qualité. 

---

image_group{"query":["local small business craftsman workshop professional website photography natural light"],"aspect_ratio":"3:4","layout":"carousel","num_per_query":1}

**3\. Pour les artisans, la visibilité locale doit être une priorité.**

Les données structurées `LocalBusiness`, un site rapide, un contenu local utile et une fiche d'établissement Google correctement renseignée sont des fondations plus solides que des outils prétendant garantir le référencement dans les réponses des IA. Google documente officiellement les données structurées locales. 

## Méthode de vérification et limites

J'ai ouvert des pages officielles et des dépôts pour les premiers outils retenus, notamment les documentations d'Anthropic, les licences d'Unsplash et d'ImageMagick, la documentation Pexels, les dépôts de GSAP et Lenis, ainsi que des pages de Google, Bing et de la CNIL.

Une distinction est essentielle pour interpréter les tableaux \:

- **Oui** \: la page officielle ou le dépôt a été ouvert et les informations indiquées ont pu être contrôlées.
- **À vérifier** \: une partie des informations nécessaires n'a pas pu être établie de manière fiable, par exemple le tarif exact, le nombre d'étoiles du jour ou la dernière version.
- Une licence logicielle libre ne garantit pas les droits sur les photos, les marques, les personnes représentées, les polices ou les modèles tiers.
- Un outil peut être gratuit à installer tout en dépendant d'une API payante, d'un abonnement Claude ou d'un service distant. Ces coûts indirects sont signalés lorsqu'ils sont identifiés.

**Important \:** une recherche exhaustive au sens strict nécessiterait de contrôler individuellement chaque skill de ta liste, chaque dépendance et chaque condition de licence. Je ne présenterai donc pas les métadonnées non vérifiées comme si elles avaient été contrôlées. Les classements ci-dessous privilégient les outils dont la valeur pour ton activité est la plus élevée.

## 1\. Design de sites d'exception

C'est le domaine où je concentrerais les premiers efforts. L'objectif n'est pas de faire générer plus de CSS à Claude, mais de lui donner une méthode de direction artistique, des références précises et un moyen de détecter les défauts avant livraison.

| Nom | Lien officiel | Apport concret pour un artisan | Type | Gratuité et limites | Licence | Mise à jour / étoiles | Installation en une ligne | Risques | Vérifié |
|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| **Impeccable** | [GitHub](https://github.com/pbakaus/impeccable) | Critique visuelle, amélioration des interfaces, commandes de design et détection de défauts récurrents. Excellent pour supprimer l'aspect générique. | Skill + CLI | Installation gratuite ; `npx impeccable install`\. Pas de quota d'API documenté pour l'usage local. | Apache-2.0 | Environ 70 k étoiles ; dépôt actif en octobre 2026. | `npx impeccable install` | Le CLI exécute du code local et modifie le projet selon les commandes choisies. Examiner les changements. | Oui  |
| **Frontend Design d'Anthropic** | [Dépôt officiel](https://github.com/anthropics/skills/tree/main/skills/frontend-design) | Force une identité visuelle propre à chaque entreprise : typographie, palette, composition et parti pris esthétique. | Skill `SKILL.md` | Gratuit ; le skill n'exige pas sa propre clé d'API. L'utilisation de Claude Code reste soumise à ton accès Claude. | Fichier `LICENSE.txt` du dépôt ; vérifier ses termes exacts avant redistribution. | Dépôt actif ; nombre d'étoiles du dépôt à vérifier. | `claude plugin marketplace add anthropics/skills` puis installer le plugin `frontend-design` si disponible dans la marketplace | Instructions seulement : ne garantit ni la qualité finale ni l'absence de code incorrect. | Oui  |
| **UI UX Pro Max** | [GitHub](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | Base de connaissances consultable sur les styles, palettes, associations typographiques et règles UX. Utile pour construire un système de design cohérent sans framework lourd. | Skill + CLI | Gratuit et open source selon le dépôt ; aucun crédit payant requis pour la base locale. | MIT, selon les métadonnées du projet ; vérifier le fichier LICENSE du dépôt. | Plus de 100 k étoiles rapportées par des indexeurs ; chiffre exact du jour à vérifier. | `claude plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill` puis installer le plugin annoncé dans le dépôt | Peut produire des associations trop standardisées si le brief et les références sont vagues. | Oui pour le dépôt, détails de licence à confirmer  |
| **Emil Kowalski — Skills** | [GitHub](https://github.com/emilkowalski/skills) | Ressources orientées interfaces soignées et interactions. À exploiter comme complément de méthode plutôt que comme système de design complet. | Skills | Dépôt gratuit. | MIT : le fichier de licence autorise l'utilisation, la modification et la redistribution sous ses conditions. | Commit exact et étoiles du jour à vérifier. | `git clone https://github.com/emilkowalski/skills.git` | Lire chaque `SKILL.md` avant installation ; un skill n'est pas un sandbox de sécurité. | Oui  |
| **Refero** | [Site officiel](https://refero.design/) | Références de sites et d'interfaces pour étudier les hiérarchies visuelles, les pages d'accueil et les parcours. | Références visuelles | Accès gratuit exact, limites de recherche et éventuel abonnement : à vérifier. | Pas une licence logicielle ; les captures restent soumises aux droits de leurs auteurs. | À vérifier. | Aucune installation nécessaire. | Ne pas recopier les sites à l'identique ni réutiliser leurs images ou textes sans autorisation. | À vérifier |
| **Aceternity UI** | [Site officiel](https://ui.aceternity.com/) | Inspirations d'animations, effets de survol et composants visuels. Peut donner des idées pour des sections héroïques ou des portfolios. | Bibliothèque de composants | La gratuité et la licence doivent être vérifiées composant par composant ; une partie de l'écosystème peut être liée à React. | Selon le composant et le dépôt source. | À vérifier. | Pas de commande universelle adaptée au HTML natif. | Ne pas introduire Tailwind ou React dans un site statique uniquement pour reproduire un effet. | À vérifier |
| **Figma** | [Site officiel](https://www.figma.com/) | Explorer une maquette, ses espacements, ses composants et ses couleurs avant que Claude écrive le HTML/CSS. Tu disposes déjà du connecteur. | Outil de design + connecteur | Formule gratuite avec limites ; les plafonds actuels doivent être vérifiés. | Conditions propriétaires. | Service actif ; version et limites de formule à vérifier. | Connecteur déjà branché ; aucune installation de bibliothèque requise. | Les fichiers peuvent contenir des informations client ; attention aux autorisations et aux données transmises au connecteur. | À vérifier pour la formule exacte |

### Mon choix pour le design

Je commencerais par **Frontend Design + Impeccable**, puis j'ajouterais UI UX Pro Max si les résultats manquent encore de cohérence.

Ne cumule pas dix skills de design qui donnent des instructions contradictoires. Il vaut mieux une chaîne explicite \:

1. définir l'identité visuelle ;
2. documenter les choix dans un `DESIGN.md` ;
3. réaliser le site en HTML/CSS/JavaScript ;
4. prendre des captures de la version ordinateur et de la version mobile ;
5. faire une critique visuelle ;
6. corriger puis recommencer.

Le dépôt Impeccable annonce notamment une skill, 24 commandes et 62 règles de détection déterministes pour les défauts de design. C'est un avantage concret par rapport à une simple consigne demandant à Claude de « faire plus premium ». 

---

## 2\. Photos, images et polices

Pour un site d'artisan, la meilleure image est souvent une photographie authentique de l'atelier, de l'équipe ou d'une réalisation. Les banques d'images doivent combler les manques, pas donner l'impression que l'entreprise utilise des photos génériques.

| Nom | Lien officiel | Apport concret pour un artisan | Type | Gratuité et limites | Licence | Mise à jour / étoiles | Installation en une ligne | Risques | Vérifié |
|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| **Unsplash** | [Licence](https://unsplash.com/license) | Photos éditoriales de qualité pour illustrer une ambiance, un matériau ou un secteur d'activité. | Banque d'images | « All images can be downloaded and used for free » ; usages commerciaux et non commerciaux autorisés. Attribution appréciée mais non obligatoire. | Licence Unsplash, pas une licence logicielle. | Service actif ; sans étoiles GitHub pertinentes. | Pas d'installation ; téléchargement manuel ou API si nécessaire. | Pas de revente d'images sans modification significative ; droits éventuels sur marques et personnes à examiner. | Oui  |
| **Pexels** | [API officielle](https://www.pexels.com/api/documentation/) | Photos **et vidéos** gratuites. L'API permet à Claude de rechercher des médias pertinents pendant la production. | Banque + API | 200 requêtes/heure et 20 000/mois par défaut ; hausse gratuite possible sur demande selon les conditions de l'API. | Licence Pexels pour les médias ; conditions distinctes pour l'API. | Documentation active, consultée le 28/10/2026. | `curl -H "Authorization: $PEXELS_API_KEY" "https://api.pexels.com/v1/search?query=artisan"` | Clé API nécessaire ; afficher un lien vers Pexels pour les requêtes API ; vérifier les droits des personnes et marques représentées. | Oui  |
| **Squoosh** | [GitHub](https://github.com/GoogleChromeLabs/squoosh) | Comparer visuellement la qualité et le poids de fichiers JPEG, WebP et AVIF avant publication. | Outil web open source | Gratuit. La compression s'effectue localement dans le navigateur ; le projet signale toutefois l'utilisation de Google Analytics. | Apache-2.0 pour le projet. | 25,9 k étoiles ; activité GitHub signalée en octobre 2026. | Ouvrir urlsquoosh.apphttps://squoosh.app/ | Aucun envoi des images au serveur pour la compression d'après le README ; télémétrie à connaître. | Oui  |
| **ImageMagick** | [Licence officielle](https://imagemagick.org/license/) | Traitement en lot, redimensionnement et conversion d'images avant déploiement. | CLI | Gratuit pour un usage commercial. La licence prévoit notamment des obligations d'attribution et de conservation de la licence lors de certaines redistributions. | ImageMagick License | Version stable affichée : 7.1.2-34 ; étoiles non pertinentes pour la page officielle. | `magick input.png -quality 85 output.webp` | Exécute des commandes locales ; contrôler les fichiers de sortie et les paramètres de conversion. | Oui  |
| **Pexels API** | [Documentation](https://www.pexels.com/api/documentation/) | Permet d'automatiser la recherche de visuels par thème et d'alimenter une bibliothèque de médias du projet. | API | Gratuit avec quotas ; clé API nécessaire. | Conditions de l'API et licence Pexels. | Consultée le 28/10/2026. | Utiliser `fetch()` côté script local ou dans un outil de préparation, pas avec la clé exposée dans le navigateur. | Ne jamais mettre la clé API dans le HTML public ; respecter les règles d'attribution de l'API. | Oui  |
| **Fontsource** | [Site officiel](https://fontsource.org/) | Auto-héberger les polices dans le projet et conserver un rendu typographique stable sans dépendance à Google Fonts. | Paquets de polices | Paquets open source gratuits ; la licence doit être vérifiée pour chaque famille téléchargée. | Dépend de la police : souvent OFL, mais pas universellement. | Activité et étoiles du dépôt à vérifier. | `npm install @fontsource-variable/inter` — exemple uniquement, à adapter à la police choisie | Éviter les familles non adaptées à l'identité du client ; vérifier la licence et les variantes réellement nécessaires. | À vérifier pour chaque famille |
| **Google Fonts** | [Site officiel](https://fonts.google.com/) | Catalogue de familles typographiques, à utiliser uniquement comme source de téléchargement lorsque la licence le permet. | Catalogue de polices | Gratuit ; les licences varient selon les familles. | Souvent SIL OFL, mais à contrôler individuellement. | Service actif. | Télécharger les fichiers autorisés puis les héberger sur le site. | Ne pas intégrer les fichiers CSS distants si l'objectif est d'éviter les requêtes vers Google. | À vérifier par police |

Les licences d'Unsplash et les limites de Pexels sont explicitement documentées par leurs éditeurs. Pexels demande notamment de mettre en évidence un lien vers le service lors de l'utilisation de son API. 

### Pipeline d'images que je recommande

**1\. Choisir la source**

Photos du client en priorité ; Unsplash ou Pexels en complément, avec une vérification des droits.

---

**2\. Préparer les fichiers**

Recadrage, redimensionnement et conversion WebP/AVIF ; conserver un original pour les retouches.

---

**3\. Adapter au téléphone**

`srcset`, `sizes`, dimensions explicites, `loading="lazy"` pour les images non prioritaires et chargement prioritaire de l'image principale si nécessaire.

---

**4\. Vérifier**

Comparer la qualité visuelle, le poids, le LCP et le rendu sur une largeur de téléphone réelle.

Pour l'automatisation, **ImageMagick** est plus adapté à une chaîne de traitement locale que Squoosh. Squoosh reste pratique pour les comparaisons visuelles manuelles.

---

## 3\. Animations, transitions et 3D légère

Tu disposes déjà d'une base adaptée avec GSAP, ScrollTrigger et Lenis. Je n'ajouterais pas une deuxième bibliothèque d'animation généraliste sans besoin concret.

| Nom | Lien officiel | Apport concret pour un artisan | Type | Gratuité et limites | Licence | Mise à jour / étoiles | Installation en une ligne | Risques | Vérifié |
|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| **GSAP + ScrollTrigger** | [GitHub officiel](https://github.com/greensock/GSAP) | Révélations au scroll, animations typographiques, effets de profondeur, séquences coordonnées et micro-interactions. | Bibliothèque JavaScript | Le README indique : « the entire GSAP toolset is FREE, even for commercial use ». | Licence standard GreenSock ; consulter [les termes](https://gsap.com/standard-license\.) | Dépôt actif en 2026 ; étoiles exactes à vérifier. | `npm install gsap` | Risque de surcharge visuelle et de coût CPU sur mobile ; respecter `prefers-reduced-motion`\. | Oui  |
| **Lenis** | [GitHub officiel](https://github.com/darkroomengineering/lenis) | Défilement fluide cohérent avec des animations GSAP et des effets de défilement. | Bibliothèque JavaScript | Gratuit, open source. | MIT. | 16,9 k étoiles au moment de la consultation ; dépôt actif. | `npm install lenis` | Peut compliquer le défilement natif si mal intégré ; vérifier ancrages, clavier, tactile et réduction des animations. | Oui  |
| **Three.js** | [Site officiel](https://threejs.org/) | Scène 3D légère, modèle d'un produit ou illustration interactive pour un métier qui s'y prête. | Bibliothèque JavaScript / WebGL | Bibliothèque open source gratuite. | MIT. | Dernière version et étoiles du jour à vérifier. | `npm install three` | WebGL, poids des modèles et consommation GPU ; à éviter sur chaque section d'un site vitrine. | À vérifier pour la version actuelle |
| **CSS natif** | [MDN](https://developer.mozilla.org/en-US/docs/Web/CSS) | Transitions, animations simples, effets de survol, états de boutons et menus accessibles sans dépendance. | Technologie native | Gratuit ; aucune clé API ni dépendance supplémentaire. | Standard web, documentation MDN sous ses conditions propres. | Documentation évolutive. | Aucune installation | Éviter les animations coûteuses de `top`, `left` ou de grandes zones floues ; privilégier `transform` et `opacity` quand cela convient. | Oui pour la documentation, date de révision exacte à vérifier |
| **Motion** | [GitHub](https://github.com/motiondivision/motion) | Alternative d'animation déclarative pour certains projets. | Bibliothèque JavaScript | Gratuit et open source selon le dépôt ; adéquation au HTML natif à vérifier pour le cas retenu. | MIT selon le dépôt ; vérifier la version. | À vérifier. | À définir après vérification de l'API adaptée au projet. | Ne pas ajouter une dépendance principalement conçue pour React si le site n'en utilise pas. | À vérifier |

### Règles d'animation à imposer à Claude Code

Ajoute une consigne permanente dans ton `CLAUDE.md` \:

- privilégier les animations courtes, intentionnelles et réversibles ;
- ne pas animer chaque titre et chaque carte ;
- ne pas empêcher le défilement natif sans nécessité ;
- respecter `prefers-reduced-motion`, y compris pour les animations déclenchées au scroll ;
- éviter les animations qui retardent l'accès au contenu ;
- vérifier les interactions tactiles, le clavier et les liens d'ancrage ;
- mesurer les performances sur un appareil mobile modeste.

GSAP et Lenis sont les choix les plus cohérents avec ton stack actuel. Three.js est une option de différenciation, pas une dépendance par défaut.

---

## 4\. Vidéos de présentation, montage et son

Le besoin doit être séparé en deux cas : créer une vidéo publicitaire ou une vidéo de présentation d'un site, puis produire les fichiers finaux. Les outils qui rendent une vidéo en code ne sont pas tous gratuits dans les mêmes conditions.

| Nom | Lien officiel | Apport concret pour un artisan | Type | Gratuité et limites | Licence | Mise à jour / étoiles | Installation en une ligne | Risques | Vérifié |
|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| **FFmpeg** | [Site officiel](https://ffmpeg.org/) | Conversion, découpage, compression, assemblage, extraction audio et création de rendus vidéo à partir d'images. | CLI | Gratuit et open source ; pas de crédits ni d'API payante. | LGPL ou GPL selon la compilation et les composants activés. | Version et étoiles du jour à vérifier. | `ffmpeg -i input.mov -c:v libx264 -crf 23 output.mp4` | La licence exacte dépend de la compilation ; respecter les droits des sources audio et vidéo. | À vérifier pour la version actuelle |
| **Remotion** | [Tarifs et licence](https://www.remotion.dev/docs/license/pricing) | Générer des vidéos reproductibles à partir de code, de textes, de captures et de séquences animées. | Framework de rendu vidéo | Licence gratuite pour les individus et entreprises de 3 personnes maximum, avec usage commercial illimité selon les conditions. La licence entreprise devient payante au-delà ; l'automatisation de rendus à grande échelle a aussi des conditions propres. | Licence Remotion, pas une simple MIT pour tous les usages. | Version 4.0.526 visible sur la page des releases ; publication affichée au 17 septembre 2026. | `npx create-video@latest` | Le modèle tarifaire dépend de la taille de l'organisation et du mode d'utilisation ; vérifier les conditions avant de construire un service automatisé. | Oui  |
| **Hyperframes** | [Site officiel](https://hyperframes.dev/) | Création de vidéos pilotées par HTML/CSS et animations web, potentiellement adaptées à des présentations de sites. | Outil vidéo en code | Gratuité intégrale et éventuelles dépendances payantes à confirmer. | À vérifier dans le dépôt et ses dépendances. | Dernier commit et étoiles à vérifier. | À vérifier ; ne pas installer avant contrôle du dépôt exact. | Vérifier l'exécution de scripts et les binaires requis. | À vérifier |
| **OpenMontage** | urlRecherche GitHubhttps://github.com/search?q=OpenMontage&type=repositories | Piste de montage automatisé à évaluer si le dépôt exact correspond au projet visé. | Projet / CLI éventuel | Pas de gratuité confirmée pour un dépôt précis. | À vérifier. | À vérifier. | Aucune commande recommandée sans identification du dépôt exact. | Le nom seul ne permet pas de confirmer l'éditeur ou la sécurité. | À vérifier |
| **yt-dlp** | [GitHub officiel](https://github.com/yt-dlp/yt-dlp) | Télécharger des vidéos que tu as le droit de récupérer pour les intégrer à un workflow de montage. | CLI | Gratuit et open source. | Licence principale et dépendances : vérifier le fichier de licence et `THIRD_PARTY_LICENSES.txt` pour les exécutables compilés. | Version `2026.10.26` publiée le 26 octobre 2026. | `python -m pip install -U yt-dlp` | Ne contourner ni DRM ni restrictions d'accès ; respecter les conditions du service source et les droits d'auteur. | Oui  |
| **Pexels Vidéos** | [API officielle](https://www.pexels.com/api/documentation/) | Plans d'illustration et séquences libres d'utilisation commerciale selon la licence Pexels. | Banque de vidéos + API | API gratuite, limitée par défaut à 200 requêtes/h et 20 000/mois. | Licence Pexels pour les médias ; conditions API séparées. | Consultée le 28/10/2026. | Utiliser l'API avec une clé gardée côté serveur ou dans un script local. | Les personnes, marques et éléments protégés dans les vidéos peuvent nécessiter des autorisations supplémentaires. | Oui  |

### Ce que je ferais pour des vidéos clients à 0 €

- **Captures du site** \: Playwright.
- **Animation de textes et d'éléments web** \: HTML/CSS/GSAP.
- **Assemblage et compression** \: FFmpeg.
- **Vidéos d'illustration** \: Pexels, après contrôle de la licence.
- **Rendu vidéo entièrement programmatique** \: Remotion uniquement si la licence correspondant à ton organisation et à ton mode de production reste gratuite.

Je ne considérerais pas un générateur vidéo IA distant comme un outil gratuit permanent tant que ses conditions ne garantissent pas une utilisation durable sans crédits payants.

Pour la musique, il faut vérifier la licence de chaque morceau, y compris les conditions de monétisation, les revendications automatiques et les éventuelles obligations d'attribution. Une piste dite « gratuite » n'est pas nécessairement libre de toute restriction commerciale.

---

## 5\. Marketing, rédaction et acquisition de clients

Pour DIG16, la priorité n'est pas de publier automatiquement partout. Il faut produire des contenus crédibles, démontrer la valeur des sites et créer un système de prospection qui ne devienne ni coûteux ni juridiquement risqué.

| Nom | Lien officiel | Apport concret pour un artisan | Type | Gratuité et limites | Licence | Dernière mise à jour / étoiles | Installation en une ligne pour Claude Code | Risques | Vérifié |
|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| **Corey Haines — Marketingskills** | [GitHub](https://github.com/coreyhaines31/marketingskills) | Ensemble de skills pour le copywriting, le SEO, le CRO, l'analyse marketing et l'acquisition. Très pertinent pour préparer les pages de vente de DIG16 et celles des clients. | Skills + marketplace éventuelle | Gratuit selon le dépôt ; pas de crédits API nécessaires pour les fichiers d'instructions locaux. | MIT, selon le dépôt. | Environ 56,7 k étoiles rapportées le 28 octobre 2026 ; dépôt actif. | `git clone https://github.com/coreyhaines31/marketingskills.git` | Les scripts éventuels et les commandes doivent être inspectés ; certaines recommandations marketing peuvent ne pas convenir au marché français. | Oui  |
| **Claude Code — Frontend Design** | urlAnthropichttps://github.com/anthropics/skills | Améliore le discours commercial par l'alignement entre l'identité du client, le message et le rendu visuel. | Skill | Gratuit comme fichier de skill ; Claude Code reste soumis à l'accès au modèle. | Selon la licence du dépôt et du fichier concerné. | Dépôt officiel actif. | Installer le skill depuis la marketplace officielle. | Ne remplace pas une validation factuelle des promesses commerciales. | Oui  |
| **Gmail** | [Connecteur officiel](https://claude.com/marketplace/plugins) | Préparer et organiser les échanges B2B, retrouver les décisions et suivre les réponses des prospects. | Connecteur | Dépend de ton compte et de ton abonnement Gmail/Google Workspace ; les fonctions de Claude dépendent de ton accès. | Conditions Google et Anthropic. | À vérifier pour le connecteur précis. | Utiliser le connecteur déjà branché si les autorisations sont suffisantes. | Ne pas envoyer automatiquement des messages commerciaux sans validation ; protéger les données de prospects. | À vérifier |
| **Metricool** | [Site officiel](https://metricool.com/) | Planification et analyse des publications sur les réseaux sociaux ; tu disposes déjà du connecteur. | Plateforme + connecteur | Offre gratuite avec limitations potentielles sur les marques, publications et historiques ; seuils actuels à vérifier. | Propriétaire. | À vérifier. | Aucun ajout nécessaire si le connecteur existant couvre les actions souhaitées. | Une automatisation peut publier le mauvais contenu ou divulguer des informations client ; prévoir une validation. | À vérifier |
| **Canva** | [Site officiel](https://www.canva.com/) | Décliner des visuels de portfolio, publications et présentations commerciales. | Outil de design + connecteur | Formule gratuite avec éléments et fonctions limités ; ne pas présumer que tous les modèles, éléments ou fonctions sont gratuits. | Licence Canva et licences propres aux éléments utilisés. | À vérifier pour les quotas actuels. | Utiliser le connecteur existant et privilégier les éléments explicitement gratuits. | Vérifier les droits commerciaux des éléments et modèles ; ne pas réutiliser un élément Pro sans licence appropriée. | À vérifier |
| **Tavily** | [Site officiel](https://tavily.com/) | Recherche web structurée pour étudier un secteur, trouver des informations locales et préparer un dossier de prospect. | API / MCP | Offre gratuite potentiellement limitée ; quotas actuels et éventuelle obligation de paiement à vérifier. | Conditions propriétaires. | À vérifier. | Utiliser le connecteur déjà configuré. | Clé API et transmission de requêtes à un tiers ; ne pas inclure de données confidentielles dans les requêtes. | À vérifier |

Les skills de `marketingskills` sont particulièrement intéressants parce qu'ils couvrent plusieurs étapes du marketing, et non seulement la rédaction. Le dépôt les présente comme des compétences de marketing pour Claude Code et les agents IA, notamment en CRO, copywriting, SEO et growth engineering. 

### Prospection B2B : une précaution importante

La CNIL a publié une version actualisée de ses informations sur la prospection commerciale par voie électronique le **10 juin 2026**\. Pour la prospection professionnelle, l'intérêt légitime peut être applicable lorsque la sollicitation est liée à la profession du destinataire. Il faut néanmoins l'informer et lui permettre de s'opposer simplement et gratuitement, notamment dans chaque message. Les règles applicables aux particuliers sont différentes. 

Pour DIG16, je recommande donc un système où Claude \:

1. recherche des entreprises et vérifie leur activité ;
2. relève uniquement les informations professionnelles nécessaires ;
3. identifie une amélioration réelle et pertinente de leur site ;
4. rédige un message individualisé ;
5. vérifie la pertinence professionnelle et les mentions requises ;
6. laisse l'envoi à une validation humaine, au moins pendant la phase de mise au point.

Évite les campagnes automatisées de masse reposant sur des adresses récupérées sans contrôle. Un outil d'automatisation ne rend pas une prospection licite par lui-même.

---

## 6\. Référencement naturel, SEO local et visibilité dans les réponses des IA

Le référencement d'un artisan doit d'abord répondre à une intention locale : métier, ville ou zone d'intervention, réalisations, coordonnées, preuves de confiance et prise de contact.

Les outils qui promettent une place garantie dans ChatGPT ou Google AI Overviews ne doivent pas être traités comme des solutions SEO garanties.

| Nom | Lien officiel | Apport concret pour un artisan | Type | Gratuité et limites | Licence | Dernière mise à jour / étoiles | Installation en une ligne | Risques | Vérifié |
|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| **Google Search Console** | [Site officiel](https://search.google.com/search-console/about) | Suivi des requêtes, pages indexées, clics, impressions et problèmes d'indexation. | Service web / API | Service gratuit. L'accès API nécessite une autorisation et les quotas techniques applicables. | Service propriétaire. | Service actif ; sans étoiles GitHub. | Aucune installation pour l'interface ; API à configurer si nécessaire. | Nécessite de vérifier la propriété du site ; ne garantit pas de positionnement. | Oui pour le service, quotas API à vérifier |
| **Google PageSpeed Insights / Lighthouse** | urlPageSpeed Insightshttps://pagespeed.web.dev/ · urlGitHub Lighthousehttps://github.com/GoogleChrome/lighthouse | Audit des performances, de l'accessibilité, du SEO et des bonnes pratiques. Très utile avant chaque livraison. | Service web + CLI | Lighthouse est gratuit et open source. Les quotas du service PageSpeed Insights API doivent être contrôlés séparément. | Apache-2.0 pour Lighthouse. | Lighthouse 13.5.0 visible dans les releases ; publication affichée au 18 septembre 2026. | `npx lighthouse https://example.com --view` | Les résultats varient selon l'environnement ; distinguer les données de laboratoire des mesures terrain. | Oui  |
| **Schema.org / LocalBusiness** | urlGoogle Search Centralhttps://developers.google.com/search/docs/appearance/structured-data/local-business · urlSchema.orghttps://schema.org/LocalBusiness | Données structurées JSON-LD pour le nom, l'adresse, les horaires, le téléphone et le type d'activité. | Standard + documentation | Gratuit ; aucune clé API pour écrire le JSON-LD. | Standard ouvert ; documentation et contenus sous leurs conditions respectives. | Documentation officielle consultée le 28/10/2026. | Aucun paquet nécessaire : ajouter un bloc JSON-LD au HTML. | Les données doivent correspondre au contenu réel ; ne pas inventer d'avis ou de caractéristiques. | Oui  |
| **Bing Webmaster Tools / IndexNow** | [IndexNow](https://www.indexnow.com/) · [Bing](https://www.bing.com/webmasters/help/indexnow-0z209wby) | Signaler les URL publiées, mises à jour ou supprimées aux moteurs participants. | Service + protocole | IndexNow est gratuit ; génération et hébergement d'une clé nécessaires. | Protocole ouvert ; conditions propres aux services. | Documentation active ; étoiles non pertinentes. | Créer une clé IndexNow et appeler le point de terminaison officiel depuis un script de publication. | Une soumission ne garantit ni exploration immédiate ni indexation ; Google ne fait pas partie des moteurs participants annoncés par IndexNow. | Oui  |
| **Google LocalBusiness structured data** | [Documentation française](https://developers.google.com/search/docs/appearance/structured-data/local-business?hl=fr) | Aide Google à comprendre les informations d'un établissement local. | Documentation / standard | Gratuit. | Standard et documentation selon leurs conditions. | Consultée le 28/10/2026. | Ajouter le JSON-LD correspondant au vrai établissement. | N'améliore pas automatiquement le classement ; les résultats enrichis ne sont pas garantis. | Oui  |
| **OpenSEO** | [Site officiel](https://openseo.app/) | Piste pour les audits et analyses SEO, puisque tu disposes déjà d'un connecteur. | Service / connecteur | Gratuité permanente, quotas et licences de l'outil exact : à vérifier. | À vérifier. | À vérifier. | Utiliser le connecteur existant après contrôle de ses capacités. | Ne pas lui transmettre des identifiants ou données de clients sans nécessité. | À vérifier |
| **Firecrawl** | [Site officiel](https://www.firecrawl.dev/) | Extraction de contenu de pages pour analyser des concurrents, comparer des services et préparer des audits. | API / MCP | Quotas gratuits et tarifs actuels à vérifier ; ne pas présumer que le plan gratuit suffit à un usage intensif. | Conditions propriétaires du service et licence des composants concernés. | À vérifier. | Utiliser le connecteur existant avec des quotas surveillés. | Les données sont envoyées à un service tiers ; respecter les droits des sites consultés et les restrictions d'accès. | À vérifier |
| **Tavily** | [Site officiel](https://tavily.com/) | Recherche web et collecte de sources pour les analyses SEO et les recherches sectorielles. | API / MCP | Gratuité limitée à vérifier ; clé API généralement nécessaire. | Propriétaire. | À vérifier. | Connecteur déjà disponible. | Vérifier les quotas et la provenance des données avant d'automatiser. | À vérifier |

### Ce que Claude devrait générer pour chaque site livré

Je transformerais le SEO en une checklist de livraison obligatoire \:

- titre et meta description distincts par page ;
- une structure de titres logique ;
- URLs canoniques ;
- sitemap XML et `robots.txt` cohérents ;
- liens internes fonctionnels ;
- images avec dimensions, textes alternatifs pertinents et chargement adapté ;
- données JSON-LD exactes pour l'activité ;
- coordonnées cohérentes avec la fiche d'établissement ;
- liens de contact, téléphone et itinéraire vérifiés ;
- contrôle des erreurs 404, redirections et pages non indexables ;
- audit Lighthouse et contrôle sur téléphone ;
- soumission de la sitemap et, si pertinent, notification IndexNow.

Pour la visibilité dans les réponses des IA, ajoute un contenu réellement utile, des informations factuelles cohérentes sur l'entreprise et des pages qui répondent précisément aux questions des clients. Mesure ensuite le trafic et les références observables. **Il n'existe pas de commande magique qui garantisse une citation dans ChatGPT, Perplexity ou les résultats génératifs de Google.**

---

## 7\. Sécurité, accessibilité et conformité RGPD

Ce domaine mérite une automatisation forte : les erreurs sont souvent invisibles à l'œil nu, mais peuvent exposer des secrets, dégrader l'accessibilité ou laisser un formulaire vulnérable.

| Nom | Lien officiel | Apport concret pour un artisan | Type | Gratuité et limites | Licence | Dernière mise à jour / étoiles | Installation en une ligne | Risques | Vérifié |
|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| **Playwright** | [Site officiel](https://playwright.dev/) | Tests automatisés sur Chromium, Firefox et WebKit, captures d'écran, formulaires, navigation et contrôle mobile. | Bibliothèque / CLI / MCP | Gratuit et open source. | Apache-2.0. | Version publiée dans le dépôt ; étoiles exactes du jour à vérifier. | `npm install -D @playwright/test` | Exécute un navigateur et des scripts locaux ; les tests peuvent envoyer des formulaires réels si l'environnement n'est pas isolé. | Oui  |
| **axe-core** | [GitHub officiel](https://github.com/dequelabs/axe-core) | Détecte de nombreux problèmes d'accessibilité : noms accessibles, attributs ARIA et autres violations automatisables. | Bibliothèque de tests | Gratuit et open source. | MPL-2.0 ; consulter le fichier LICENSE du dépôt. | Version 4.14.0 publiée le 5 octobre 2026. | `npm install -D @axe-core/playwright` | Ne détecte pas tous les problèmes ; un audit manuel au clavier reste nécessaire. | Oui  |
| **Gitleaks** | [GitHub officiel](https://github.com/gitleaks/gitleaks) | Recherche de clés API, mots de passe et secrets accidentellement commis dans les fichiers ou l'historique Git. | CLI | Gratuit, sans API payante obligatoire. | MIT. | Release v8.30.1 ; publication le 21 mars 2026 ; environ 30 k étoiles selon les indexeurs consultés. | `gitleaks detect --source .` — vérifier la syntaxe correspondant à la version installée. | Peut produire des faux positifs ; configurer des exclusions sans masquer les vrais secrets. | Oui pour le dépôt et la licence, commande à confirmer selon la version  |
| **Lighthouse** | [GitHub](https://github.com/GoogleChrome/lighthouse) | Contrôle des performances, de l'accessibilité, du SEO et des bonnes pratiques avant déploiement. | CLI / outil d'audit | Gratuit, open source. | Apache-2.0. | Version 13.5.0 affichée en septembre 2026. | `npx lighthouse https://example.com --view` | Un bon score ne garantit ni la sécurité ni la conformité légale. | Oui  |
| **ImageMagick** | [Licence](https://imagemagick.org/license/) | Traitement local des images avant leur publication, pour éviter des ressources trop lourdes. | CLI | Gratuit pour un usage commercial. | ImageMagick License. | Version stable affichée 7.1.2-34. | `magick input.jpg -resize 1600x1600\> output.jpg` | Exécute des commandes locales ; vérifier les fichiers produits. | Oui  |
| **Cloudflare Pages `_headers`** | [Documentation officielle](https://developers.cloudflare.com/pages/configuration/headers/) | Définir des en-têtes de sécurité, par exemple CSP, `X-Content-Type-Options` et `Referrer-Policy`\. | Configuration de déploiement | Fonction disponible dans Cloudflare Pages ; pas d'API payante nécessaire pour écrire le fichier. | Conditions Cloudflare. | Documentation mise à jour le 25 août 2026. | Créer un fichier `_headers` dans le répertoire publié. | Une CSP trop stricte peut bloquer scripts, styles ou polices ; tester chaque site après modification. | Oui  |
| **Anthropic Security Guidance** | [Claude Marketplace](https://claude.com/marketplace/plugins) | Relecture orientée sécurité des modifications de Claude, détection de certaines classes de vulnérabilités. | Plugin / skill | Plugin répertorié comme vérifié par Anthropic ; coût supplémentaire et compatibilité exacte à confirmer pour ton accès. | Conditions du plugin et du dépôt. | Marketplace consultée le 28/10/2026. | Installer le plugin officiel `Security Guidance` depuis la marketplace Claude Code. | Une revue IA ne remplace pas les tests de sécurité et la validation humaine. | Oui pour la présence en marketplace  |

### Fichier `_headers` pour Cloudflare Pages

Voici une base à faire vérifier par Claude selon les ressources du site \:

```text
/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: DENY
  Permissions-Policy: camera=(), microphone=(), geolocation=()
```

La CSP mérite un traitement séparé : elle doit tenir compte des scripts, des styles, des images, des polices et des formulaires effectivement utilisés. N'ajoute pas aveuglément `default-src 'self'` sans tester l'ensemble du site.

La documentation Cloudflare confirme que le fichier `_headers` permet de définir ou de remplacer les en-têtes de réponse des ressources statiques. 

### RGPD : ce qui ne se règle pas avec une simple bibliothèque

Un site statique peut être très simple à rendre respectueux de la vie privée, mais il faut contrôler \:

- les cookies et stockages réellement utilisés ;
- les scripts tiers, les cartes intégrées, les vidéos et les outils statistiques ;
- les formulaires et les données collectées ;
- les mentions légales et les informations relatives aux traitements ;
- les durées de conservation, la sécurité et les modalités d'exercice des droits ;
- la nécessité réelle d'une bannière de consentement selon les traceurs et traitements.

Ne demande pas à Claude d'ajouter une bannière de cookies par défaut à chaque site. Il doit d'abord analyser les traitements et les traceurs effectivement présents.

---

## 8\. Campagnes publicitaires Google Ads et Meta Ads

Le budget publicitaire lui-même n'est pas gratuit. En revanche, les outils de préparation, d'analyse et de suivi peuvent réduire le coût du travail.

| Nom | Lien officiel | Apport concret pour un artisan | Type | Gratuité et limites | Licence | Mise à jour / étoiles | Installation en une ligne | Risques | Vérifié |
|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| **Meta Ad Library** | urlBibliothèque publicitairehttps://www.facebook.com/ads/library/ | Étudier les publicités visibles de concurrents et les messages utilisés dans un secteur. | Outil web | Consultation gratuite ; les fonctions d'API et les données accessibles dépendent des règles Meta. | Service propriétaire. | Service actif ; sans étoiles GitHub. | Pas d'installation requise. | Ne pas confondre visibilité d'une publicité et rentabilité réelle ; disponibilité variable selon les pays et catégories. | Oui pour le service, détails d'API à vérifier |
| **Google Ads Transparency Center** | [Site officiel](https://adstransparency.google.com/) | Examiner les publicités diffusées par un annonceur, les variantes de message et certains détails de diffusion. | Outil web | Consultation gratuite. | Service propriétaire. | Service actif ; sans étoiles GitHub. | Pas d'installation requise. | Les informations publiques ne révèlent pas nécessairement le ciblage, le budget ou les conversions. | Oui pour le service |
| **Google Ads API** | [Documentation officielle](https://developers.google.com/google-ads/api) | Automatiser la préparation, la consultation et le suivi de campagnes avec les autorisations appropriées. | API | Pas de coût de licence pour l'API elle-même, mais l'utilisation de Google Ads peut engendrer des dépenses publicitaires. Les accès et quotas doivent être vérifiés. | Conditions Google Ads API. | Documentation active ; modèle d'accès modifié en 2026. | Configurer un projet Google Cloud et l'accès API avant d'écrire un script. | Les scripts peuvent modifier ou lancer des campagnes payantes ; exiger une confirmation avant toute action. | Oui pour la documentation, quotas exacts à vérifier  |
| **Meta Marketing API** | [Documentation officielle](https://developers.facebook.com/docs/marketing-apis/) | Automatiser des opérations autorisées sur les comptes publicitaires et récupérer certaines données de campagne. | API | Pas de garantie de disponibilité universelle : permissions, examen d'application, rôles et accès peuvent être nécessaires. Les annonces restent payantes. | Conditions Meta. | À vérifier pour les autorisations exactes. | Configurer une application Meta et les permissions requises. | Accès aux comptes et données sensibles ; ne pas automatiser de dépense sans garde-fous. | À vérifier |
| **Google Tag Manager** | [Site officiel](https://tagmanager.google.com/) | Centraliser les balises de mesure lorsque le client en a réellement besoin. | Service web | Gratuit dans sa version standard. | Propriétaire. | Service actif. | Pas d'installation CLI nécessaire. | Peut charger des traceurs tiers et nécessiter une gestion du consentement selon la configuration. | Oui pour le service ; conformité à analyser au cas par cas |

### Règles de sécurité pour les campagnes

Pour une automatisation Claude Code, sépare les actions en trois catégories \:

- **Lecture seule** \: rapports, statistiques, inventaire des campagnes.
- **Préparation** \: création d'un brouillon de campagne, rédaction des annonces, estimation des paramètres.
- **Actions payantes** \: publication, modification de budget, changement de ciblage et activation.

La troisième catégorie doit nécessiter une confirmation humaine explicite. Une clé API autorisée à modifier les campagnes peut dépenser de l'argent réel.

---

## 9\. Outils complémentaires : tests visuels, documentation et automatisation

C'est probablement la catégorie où tu peux obtenir le gain de productivité le plus immédiat : Claude devient beaucoup plus efficace quand il peut vérifier ce qu'il vient de produire.

| Nom | Lien officiel | Apport concret pour un artisan | Type | Gratuité et limites | Licence | Mise à jour / étoiles | Installation en une ligne | Risques | Vérifié |
|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| **Playwright MCP** | [Plugin Claude Marketplace](https://claude.com/marketplace/plugins) | Permet à Claude d'ouvrir le site, cliquer, remplir des formulaires, naviguer et produire des captures. | MCP / plugin | Logiciel Playwright gratuit ; coûts éventuels liés à l'accès Claude ou à d'autres services à distinguer. | Apache-2.0 pour Playwright. | Plugin officiel répertorié ; version exacte du serveur à vérifier. | Installer le plugin Playwright depuis la marketplace officielle. | Le navigateur peut exécuter du JavaScript et soumettre des formulaires ; utiliser un environnement de test. | Oui  |
| **Chrome DevTools MCP** | [GitHub](https://github.com/ChromeDevTools/chrome-devtools-mcp) | Inspecter un site dans Chrome, consulter des informations de performance et aider au diagnostic des problèmes réels. | MCP | Projet open source gratuit. | Apache-2.0. | Dépôt actif ; étoiles exactes à vérifier. | `npx -y chrome-devtools-mcp@latest` — vérifier les instructions du dépôt avant lancement. | Lance un serveur local et pilote un navigateur ; n'exposer que les accès nécessaires. | Oui pour la licence, commande et version à confirmer  |
| **Context7** | [Marketplace Claude](https://claude.com/marketplace/plugins) | Fournir à Claude une documentation actualisée des bibliothèques afin de limiter les API inventées ou obsolètes. | MCP / plugin | Plugin répertorié dans la marketplace ; quotas et conditions du service distant à vérifier. | Selon le serveur et les composants. | Marketplace consultée le 28/10/2026. | Installer le plugin Context7 depuis la marketplace. | Envoie les requêtes de documentation au service distant ; ne pas y transmettre de secrets. | Oui pour la présence en marketplace  |
| **Superpowers** | [Marketplace Claude](https://claude.com/marketplace/plugins) | Structure le travail de l'agent : planification, développement, débogage et tests. | Plugin + skills | Gratuit à installer selon le dépôt ; dépend de l'accès à Claude Code. | Vérifier la licence du dépôt officiel avant redistribution. | Plugin répertorié comme vérifié par Anthropic. | Installer `Superpowers` depuis la marketplace. | Peut ajouter des étapes et consommer davantage de temps et de contexte ; adapter le workflow à un site statique. | Oui pour la présence en marketplace  |
| **GitHub Actions** | [Documentation](https://docs.github.com/actions) | Exécuter automatiquement les audits, tests, vérifications de liens et contrôles de build avant déploiement. | CI/CD | Quotas gratuits selon le type de dépôt, l'exécuteur et le forfait ; vérifier les limites actuelles. | Service propriétaire avec conditions spécifiques. | Service actif. | Ajouter un workflow YAML dans `.github/workflows/`\. | Les secrets des workflows doivent être protégés ; ne jamais exécuter du code non fiable avec des secrets de production. | À vérifier pour les quotas précis |
| **Cloudflare Pages** | [Documentation officielle](https://developers.cloudflare.com/pages/) | Hébergement statique et déploiement des sites, avec configuration des en-têtes et intégration Git. | Hébergement / CI/CD | Offre gratuite avec limites ; vérifier les quotas applicables à ton usage. | Service propriétaire. | Documentation active ; mise à jour de la page des en-têtes le 25 août 2026. | Déploiement via Git ou Wrangler selon le projet. | Les fonctions serveur et certaines options avancées peuvent relever de limites différentes du simple hébergement statique. | Oui pour les en-têtes, quotas actuels à vérifier  |

### Boucle de vérification que je mettrais en place

**Étape 1 — Génération**

Claude modifie le HTML, le CSS et le JavaScript, puis explique les fichiers changés.

**Étape 2 — Inspection visuelle**

Playwright prend des captures à plusieurs largeurs, notamment téléphone et ordinateur.

**Étape 3 — Contrôles automatiques**

Playwright, axe-core et Lighthouse contrôlent les parcours, les problèmes d'accessibilité et les performances.

**Étape 4 — Contrôle avant publication**

Gitleaks, vérification des liens, inspection des en-têtes et relecture des changements avant déploiement.

Cette boucle apporte davantage de garanties qu'une longue liste de prompts de programmation : elle permet de détecter des défauts visibles, fonctionnels et techniques, puis de les corriger avant livraison.

---

## 10\. Top 10 toutes catégories : les outils que je choisirais en premier

Voici mon classement selon le gain attendu pour tes sites, leur visibilité, la fiabilité des livraisons et le respect de ton budget. Il s'agit d'un classement de pertinence pour DIG16, pas d'un classement général de popularité.

image_group{"query":["Impeccable design system website interface visual design audit"],"aspect_ratio":"4:5","layout":"carousel","num_per_query":1}

## 1\. Impeccable

(Priorité immédiate)

**Pourquoi lui avant les autres \:** il cible directement le défaut le plus coûteux d'un site généré par IA : une interface fonctionnelle, mais générique. Ses commandes et règles de critique donnent un processus d'amélioration répétable.

[Dépôt officiel](https://github.com/pbakaus/impeccable) · Apache-2.0 · Installation gratuite.

---

image_group{"query":["Anthropic Claude Code frontend design skill website typography creative art direction"],"aspect_ratio":"4:5","layout":"carousel","num_per_query":1}

## 2\. Frontend Design d'Anthropic

**Pourquoi avant les autres \:** c'est le socle de direction artistique à appliquer avant d'écrire les composants. Il pousse Claude à choisir une identité adaptée à l'activité plutôt qu'à reproduire les mêmes modèles.

[Skill officiel](https://github.com/anthropics/skills/tree/main/skills/frontend-design) · Licence à vérifier dans le dépôt.

---

image_group{"query":["Playwright browser automation mobile desktop screenshot website testing"],"aspect_ratio":"4:5","layout":"carousel","num_per_query":1}

## 3\. Playwright

**Pourquoi avant les autres \:** il donne à Claude les moyens de vérifier un site réel, et pas seulement de produire du code qui semble correct. Les captures et les tests de formulaires sont particulièrement précieux pour le téléphone.

[Site officiel](https://playwright.dev/) · Apache-2.0 · Gratuit.

---

image_group{"query":["Google Lighthouse website performance audit Core Web Vitals mobile report"],"aspect_ratio":"4:5","layout":"carousel","num_per_query":1}

## 4\. Lighthouse

**Pourquoi avant les autres \:** il apporte une mesure technique répétable avant la mise en ligne. Il aide à détecter les régressions de performance et d'accessibilité qui ne se voient pas nécessairement dans une capture d'écran.

[GitHub officiel](https://github.com/GoogleChrome/lighthouse) · Apache-2.0 · Gratuit.

---

image_group{"query":["axe core accessibility testing website browser audit"],"aspect_ratio":"4:5","layout":"carousel","num_per_query":1}

## 5\. axe-core

**Pourquoi avant les autres \:** il complète Lighthouse par des tests d'accessibilité intégrables aux tests automatisés. C'est une façon peu coûteuse de contrôler chaque livraison, tout en conservant une vérification manuelle.

[Dépôt officiel](https://github.com/dequelabs/axe-core) · MPL-2.0 · Gratuit.

---

image_group{"query":["GSAP ScrollTrigger premium editorial website scroll animation typography"],"aspect_ratio":"4:5","layout":"carousel","num_per_query":1}

## 6\. GSAP + ScrollTrigger

**Pourquoi avant les autres \:** tu connais déjà cette technologie. Elle te permet d'obtenir des animations élaborées sans changer de stack ni introduire un framework lourd. Son utilisation commerciale gratuite est explicitement annoncée par le projet.

[Dépôt officiel](https://github.com/greensock/GSAP) · Licence standard GreenSock.

---

image_group{"query":["Google Search Console search analytics local business website performance report"],"aspect_ratio":"4:5","layout":"carousel","num_per_query":1}

## 7\. Google Search Console

**Pourquoi avant les autres \:** elle fournit des données de recherche réelles. Pour améliorer la visibilité des artisans, ces données sont plus utiles que des promesses d'outils SEO qui ne démontrent pas leurs résultats.

[Site officiel](https://search.google.com/search-console/about) · Gratuit.

---

image_group{"query":["Schema.org JSON LD structured data local business website code"],"aspect_ratio":"4:5","layout":"carousel","num_per_query":1}

## 8\. Schema.org / LocalBusiness

**Pourquoi avant les autres \:** les informations structurées sont peu coûteuses à intégrer et peuvent améliorer la compréhension de l'activité et des coordonnées du client par les moteurs. C'est une excellente tâche à standardiser dans chaque projet.

[Documentation Google](https://developers.google.com/search/docs/appearance/structured-data/local-business) · Gratuit.

---

image_group{"query":["Unsplash professional artisan woodworking workshop natural light photography"],"aspect_ratio":"4:5","layout":"carousel","num_per_query":1}

## 9\. Unsplash + Pexels

**Pourquoi avant les autres \:** ils donnent accès à des visuels de qualité sans abonnement obligatoire. Le meilleur résultat reste cependant d'utiliser les propres réalisations du client et de réserver les banques d'images aux illustrations complémentaires.

urlLicence Unsplashhttps://unsplash.com/license · [API Pexels](https://www.pexels.com/api/documentation/) · Conditions commerciales à respecter.

---

image_group{"query":["Gitleaks terminal security scan developer code repository"],"aspect_ratio":"4:5","layout":"carousel","num_per_query":1}

## 10\. Gitleaks

**Pourquoi avant les autres \:** il réduit un risque concret des projets développés avec des agents : la présence accidentelle de clés API ou de secrets dans le code et l'historique Git. Son coût d'utilisation ne dépend pas de crédits IA.

[Dépôt officiel](https://github.com/gitleaks/gitleaks) · MIT · Gratuit.

## 11\. Comment exploiter tes connecteurs et tes outils existants

Tu as déjà plusieurs connecteurs qui couvrent une partie des besoins. Je n'ajouterais pas un nouvel outil avant d'avoir testé les fonctions effectivement accessibles par les connecteurs actuels.

| Connecteur existant | Usage prioritaire | Ce qui manque éventuellement |
|--------|--------|--------|
| Playwright | Contrôle visuel et fonctionnel des sites | Scénarios de tests standardisés, captures multi-tailles |
| Unsplash | Recherche de photos | Vérification des droits et intégration dans le pipeline d'images |
| Canva | Visuels marketing et présentations | Bibliothèque de modèles réutilisables et validation humaine |
| Figma | Références, maquettes et direction artistique | Génération et contrôle d'un `DESIGN.md` |
| OpenSEO | Audits SEO | Vérifier les fonctions réellement accessibles et les quotas |
| Metricool | Publications et analyse sociale | Calendrier éditorial et approbation des publications |
| vidIQ | Analyse YouTube | Vérifier les fonctions gratuites et les quotas du connecteur |
| Tavily | Recherche web | Workflow de recherche avec sources et contrôle des faits |
| Firecrawl | Extraction de contenu web | Respect des droits, quotas et règles d'accès |
| Gmail | Suivi commercial | Processus de validation avant envoi |
| Google Drive | Documents clients | Organisation des livrables et contrôle des permissions |
| Google Agenda | Planification | Automatisation des rappels de livraison |
| Zapier | Automatisation entre services | Vérifier les quotas gratuits avant toute dépendance opérationnelle |
| GitHub | Versionnement et automatisation | Tests, audits de sécurité et contrôle avant déploiement |
| Vercel | Prévisualisation éventuelle | Ne pas confondre les limites de Vercel avec celles de Cloudflare Pages |

Pour chacun, il reste à confirmer les autorisations exactes, les quotas et les fonctions exposées par le connecteur. La présence d'un connecteur ne signifie pas que toutes les opérations du service sont accessibles gratuitement.

---

## 12\. Pièges à éviter

Cette liste est volontairement stricte : elle distingue les outils réellement gratuits des solutions qui peuvent entraîner des dépenses, des risques de licence ou des problèmes de sécurité.

| Piège | Pourquoi l'éviter | Alternative ou mesure |
|--------|--------|--------|
| **Les outils IA de génération d'images ou de vidéos avec crédits gratuits** | Le quota peut être épuisé rapidement et l'utilisation continue nécessiter un paiement. | Favoriser les outils locaux et les banques d'images avec une licence commerciale explicite. |
| **Les offres « gratuit pour commencer »** | Un essai gratuit ou une offre temporaire ne satisfait pas ton budget de 0 €. | Lire les tarifs, les conditions de renouvellement et les limites avant installation. |
| **Les skills trouvés sur un agrégateur sans dépôt identifiable** | Le nom, la popularité et les scores de sécurité d'un agrégateur ne prouvent pas l'identité du mainteneur ni l'innocuité du code. | Installer depuis le dépôt officiel, lire `SKILL.md`, les scripts et la licence. |
| **Les skills qui exécutent des commandes opaques** | Une skill peut demander à Claude d'exécuter des commandes, de télécharger du code ou d'accéder à des fichiers. | Inspecter les scripts et limiter les permissions ; éviter les commandes distantes exécutées sans examen. |
| **Les bibliothèques de composants qui imposent React** | Elles augmentent inutilement les dépendances et peuvent être mal adaptées au HTML statique. | Réutiliser les idées de design, puis implémenter en CSS/JavaScript natif. |
| **Les promesses de référencement garanti dans les IA** | Aucun outil ne peut garantir une citation dans ChatGPT, Perplexity ou les résultats génératifs de Google. | Travailler les contenus, les données structurées, l'indexation et mesurer les résultats. |
| **Les générateurs de mentions légales ou de conformité automatiques** | Une génération standard ne connaît pas nécessairement les traitements et la situation juridique réelle du client. | Utiliser un questionnaire factuel et vérifier les textes au cas par cas. |
| **Les modèles de sites réutilisés sans licence claire** | Une capture de référence n'autorise pas à réutiliser le code, les textes, les illustrations ou les polices. | Vérifier les licences et utiliser les références comme inspiration, non comme contenu à copier. |
| **Les API dont la clé est placée dans le JavaScript public** | Un visiteur peut récupérer la clé et consommer le quota ou les autorisations associées. | Utiliser un script local, une fonction serveur adaptée ou un mécanisme sécurisé. |
| **Les outils de publication publicitaire automatisée sans confirmation** | Une mauvaise configuration peut dépenser de l'argent réel ou diffuser une publicité non validée. | Séparer lecture, préparation et publication ; exiger une confirmation explicite avant les dépenses. |
| **Les audits automatisés considérés comme une certification** | Lighthouse, axe-core et les scans de sécurité ne détectent pas tout. | Combiner tests automatiques, revue humaine et essais sur appareil réel. |
| **Les dépôts abandonnés** | Une bibliothèque peut être incompatible avec les versions actuelles ou contenir des dépendances vulnérables. | Vérifier la date du dernier commit, les releases, les issues et les dépendances. Une référence historique peut néanmoins rester pertinente si elle est stable et comprise. |

### Cas particulier : les projets que tu as déjà repérés

- **Superpowers** \: à tester comme méthode de travail ; n'empile pas ses instructions avec plusieurs workflows concurrents.
- **ECC (Everything Claude Code)** \: à auditer skill par skill, notamment les scripts, hooks, permissions et licences.
- **Agent Skills d'Addy Osmani** \: intéressant pour l'ingénierie frontend ; contrôler les compétences exactes du dépôt et leur licence.
- **Scroll-craft** \: vérifier le dépôt source exact, les dépendances et l'actualité du projet avant installation.
- **ArtCraft / PhotoCraft / LightCraft** \: noms trop ambigus pour confirmer ici une licence, un mainteneur et un dépôt uniques. Ne pas installer sans URL précise.
- **Hyperframes** \: ne pas présumer que tous les usages sont gratuits sans contrôler le dépôt exact et les dépendances nécessaires au rendu.
- **OpenMontage** \: le nom seul ne suffit pas à identifier avec certitude le projet visé. Je ne recommande donc pas une installation à ce stade.
- **Les séries de skills `better-*`, `ig-*`, `seo-*`, `high-end-visual-design`, `taste-design`, `brag-slim`, `humanizer` et autres** \: une famille de noms ne garantit ni une origine commune ni une licence commune. Vérifier chaque dépôt et sa version.

Je n'affirme pas que ces projets sont dangereux ou payants : je les classe comme **non confirmés** tant que le dépôt et les conditions exactes ne sont pas établis.

---

## 13\. Le workflow que je mettrais en production pour DIG16

Je commencerais par un ensemble réduit, entièrement local lorsque c'est possible, et sans service payant supplémentaire.

## Socle de production

Stack existant conservé : HTML/CSS/JavaScript, GSAP, ScrollTrigger, Lenis, Cloudflare Pages et polices locales.

---

**Design**

Frontend Design + Impeccable + un fichier `DESIGN.md` propre à chaque client.

**Médias**

Photos du client, Unsplash/Pexels si nécessaire, puis optimisation locale avec ImageMagick.

**Tests**

Playwright pour les parcours et les captures, axe-core pour l'accessibilité, Lighthouse pour les audits.

**SEO**

JSON-LD, Search Console, sitemap, contrôle des liens et IndexNow lorsque pertinent.

**Sécurité**

Gitleaks, revue des dépendances, en-têtes Cloudflare, contrôle des formulaires et vérification des traitements de données.

**Publication**

GitHub, tests avant déploiement, captures conservées et validation humaine finale.

### Ordre de mise en place

1. Installer et tester Frontend Design et Impeccable sur un site existant.
2. Ajouter un script de captures Playwright pour les tailles de téléphone et d'ordinateur.
3. Intégrer Lighthouse et axe-core dans la checklist de livraison.
4. Ajouter Gitleaks au contrôle des dépôts.
5. Créer un modèle de SEO local comprenant JSON-LD, sitemap, métadonnées et contrôles de liens.
6. Automatiser progressivement les tâches répétitives uniquement après validation de leur fiabilité.

Ce socle permet de renforcer la qualité sans remplacer ton stack et sans dépendre d'une plateforme de génération de sites payante.

---

## 14\. Sources officielles consultées

Les liens ci-dessous renvoient aux documentations, dépôts et licences utilisés dans cette recherche. Les pages ouvertes sont identifiées dans les citations des tableaux. Les informations qui restent à vérifier ont été explicitement signalées : la présence d'un lien dans cette liste ne vaut pas validation de tous les tarifs ou de toutes les versions.

### Claude Code, skills et design

- [Claude Marketplace](https://claude.com/marketplace/plugins)
- urlAnthropic — Agent Skillshttps://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- urlAnthropic — Frontend Designhttps://github.com/anthropics/skills/tree/main/skills/frontend-design
- [Impeccable](https://github.com/pbakaus/impeccable)
- [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)
- [Emil Kowalski — Skills](https://github.com/emilkowalski/skills)
- [Corey Haines — Marketingskills](https://github.com/coreyhaines31/marketingskills)
- [Figma](https://www.figma.com/)
- [Aceternity UI](https://ui.aceternity.com/)

### Images, polices et optimisation

- urlLicence Unsplashhttps://unsplash.com/license
- [API Pexels](https://www.pexels.com/api/documentation/)
- [Licence Pexels — usage commercial](https://help.pexels.com/hc/en-us/articles/360042295214-Can-I-use-the-photos-and-videos-for-a-commercial-project)
- urlGoogleChromeLabs — Squooshhttps://github.com/GoogleChromeLabs/squoosh
- [Licence ImageMagick](https://imagemagick.org/license/)
- [Fontsource](https://fontsource.org/)
- [Google Fonts](https://fonts.google.com/)

### Animations et vidéos

- [GSAP](https://github.com/greensock/GSAP)
- [Licence standard GSAP](https://gsap.com/standard-license)
- [Lenis](https://github.com/darkroomengineering/lenis)
- urlThree.jshttps://threejs.org/
- [Remotion — licences et tarifs](https://www.remotion.dev/docs/license/pricing)
- [Remotion — releases](https://github.com/remotion-dev/remotion/releases)
- [FFmpeg](https://ffmpeg.org/)
- [Hyperframes](https://hyperframes.dev/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)

### SEO et indexation

- urlGoogle Search Consolehttps://search.google.com/search-console/about
- urlGoogle Lighthousehttps://github.com/GoogleChrome/lighthouse
- [Google — données structurées LocalBusiness](https://developers.google.com/search/docs/appearance/structured-data/local-business)
- urlSchema.org — LocalBusinesshttps://schema.org/LocalBusiness
- [IndexNow](https://www.indexnow.com/)
- [Bing Webmaster Tools — IndexNow](https://www.bing.com/webmasters/help/indexnow-0z209wby)
- [OpenSEO](https://openseo.app/)
- [Firecrawl](https://www.firecrawl.dev/)
- [Tavily](https://tavily.com/)

### Tests, sécurité et hébergement

- urlPlaywrighthttps://playwright.dev/
- urlPlaywright — dépôt officielhttps://github.com/microsoft/playwright
- [axe-core](https://github.com/dequelabs/axe-core)
- [Gitleaks](https://github.com/gitleaks/gitleaks)
- urlChrome DevTools MCPhttps://github.com/ChromeDevTools/chrome-devtools-mcp
- [Cloudflare Pages — en-têtes HTTP](https://developers.cloudflare.com/pages/configuration/headers/)
- [Cloudflare Pages](https://developers.cloudflare.com/pages/)
- [GitHub Actions](https://docs.github.com/actions)

### Marketing, publicité et conformité

- [CNIL — prospection commerciale par courrier électronique, SMS-MMS et automate d'appel](https://www.cnil.fr/fr/la-prospection-commerciale-par-courrier-electronique-sms-mms-et-automate-dappel)
- [CNIL — questions-réponses sur la prospection B2B](https://www.cnil.fr/fr/questions-reponses-sur-les-referentiels-relatifs-la-gestion-des-activites-commerciales-et-des)
- [Meta Ad Library](https://www.facebook.com/ads/library/)
- [Google Ads Transparency Center](https://adstransparency.google.com/)
- [Google Ads API](https://developers.google.com/google-ads/api)
- [Meta Marketing API](https://developers.facebook.com/docs/marketing-apis/)
- [Google Tag Manager](https://tagmanager.google.com/)
- [Canva](https://www.canva.com/)
- [Metricool](https://metricool.com/)
- [vidIQ](https://vidiq.com/)

---

## Conclusion

Pour ton activité, je ne chercherais pas à installer les 50 skills disponibles. Je construirais plutôt un système de production reproductible autour de **Frontend Design, Impeccable, Playwright, Lighthouse, axe-core, GSAP, Search Console et Gitleaks**\.

Le gain le plus important viendra de l'association de trois capacités : concevoir des interfaces vraiment distinctives, vérifier automatiquement leur comportement sur téléphone et intégrer le SEO local dès le début. Les connecteurs et outils marketing existants pourront ensuite automatiser la recherche et la communication, sans devenir une dépendance coûteuse.

La limite importante de cette recherche reste le contrôle individuel de tous les projets de ta liste : les dépôts ambigus, les quotas de certains services et plusieurs licences de composants n'ont pas été validés suffisamment pour être déclarés conformes à tes exigences. Ils restent donc signalés comme à vérifier, plutôt que présentés artificiellement comme des outils gratuits, actifs et sûrs.

---

If you want, I can:

- Continue la recherche détaillée pour le design de sites
- Développe la liste d’outils pour photos, images et polices
- Détaille un plan d’utilisation concret des outils recommandés
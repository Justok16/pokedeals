# Sélection d'outils gratuits dans l'annuaire « There's An AI For That » (21/10/2026)

Demande de l'utilisateur (21/10) : aller sur le site cité par le reel Facebook de Gabzer et choisir **tous les outils
gratuits dont DIG16 pourrait avoir besoin**, au maximum.

## Méthode

- **Lecture du site** : theresanaiforthat.com bloque les navigateurs automatiques (vérification Cloudflare). Il a été lu
  avec le connecteur Tavily (offre gratuite de 1 000 crédits par mois, environ 25 utilisés ici).
- **Catégories passées en revue (25)** : page « Free » de l'annuaire, puis sites internet, pages d'atterrissage, référencement, logos,
  détourage, agrandissement d'images, photos de produits, maquettes, palettes de couleurs, réseaux sociaux, montage
  vidéo, sous-titres, transcription, voix, présentations, emails, devis et factures, comptabilité, contrats,
  traduction, service client, réponses aux avis, prospection, QR codes.
- **Volume** : environ 800 fiches. Les publicités (outils présents sur 3 pages ou plus) et les outils sans rapport avec
  la catégorie ont été retirés. Il restait environ 140 outils gratuits ou « freemium ».
- **Vérification à la source** : 20 outils prometteurs ont été vérifiés sur leur propre site le 21/10 (offre gratuite
  réelle, filigrane, compte exigé, où vont les fichiers).
- **Règles appliquées** : budget 0 €, aucune carte bancaire, pas de compte à créer au nom de l'utilisateur sans son
  accord, pas de fichier de prospect ou de client envoyé à un service inconnu.

Constat général : la plupart des outils « Free + from … » sont des **essais déguisés** (quelques crédits, filigrane, ou
téléchargement payant). Beaucoup font aussi ce que Claude fait déjà.

## ✅ Retenus (gratuits pour de vrai, vérifiés le 21/10/2026)

| Outil | À quoi il sert pour DIG16 | Ce qui a été vérifié sur le site officiel |
|---|---|---|
| **free.upscaler.video** (Free AI Video & Image Upscaler) | Rendre nettes les photos ou vidéos floues d'un client (règle : photos et logo du client d'abord) | « completely free and open source », « no signups », traitement dans le navigateur (projet libre WebSR, Real-ESRGAN) |
| **colorfor.ai** | Tirer une palette de la couleur du logo d'un client et **vérifier les contrastes** (lisibilité, accessibilité WCAG) avant mise en ligne | « free, no sign-up, no tracking », « No paywall. No tier called Pro », tout se passe dans le navigateur |
| **Text Behind Image** (makeitaquote.ai/text-behind-image) | Visuels de réseaux sociaux : texte placé derrière le sujet d'une vraie photo (réalisation, portrait de l'utilisateur) | « free, in your browser », « Your photo never leaves your device », export PNG en taille d'origine |

## ✅ Ajoutés le 21/10 au soir (consigne de l'utilisateur : « même s'il y a des outils similaires […], prends-les quand même s'ils permettent d'améliorer l'entreprise »)

Les outils écartés comme « doublons » ont été réexaminés. Sont gardés ceux qui apportent un vrai plus, vérifiés à la source le 21/10.

| Outil | Le plus pour DIG16 | Gratuité vérifiée | Qui fait quoi |
|---|---|---|---|
| **Postnify** (postnify.com) | **Publie aussi sur X automatiquement** (X se fait aujourd'hui à la main) et ajoute 15 publications par mois, hors quota Metricool (20 par mois, déjà dépassé en novembre). API incluse en gratuit : Claude pourra programmer lui-même. | Page tarifs : « Free Forever $0/mo », 2 réseaux, 15 publications par mois, API ✓ | **Utilisateur** : créer le compte avec contact@dig16.fr et relier X et un 2e réseau (règle `63` : chaque réseau exige le titulaire). **Claude** : clé API en variable d'environnement, puis programmation. Parcours à vérifier sur l'aide officielle avant de le lui donner. |
| **Purgebg** (purgebg.com) | Détourage **depuis le téléphone de l'utilisateur**, sans rien envoyer sur un serveur (notre `backgroundremover` ne tourne que dans la session de Claude) | « Try your first image free — no sign-up » ; ensuite compte : 5 crédits + 1 détourage rapide gratuit par jour ; « Your images stay on your device » | Utilisateur, au besoin |
| **ReviewReply** (reviewreply.pages.dev) | Outil à **conseiller aux clients** (formule Visibilité) pour répondre vite et bien à leurs avis Google, même sans nous. Les clients répondent rarement aux avis négatifs : selon une étude citée par le site (UENI, 2026, non vérifiée), seuls 9,8 % des avis à une étoile reçoivent une réponse. | « Free, no signup » | Client. Règle : ne coller que le texte de l'avis, sans le nom de la personne |
| **WebAnatomy** (webanatomy.ai) | Avis extérieur gratuit sur la page d'accueil de dig16.fr : 3 pistes pour transformer plus de visiteurs en demandes de démo | Page tarifs : « Your first 3 opportunities are free and delivered by email » | Claude lance l'analyse si l'utilisateur accepte de donner contact@dig16.fr ; chaque piste est vérifiée avec `test_pages.py` avant tout changement |
| **TrustGrowth** (trustgrowth.ai) | Audit automatique et suivi gratuit d'un site (80 contrôles, 27 critères de confiance E-E-A-T, vitesse) : dig16.fr surveillé chaque semaine | Offre gratuite : « 1 site », « Audit on Autopilot — GSC-verified » | **Utilisateur** : créer le compte et relier la Search Console (son compte Google). Claude lit ensuite les rapports. Leurs skills libres « Groundcrew » sont annoncés, mais le dépôt n'a pas été trouvé le 21/10. |
| **ProspectFlow** (prospectflow.dev) | **Test sur 3 vrais prospects** : comparer son rapport (avis, site, réseaux, concurrents, « points faibles ») avec nos fiches d'appel, et reprendre ce qui est mieux | « The free plan includes 3 lifetime prospect researches » | Utilisateur : créer le compte ; Claude choisit 3 prospects de priorité 1 et compare. Données publiques d'entreprises seulement (B2B). |

## ⏳ En réserve (gratuits mais limités, ou doublon de ce qu'on a)

| Outil | Pourquoi en réserve |
|---|---|
| **Simple Analytics** | Gratuit pour 5 sites, sans cookie, hébergé en Europe, mais **badge obligatoire** et 30 jours d'historique : pas adapté aux sites clients (on a déjà notre mesure maison). |
| **AltTextLab** | 25 images par mois gratuites ; Claude écrit déjà les textes alternatifs. |

## ⚠️ À ne pas utiliser sans précaution

- **Website Auditor.io** : l'audit gratuit annonce une vérification de visibilité dans ChatGPT, Claude et Gemini. Mais
  son formulaire (lu le 21/10) active aussi des **tests de formulaires et des tests « chaos »** (`run_forms`,
  `run_chaos`, `chaos_intensity=medium`, jusqu'à 100 pages). Il pourrait envoyer de faux messages par le formulaire
  d'un site et le charger.
  - **Jamais sur le site d'un prospect ou d'un client** (cela reviendrait à faire tester son site sans son accord).
  - Sur dig16.fr seulement après lecture de leurs conditions. Le lancement a été tenté puis abandonné, faute de vérification.

## ❌ Écartés (et pourquoi)

- **Payant en pratique** :
  - SnapSubtitles (téléchargement payant) ;
  - Auto Caption et Free Image Generator (filigrane en gratuit) ;
  - Spokk (essai de 14 jours puis 149 $/mois) ;
  - Agentkit (50 messages par mois).
- **Déjà couvert, et mieux, gratuitement** :
  - PPT Maker : on fait nos propres présentations ;
  - FreeOCR : Claude lit les images, et FreeOCR envoie les fichiers à des services d'IA ;
  - outils de traduction, d'emails et de rédaction : Claude ;
  - transcription : faster-whisper en local.
- **Hors sujet** :
  - contrats, factures et impôts : outils américains, droit et fiscalité français différents ;
  - photos de produits, Amazon : pas de vente en ligne ;
  - prospection LinkedIn : abandonnée le 10/10.
- **Mini-outils de l'annuaire lui-même** (détourage, traduction, transcription) : connexion Google obligatoire, donc
  compte de l'utilisateur.

## Suite

- Les trois outils retenus sont ajoutés à `connaissances/boite-a-outils.md`.
- À chaque nouveau besoin, chercher d'abord dans nos outils, puis dans cet annuaire (lu par Tavily). La gratuité se vérifie
  toujours sur le site de l'outil.

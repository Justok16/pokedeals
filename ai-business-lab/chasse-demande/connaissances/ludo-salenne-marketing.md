# Synthèse : playlist « Le Marketing Digital facile » (Ludo Salenne) — appliquée à DIG16

Playlist envoyée par l'utilisateur le 15/10/2026 :
https://www.youtube.com/playlist?list=PL0bL4dUOQP3bvsZYyRMR_KzRkGMvT-3PB (27 vidéos, dont deux formations de
1 h 29 et 1 h 46). Chaque vidéo est résumée dans `videos-resumes/<identifiant>.md` (Gemini, modèles gratuits,
15/10/2026). L'auteur dirige une agence de marketing (SLN) et vend des formations : ses chiffres (trafic, taux de
conversion, budgets) sont **affirmés par l'auteur**, non vérifiés. Beaucoup de vidéos visent des PME avec équipe
commerciale et outils payants (HubSpot, Semrush, publicité) : on ne garde que ce qui sert un artisan seul, sans budget.

## 1. Les idées qui reviennent dans toute la playlist

1. **Le client avant tout (persona)** : on ne devine pas son client, on l'interroge (5 à 10 entretiens réels, une
   vraie conversation, pas un questionnaire), puis on écrit 1 à 3 portraits types avec ses mots à lui.
2. **Le parcours d'achat en 3 temps** : le client a un problème → il compare des solutions → il décide. À chaque
   étape, un contenu différent ; on ne propose un rendez-vous qu'à quelqu'un qui est en phase de décision.
3. **Parler du problème et du bénéfice, pas des caractéristiques** (« technique Mario ») : appuyer sur la douleur,
   faire voir le soulagement, puis inviter à agir.
4. **Une page qui convertit** : titre + sous-titre + visuel + formulaire en haut ; détail de l'offre ; preuves
   (témoignages de profils semblables) ; formulaire court (4 à 6 champs) ; page de remerciement qui propose une suite.
5. **Le référencement local de base** : site rapide (moins de 3 s), sécurisé, adapté au téléphone ; titres avec les
   **mots que tapent vraiment les clients** (souvent différents du jargon du métier) ; quelques liens d'autres sites
   (« recommandations ») ; améliorer d'abord les pages qui sont déjà proches de la première page (Search Console).
6. **Réseaux sociaux** : 2 ou 3 réseaux au plus, là où est le client ; formats natifs ; répondre aux commentaires.
7. **Aimant à contacts** (« lead magnet ») : un outil ou un contenu gratuit utile contre un contact.
8. **Positionnement tranché** : dire pour qui on travaille… et pour qui on ne travaille pas.
9. **Copywriting** : structure AIDA (attention, intérêt, désir, action), phrases courtes, lever les objections dans
   le texte, preuve sociale.
10. **Avec l'IA (ChatGPT dans ses vidéos)** : découper (titre → plan → chaque partie), donner le contexte du persona,
    toujours relire et corriger avant de publier.

## 2. Ce que DIG16 fait déjà (vérifié le 15/10)

| Idée | Où c'est déjà en place |
|---|---|
| Interroger les clients avant de construire | `57-entretiens-etude-de-marche.md` (priorité n° 1 depuis le 05/10) |
| Parler du résultat, pas de la technique | site : « Page d'accueil refaite gratuitement », « en ligne en 7 jours », « à votre nom » ; antisèche |
| Page qui convertit | accueil : promesse + bouton en haut, offres, questions fréquentes, formulaire de **6 champs** (dont 2 facultatifs/menus), barre « Appeler / Démo gratuite » sur téléphone |
| Aimant à contacts | **le test du pouce** (outil gratuit) et la démo gratuite |
| Référencement technique | site rapide (polices et images optimisées, CLS ≈ 0), HTTPS, adapté au téléphone, Search Console et Bing branchés, sitemap, IndexNow |
| Lever les objections | antisèche de 55 réponses (`outils/prospects/antiseche.py`) et FAQ du site |
| Positionnement tranché | artisans et commerçants de Charente, secteurs exclus (CLAUDE.md), 15 clients maximum la 1re année |
| Formats natifs, réseaux limités | vidéos publiées en natif (Reels) par Metricool ; réseaux en pause jusqu'au 1er client (05/10) |
| Relire tout texte produit par l'IA | contrôle qualité `44` + skill `humanizer` |

## 3. Appliqué le 15/10/2026

1. **Page de remerciement du formulaire** (accueil) : après l'envoi, le message propose maintenant une suite :
   « En attendant, faites le test du pouce : vos clients vous trouvent-ils et vous appellent-ils du bout du
   pouce ? » (lien vers l'outil). Testé sur téléphone (envoi simulé).
2. **Guide d'entretien `57`** : question bonus « Si vous cherchiez un artisan comme vous sur votre téléphone, vous
   taperiez quoi ? » (les vrais mots-clés pour les titres des sites clients) ; conseils de conduite (conversation et
   relances, écouter, chercher le déclencheur, ne jamais enregistrer sans accord, portraits types écrits après 5 à
   10 entretiens avec les mots réels, bilan des « oui » et des « non »).

## 4. À faire plus tard (quand il y aura de la matière réelle)

| Idée | Condition pour le faire |
|---|---|
| Portraits types (personas) DIG16 | après 5 à 10 entretiens réels (`57`) ; jamais inventés |
| Témoignages sur le site (preuve sociale) | seulement de vrais clients, avec leur accord écrit |
| Améliorer les pages proches de la 1re page Google | dès que la Search Console affiche des impressions (0 le 13/10) |
| Pages « métier + commune » pour les sites clients | à partir des mots notés pendant les entretiens |
| Publier les liens en premier commentaire plutôt que dans le texte (portée Facebook) | affirmation de l'auteur, à tester sur quelques publications quand les réseaux reprendront |

## 5. Écarté (et pourquoi)

- Publicité payante (Google Ads, Facebook Ads, LinkedIn Ads), achat de fichiers de contacts, influenceurs : budget 0 €
  et démarchage encadré (`35`).
- HubSpot, Semrush, Ahrefs, Yooda, notation automatique des prospects (« lead scoring »), séquences d'e-mails
  automatiques : outils payants et pensés pour des équipes commerciales ; à notre échelle (15 clients la 1re année),
  la liste privée et le suivi à la main suffisent.
- LinkedIn : abandonné le 10/10 (décision de l'utilisateur).
- Blog avec un article par semaine : pas maintenant (toute construction se justifie par une demande d'artisan).
- VPN et réglages américains pour tester les nouveautés de Google : sans intérêt.
- Budget marketing de 15 à 25 % du chiffre d'affaires : affirmation de l'auteur pour des entreprises établies, pas
  pour un démarrage à 0 €.

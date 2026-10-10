# 59 — Sites « immersifs » (défilement qui fait avancer un film) : étude et méthode DIG16

Créé le 07/10/2026 à la demande de l'utilisateur : « je veux que mes sites internet puissent ressembler à ça,
étudie cette vidéo au maximum » (vidéo [flL6i2L2Oks](https://youtu.be/flL6i2L2Oks), Zeyneb Madi).

## 1. Ce que montre la vidéo (analyse image par image, relais Gemini en mode « design », 3 tranches de 10 min)

- **Le site** : « Villa Solenne », bien fictif d'une agence fictive (« Maison Varenne »). La visite se fait pièce par
  pièce **au défilement** : la vidéo avance et recule sous la molette. Les 9 pièces sont, dans l'ordre : façade,
  hall, bibliothèque, salon, cuisine, terrasse et piscine, suite, spa, toit.
- **Éléments visibles** :
  - en bas à gauche, un petit plan du niveau (rez-de-chaussée, étage, toit) qui indique la position ;
  - des points cliquables posés sur l'image, qui ouvrent un détail ;
  - un compteur « pièces visitées / détails découverts », comme dans un jeu ;
  - ensuite : fiche technique, carte et temps de trajet, équipe de l'agence, biens similaires, formulaire de
    visite, pied de page.
- **Style** :
  - typographie à empattements de style « luxe », menus fins ;
  - couleurs pierre, sable et bois ;
  - cartes semi-transparentes floutées, coins légèrement arrondis.
- **Fabrication** :
  - Claude Code et le skill gratuit **scroll-craft** (github.com/nateherkai/scroll-craft, licence MIT, lu en
    entier le 07/10) ;
  - images et vidéos **générées par IA avec Higgsfield (payant)** ;
  - site Vite, mis en ligne chez **Hostinger (payant)** ;
  - coût des jetons et des générations affiché à l'écran : environ 44,57 €.
- **Limites visibles** : quelques animations ratées au premier essai, et le coût des générations qui s'ajoute à
  chaque nouvel essai.

## 2. Le skill scroll-craft (ce qu'on en retient)

- **Un moteur sans dépendance** (`scrollcraft.js` + `.css`) :
  - on écrit du vrai HTML, le moteur lit des attributs `data-sc-*` ;
  - on ne modifie jamais le moteur ; on le règle avec 6 couleurs et 2 polices ;
  - vérifié : sa seule requête réseau charge la vidéo du site lui-même.
- **Neuf « dispositifs »** :
  - `scrub` : le film suit le défilement ;
  - `pin` : le cadre tient pendant que le texte avance ;
  - `pan` : un travelling latéral ;
  - `reveal`, `kinetic`, `parallax`, `count`, `flow`, `drift`, et les effets liés au pointeur.
  - Règles : au moins 4 dispositifs différents, jamais deux fois le même d'affilée, au plus 2 films par page.
- **Règles de qualité utiles** :
  - un seul « moment fort » par page, et une fin qui tient au lieu de s'effacer ;
  - aucun chiffre inventé ;
  - pas de flèche « faites défiler », pas de compteur « 01/06 » ;
  - contraste mesuré, version téléphone pensée à part, mode « mouvements réduits ».
- **Coût** : le skill dit lui-même que **construire à partir des vraies photos et vidéos du client est gratuit**.
  Seule la génération d'images (kie.ai) est payante.

## 3. Notre version gratuite (démo `site-dig/demos/menuisier-visite/`, 07/10)

- **Le film** :
  - `outils/film_photos.py` compose un plan-séquence à partir de photos fixes : poussées et travellings
    sous-pixel, fondus de 0,7 s. Il n'y a ni IA payante ni tremblement (contrairement au filtre `zoompan`
    de FFmpeg) ;
  - le film est encodé « pour le défilement », avec une image clé toutes les 6 images ;
  - poids : ordinateur 5,4 Mo (MP4) ; téléphone 2,8 Mo (MP4, cadrage vertical à part) ;
  - une version WebM se charge seulement dans les navigateurs sans lecteur MP4.
- **Le parcours** :
  1. Visite de l'atelier : 1 film, 5 légendes synchronisées sur le film lui-même, petit plan des étapes cliquable.
  2. « Regardez de près » : 4 points à toucher sur une photo, avec un compteur des détails découverts. C'est
     l'interaction propre à cette démo. Sur téléphone, le détail s'affiche sous la photo pour ne jamais cacher les
     autres points.
  3. « Ce que nous fabriquons » en travelling latéral.
  4. Les 3 étapes avec le cadre fixe.
  5. La fin qui tient : un seul geste, « Demander un devis ».
- **Contrôle** (Chromium, à 1440 × 900 et 390 × 844, et en mouvements réduits) :
  - aucune erreur ;
  - aucun débordement horizontal ;
  - film et légendes synchronisés à chaque position ;
  - en mouvements réduits, la visite devient 5 photos légendées, sans écran figé.
- **Optimisé après l'audit Lighthouse** (téléphone) :
  - images en WebP, en deux tailles (640 et 1200 px) ;
  - moteur minifié (`scrollcraft.min.js`, 21 Ko) avec sa licence MIT jointe (`LICENCE-scrollcraft.txt`) ;
  - polices chargées sans bloquer l'affichage ;
  - noms accessibles pour les boutons du plan.
  - Sur tout le site, ajout de `robots.txt` (il manquait : l'accueil était renvoyé à sa place) et d'une vraie
    page 404.
- **Sécurité** : `_headers` autorise désormais `media-src 'self' blob:`, parce que le moteur charge la vidéo en
  mémoire pour pouvoir la parcourir.
- **À vérifier sur un vrai téléphone** :
  - un navigateur sans écran ne reproduit pas Safari iPhone (décodeur vidéo, mode économie d'énergie) ;
  - à contrôler par l'utilisateur sur son téléphone avant toute présentation à un client.

## 4. Pour un client (quand il y en aura)

- **Matière** : ses vraies photos, ou mieux, **une vidéo de 30 s filmée au téléphone** en marchant dans l'atelier
  ou sur un chantier. Le film devient alors une vraie visite (règle des démos : photos du prospect d'abord, et
  accord préalable avant de s'en servir).
- **Coût** : 0 € (Cloudflare Pages, aucune génération payante). Hostinger, Higgsfield et Vite sont inutiles pour
  nous.
- **Offre** : réservée à la formule Prestige (page conservée, jamais proposée en prospection, décision du 05/10),
  ou sur demande d'un artisan. Les prix ne changent pas sans décision de l'utilisateur.

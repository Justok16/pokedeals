# Flyer A5 et prompt pour comparer avec d'autres IA (26/09/2026)

- Flyer Claude : `supports/flyer-dig-a5.html` (A5 recto seul, 148 × 210 mm, QR code vers la démo ;
  version 2 du 26/09 : l'utilisateur a jugé la v1 bicolore trop simple et le verso peu lu). PDF prêt à imprimer, généré à partir de ce fichier.
- À compléter avant impression : téléphone, email, prénom et nom, SIREN,
  adresse (après création de la micro-entreprise). Prix à valider.
- Impression : prévoir 3 mm de fond perdu si l'imprimeur le demande.

## Prompt à copier dans une autre IA (ChatGPT, Gemini, Canva, etc.)

Voir le texte exact dans la réponse du 26/09 ; version de référence :

> Crée un flyer publicitaire A5 portrait (148 × 210 mm), **recto seul**,
> prêt à imprimer, ultra moderne et très accrocheur, pour « DIG16 », un
> créateur indépendant de sites internet pour artisans, commerçants et
> indépendants en zone rurale en France.
> Cible : patrons de très petites entreprises (plombiers, maçons, garages,
> coiffeurs, restaurants, gîtes…), 35-65 ans, pressés, méfiants envers les
> contrats longs ; beaucoup ont un vieux site loué ou pas de site.
> Tout doit tenir sur une seule face et se comprendre en 5 secondes.
> Contenu : titre « Vos clients vous cherchent sur leur téléphone. Ils vous
> trouvent ? » ; sous-titre « Un site moderne, rapide, qui vous appartient.
> Fait près de chez vous, sans contrat qui vous enferme. » ; 4 avantages
> avec icônes (plus d'appels et de devis ; votre site vous appartient, site
> et nom de domaine à votre nom ; en ligne en 7 jours, 20 min ensemble ;
> suivi chaque mois, mises à jour sous 48 h) ; un visuel fort : un
> smartphone qui affiche un beau site d'artisan avec une notification
> « Nouvelle demande de devis ! » ; un encadré offre très visible « Votre
> page d'accueil refaite gratuitement, avant de décider », « dès 29 €/mois
> · 0 € de création · 6 mois puis sans engagement », avec un QR code et
> [téléphone] · [email].
> Style : premium, coloré et vivant (dégradés profonds bleu nuit, violet,
> orange, vert émeraude), titres en serif élégante et épaisse, texte
> sans-serif lisible, effets de verre dépoli, ombres douces, beaucoup de
> contraste. Pas d'aspect « bon marché », pas de clipart.
> Mentions légales en petit en bas : « DIG16 — [Prénom Nom], entrepreneur
> individuel (EI) — SIREN [à compléter] — [adresse]. TVA non applicable,
> art. 293 B du CGI. Offre Essentiel : site 5 pages, hébergement, 1
> modification/mois ; engagement minimal 6 mois. Démo sans obligation
> d'achat. Visuel d'illustration. Ne pas jeter sur la voie publique. »
> Interdits : citer ou critiquer un concurrent, faux avis, résultats
> chiffrés inventés.
> Livre : le flyer en PDF ou image haute définition (300 dpi, 3 mm de fond
> perdu), puis 3 variantes de titre.

## Version 3 (26/09) : Canva

- Essai 1 avec l'ancien outil Canva (`generate-design`) : 4 propositions
  inutilisables (textes incompréhensibles, fausses dates, format paysage).
- Essai 2 avec `create-design`, format « Flyer (Portrait A5) » et textes
  imposés : **réussi** (photo réaliste, icônes, textes corrects). Design
  dans le compte Canva de l'utilisateur (« DAHWQBvgVuI »), modifiable.
- QR code ajouté par Claude dans le cadre vide (vérifié : il mène à la
  démo), export 300 dpi (1748 × 2480 px).
- Reste à faire dans Canva : téléphone, email, nom, SIREN ; remplacer le
  lien du QR code par la démo définitive.
- 26/09, v3.1 après validation des prix : « dès 29 € », « trouvent ? »,
  « EI » (Canva avait écrit « El »), mention « nom de domaine à la charge
  du client » ; modifications enregistrées dans le design Canva.

## Comparaison avec les autres IA (26/09) — fichiers dans `supports/concurrence/`

| IA | Bonnes idées | Défauts relevés |
|---|---|---|
| Grok | Logo en pastille « D », étiquette de cible, avantages avec phrase, bloc offre à pastilles | QR décoratif illisible ; « contact@dig.fr » (domaine déjà pris par un tiers) ; entreprise fictive dans une vraie ville ; faux numéro ; 49 € |
| ChatGPT | Vrai site d'artisan dans le téléphone ; « Simple, humain, sans vous compliquer la vie » | Logo qui chevauche le texte ; bloc offre coupé par le téléphone ; grand vide ; QR = texte, pas de lien |
| Mistral | Pastilles « Fait près de chez vous » et « Offre découverte » ; « appelez ou scannez, la démo est gratuite » | Logo qui chevauche ; QR factice ; icônes cassées ; écran vide |
| Gemini | Bandeau « Spécial artisans… ruraux » ; bloc contact étiqueté ; 3 variantes de titre | Fond coupé net à mi-hauteur ; écran presque vide ; faux avis « 4,9/5 – 38 avis » et faux numéro dans la maquette ; QR illisible ; 49 € |
| Claude (Canva) | Photo réaliste, seul QR fonctionnel, prix et mentions à jour | Moins d'explications sous les avantages, pas de logo |

Variantes de titre retenues (Gemini) : « Artisan, commerçant : vos clients cherchent
sur internet. Êtes-vous visible ? » ; « Transformez les recherches sur smartphone
en vrais devis et chantiers locaux. » Écartée : « Marre des sites payés une
fortune ou bloqués ? » (dénigrement implicite des concurrents).

## Version 4 (26/09) — la synthèse, validée par l'utilisateur (« vas-y pour la v4 »)

- Design Canva « DAHWQH2QKK8 » (modifiable par l'utilisateur) ; fichiers
  `supports/flyer-dig-a5-v4.pdf` et `.png` (1748 × 2480 px, 300 dpi).
- Reprend : mise en page et logo « D » (Grok), textes et bloc contact
  (Gemini), site dans le téléphone (ChatGPT), pastilles « Fait près de chez
  vous » et « Offre découverte » + « Appelez ou scannez » (Mistral), photo,
  prix 29 € et mentions (Claude).
- Corrigé après génération : « E1 » → « EI » ; QR code réel envoyé dans
  Canva (vérifié : il ouvre la démo).
- À compléter après création : téléphone, email, prénom et nom, SIREN,
  adresse ; lien du QR vers la démo définitive.


## Correction du 26/09 (soir)

- L'ancien QR code menait à `dig-demo-menuisier.vercel.app`, projet Vercel supprimé : il ne fonctionnait plus.
- Remplacé dans Canva (design « DAHWQH2QKK8 ») par un QR vers **https://digsite.pages.dev/** (`site-dig/qr-digsite.png`) ; vérifié en décodant l'export 1748 × 2480 px. PNG et PDF du flyer mis à jour dans `supports/`.

## Parrainage (28/09)

- Ajout validé par l'utilisateur (« ok flyer ») : « Recommandé par un client ? 1er mois offert. »
  sous « Appelez ou scannez », dans l'élément texte d'origine (même police), 10 pt, interligne 1,05.
- Contrôle : QR décodé → https://digsite.pages.dev/ ; écart mesuré entre la dernière ligne et le
  bord du bloc ≈ 1,7 mm, aucun chevauchement avec l'icône email. PNG 1748 × 2480 et PDF A5 mis à jour.

## Version 5 (28/09/2026, après l'audit externe)

- Fichier de référence : `supports/flyer-dig-a5.html` → `supports/flyer-dig-a5-v5.pdf` et `.png`.
- « Plus d'appels et de devis » (promesse de résultat) remplacé par « Facile à appeler » ; note
  fictive « 4,9/5 » retirée de l'image d'exemple ; « premier mois réglé avant la mise en ligne »
  ajouté aux mentions ; prix « dès 49 €/mois ».
- **QR code refait** : la source HTML menait encore à l'ancienne démo supprimée (erreur 404).
  Nouveau QR vers https://digsite.pages.dev/, décodé depuis le PDF lui-même, y compris à basse
  résolution. Contrôle ajouté : tous les QR et liens des PDF et du site testés (35 liens).
- Anciennes versions retirées du dossier (v4 : « dès 29 € » ; export Canva : QR mort). Le
  design Canva DAHWQH2QKK8 n'est plus la référence.
- Reste avant impression : prénom, nom, SIREN, adresse, téléphone et email (après immatriculation).

- 28/09 (soir) : PDF refait à partir d'une image 300 ppp (1 748 × 2 480 px, A5 exact) après une capture de l'utilisateur montrant des rectangles sombres et un titre tronqué dans sa visionneuse ; contrôlé avec pdfium et MuPDF, QR décodé.

## Flyer de référence : Canva (28/09/2026, soir) — choix de l'utilisateur (« bien plus beau »)

- Design Canva DAHWQH2QKK8, exports `supports/Dig-Flyer-A5.pdf` (A5 exact) et `.png` (300 ppp).
- Corrections : « dès 49 € » ; « Facile à appeler / Pensé d’abord pour le téléphone » (plus de
  promesse de résultat) ; « Modifications sous 48 h, bilan mensuel » ; « Premier mois offert »
  (parrainage) ; mentions légales avec « premier mois réglé avant la mise en ligne » ;
  apostrophes typographiques ; titres des cartes harmonisés (même taille, une ligne) ;
  coupures de lignes volontaires ; encadré de l'offre ajusté.
- Contrôle : texte extrait (aucune trace de 29 €, promesse, note fictive), QR décodé depuis le
  PDF à 300 et 72 ppp → https://digsite.pages.dev/, rendu identique pdfium / MuPDF, marges :
  3,2 mm en bas, 6,3 mm à gauche et à droite (zone de sécurité d'imprimeur ≈ 3 mm).
- Le flyer HTML (`flyer-dig-a5.html`, v5) reste une solution de secours.
- Avant impression : prénom, nom, SIREN, adresse, téléphone, email (après immatriculation) ;
  demander à l'imprimeur s'il veut un fond perdu (Canva : « Fond perdu » à l'export).

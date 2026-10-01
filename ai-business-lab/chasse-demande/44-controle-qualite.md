# Contrôle qualité obligatoire avant tout envoi (règle du 26/09)

Exigence de l'utilisateur : « tous les documents que tu fabriques et que tu
me présentes [doivent être] irréprochables, aussi bien sur le fond que sur la
forme ». Rien n'est envoyé tant que chaque case applicable n'est pas cochée.

## Fond
- [ ] Chaque fait, chiffre, prix, délai est vérifié à la source (ou marqué « à vérifier »).
- [ ] Cohérence entre documents : prix (29/49/79 €, 690 €), « en ligne en 7 jours »,
      « 6 mois puis sans engagement », « mises à jour sous 48 h », nom de domaine
      à la charge du client, adresse du site (https://digsite.pages.dev/).
- [ ] Aucun faux avis, aucune promesse de résultat Google, aucune donnée privée
      dans un document public.
- [ ] Orthographe, accents, typographie française (espaces avant « : ; ? ! »).
- [ ] Le contenu correspond au métier / au destinataire (pas de texte d'artisan
      sur un restaurant, pas de paragraphe répété).

## Forme
- [ ] Rendu regardé en image, en entier, à la bonne taille (pas seulement un aperçu).
- [ ] Alignements mesurés au pixel : texte centré dans ses boutons et pastilles,
      éléments centrés dans leurs cadres (écart ≤ 1 px à l'export haute définition).
- [ ] Aucun chevauchement (boutons, barres fixes, textes) à toutes les tailles
      d'écran : 320, 360, 390, 414, 768, 1024, 1440 px, et à plusieurs hauteurs de défilement.
- [ ] Contraste et lisibilité : texte lisible sur photo, taille suffisante sur téléphone.
- [ ] Liens et QR codes testés (QR décodé sur l'export, lien qui répond 200).
- [ ] Polices chargées, images affichées, pas de débordement horizontal.
- [ ] PDF : chaque page regardée en entier (planche de toutes les pages) ; aucun
      titre seul en bas de page, aucune page presque vide, aucun numéro de
      téléphone ou mot composé coupé en fin de ligne, pas de mot seul sur la
      dernière ligne d'un grand titre.
- [ ] Pas de texte en dégradé (« background-clip:text ») dans un PDF : Chromium
      peut dessiner un cadre parasite autour ; utiliser une couleur pleine.
- [ ] Pas deux démos avec la même photo principale dans un même livret.
- [ ] Photos nettes, mesurées avec `outils/nettete.py` : taille au moins égale à la
      surface affichée × densité de l'écran (jusqu'à ×3 sur téléphone) ; photo de fond en version haute pour téléphone et large pour
      ordinateur ; vérifiées en gros plan, pas seulement en miniature.
- [ ] Animations : vérifiées à 0, 25, 50, 75 et 100 % de leur durée.
- [ ] Lisibilité mesurée (`outils/lisibilite.py`) : aucun texte sous 13 px ni en
      graisse fine (< 400) ; contraste ≥ 4,5 (≥ 3 au-delà de 24 px) ; ombre portée
      sous tout texte posé sur une photo. Menu vérifié sur une seule ligne de
      320 à 1 440 px.
- [ ] Pas de look « fait par IA » (`outils/anti_generique.py`, règles tirées de Taste Skill) :
      pas de numéros de section décoratifs, d'étapes « Étape 1 », d'invitation à défiler, de verbes
      creux, de noms bidon, d'images de remplissage ; « attention » à examiner (3 colonnes égales,
      chiffres trop ronds, noir pur).

## Outils
- Accessibilité et ergonomie (depuis le 28/09) : `outils/audit_acces.py page.html …` doit afficher « problèmes : 0 » (boutons et liens d'au moins 44 px sur téléphone, champs de formulaire avec étiquette, titres dans l'ordre, variante « réduire les animations », attribut lang, images avec alt).
- PDF à effets visuels (dégradés, transparences, texte en dégradé) — leçon du 28/09 : la visionneuse du téléphone de l'utilisateur affichait des rectangles sombres et masquait « Ils vous trouvent ? » sur le flyer. Règle : ces PDF (flyer, visuels) sont produits à partir d'une image à 300 ppp (format exact, QR décodé depuis le PDF), et tout PDF est contrôlé avec DEUX moteurs d'affichage (pdfium et MuPDF) avant envoi.
- Photos (depuis le 28/09) : `python3 outils/verif_metadonnees.py <dossier>` sur toute photo avant mise en ligne ; aucune position GPS ni donnée d'appareil ne doit rester (`--nettoyer` les retire).
- Second avis (depuis le 28/09) : document important relu aussi par Gemini en lecture seule (`/api/avis`, voir `33-outils.md`) ; chaque remarque est vérifiée avant d'être appliquée.
- Sécurité (depuis le 28/09) : skill `vibe-security` (`.claude/skills/vibe-security`) passé sur tout code nouveau (relais, formulaires, paiement) ; aucune clé, jeton ou adresse personnelle dans le dépôt ; en-têtes de sécurité du site dans `site-dig/_headers` (tester qu'aucune page n'est bloquée). Le jour où un formulaire envoie vraiment des données : limite d'envois (anti-spam) et vérification côté serveur.
- Démos : `outils/prospects/verif_maquettes.py`, `qa_maquettes.py`, captures d'écran relues une par une.
- Flyer / visuels Canva : export 1748 × 2480 px, mesure des marges et décodage du QR
  (`outils/prospects/controle_flyer.py`).

- Démos personnalisées de prospects (depuis le 28/09, audit externe n° 1) : **jamais publiées en ligne** sans accord écrit du prospect ; montrées sur écran ou en PDF privé, supprimées en cas de refus. Les démos publiques du site utilisent uniquement des entreprises fictives.

## Doublons entre listes de prospects (leçon du 30/09/2026)

Erreur constatée : les ajouts n°12 et 13 reprenaient 23 artisans déjà présents dans les ajouts
n°4 et 5, car le registre anti-doublons avait été construit sans ces deux listes. Règles depuis :
1. Le registre des prospects est **reconstruit à partir de toutes les listes publiées** (fichiers
   HTML) avant chaque nouvel ajout, jamais tenu à la main.
2. Contrôle sur **chaque** numéro d'une fiche (une fiche peut en avoir deux) **et** sur le nom
   normalisé (sans points, accents, « SARL », « SAS »…) : « E.E.C.E » = « SARL E.E.C.E ».
3. Un doublon garde son **premier** numéro ; il est retiré de la liste récente, avec une note
   « n° X = n° Y », et les copies Drive périmées sont renommées « ANCIENNE VERSION ».

## « Sans site » : jamais sur la seule détection automatique (leçon du 01/10/2026)

La détection automatique (recherche du nom légal) rate les sites dont le nom de domaine diffère du
nom de l'entreprise (ex. un nom commercial abrégé, un numéro de département ou le métier dans l'adresse) : sur 12
artisans avec salariés marqués « sans site », 9 en avaient un. Règle : chaque prospect est vérifié
par une recherche web « nom + commune » AVANT d'entrer dans une liste ; un domaine trouvé est testé
(il répond ? page réelle et non « domaine à vendre » ?) ; un site mort ou abandonné depuis des années
reste un bon prospect (à noter sur la fiche : « site abandonné »).

Compléments du réaudit du 01/10 (56 fiches contrôlées, 1 retirée) :
- Chercher aussi **l'adresse e-mail** de l'entreprise : un e-mail sur un domaine propre
  révèle un domaine à tester, même si aucune recherche ne montre de site.
- Une **grosse structure** (hébergement, plus de 10 salariés, lieu de réception) a presque toujours
  un site : la tester avec plusieurs noms de domaine probables (nom court, avec ou sans article, .com et .fr).
- Un **domaine en maintenance ou « en construction »** (page d'attente d'hébergeur) n'est pas un
  site : la fiche le précise, c'est même un argument d'appel.
- Avant les recherches web, lancer `outils/prospects/sonder_domaines.py` (noms de domaine probables :
  avec ou sans tiret, .fr/.com, suffixe 16) ; vérifier ensuite l'identité de tout site trouvé
  (adresse, téléphone, mentions légales) : un homonyme d'une autre région n'est pas « son » site.
- Un site sur un outil de création (Wix, Hostinger, WordPress…) compte comme un site, même gratuit ;
  un site gratuit abandonné depuis des années reste un prospect « refonte ».
- Une page générée automatiquement par un concurrent sans l'accord de l'artisan (ex. Artizo,
  « réclamez votre site ») n'est pas son site.
- **Page dans le site d'un groupe** ou **même dirigeant qu'une entreprise qui a un site** : la fiche
  le précise, et l'accroche ne dit jamais « vous n'avez aucun site ».

## Supports à pages A4 fixes : débordement (outil ajouté le 01/10/2026)

Le contrôle pymupdf « texte sur le pied de page » n'a pas vu un tableau qui passait **sous** le pied de
page de la page 8 du guide (le texte coupé n'est plus dans le PDF). Désormais, tout PDF d'un support à
`<section class="page">` est produit par `python3 outils/pdf_pages.py <html> <pdf>` : il mesure, page par
page, le bas de chaque bloc par rapport au haut du pied de page et **refuse d'écrire le PDF** si une page
déborde. Puis regarder l'image de chaque page modifiée.

## Prospects « sans site » : deux contrôles de plus (leçon du 01/10/2026, soir)

Sur 13 candidats RGE annoncés « aucun site » par la détection automatique, **13 avaient en réalité un
site ou étaient à écarter**. Deux erreurs n'auraient été vues ni par le sondage des domaines ni par la
recherche « nom + commune » :
1. **Rechercher le numéro de téléphone sur le web** (entre guillemets) : c'est ce qui a révélé
   `sorc16.fr` (sigle de l'entreprise) et `adigenieclimatique.com` (enseigne différente du nom
   légal). Obligatoire avant de déclarer un prospect « sans site ».
2. **Lire la fiche Pappers** : si elle affiche « s'est opposée à l'utilisation de ses données à des
   fins de prospection », on n'appelle pas (respect du choix de l'entreprise, cadre `35`).
`sonder_domaines.py` teste désormais aussi le sigle et le nom sans mots répétés.

## Orthographe et grammaire (outil ajouté le 01/10/2026)

Avant tout envoi d'un document ou d'une page : `python3 outils/typo_fr.py <fichier>` (espaces
insécables) puis `python3 outils/orthographe.py <fichier>` (LanguageTool hors ligne). Chaque
remarque est relue à la main : l'outil se trompe parfois (accord d'un participe avec un COD placé
avant, noms propres) ; on ne corrige que les vraies fautes.

Améliorations du 01/10 (soir) : le texte des pages HTML est lu **tel que le navigateur l'affiche**
(un mot coupé par une balise n'est plus signalé) ; code, commandes et adresses web sont remplacés par
« Truc » ; les mots à majuscule, chiffre ou « _ » (marques, prénoms, termes techniques) sont écartés.
Ajouter `--noms` pour les voir quand même, et les vérifier à la source. Bilan du premier passage
complet (site Dig, démos, 9 supports) : de 90 à une vingtaine de remarques, aucune vraie faute ;
le reste, ce sont des conseils de style ou des citations en anglais.

## Listes, feuilles et registre : contrôle croisé obligatoire (leçon du 01/10/2026)

La feuille de suivi Drive avait été construite par une lecture des fiches qui, quand une fiche
n'avait pas de lien téléphone, prenait le numéro de la fiche **suivante** et la fusionnait :
4 artisans « sans numéro » affichaient le numéro d'un autre prospect, et 4 prospects (dont une PME de
20 à 49 salariés) manquaient dans la feuille et dans le registre des doublons. Règle : après toute
création ou modification d'une liste, d'une feuille ou du registre, lancer le contrôle croisé
(script `verifier_tout.py` du dossier de travail privé) et n'envoyer qu'à **0 problème** :
- fiches ↔ feuille dans les deux sens : numéro, nom, commune, liste, téléphone ;
- doublons entre listes (même téléphone, même nom) ;
- chaque PDF contient toutes les fiches de sa liste et n'est pas plus ancien qu'elle ;
- chaque fiche figure au registre des doublons ;
- toute copie envoyée sur Drive est retéléchargée et comparée ligne à ligne au fichier contrôlé.
La lecture des fiches se fait **fiche par fiche** (découpage sur le début de chaque fiche), jamais
par une expression qui peut déborder d'une fiche sur la suivante.

## Sécurité irréprochable (exigence de l'utilisateur du 30/09/2026)

Tout site livré (Dig ou client) et toute démo publiée passent, **avant livraison et après chaque
mise en ligne** :
1. `outils/audit_securite.py https://site --proprietaire` → **100/100 exigé** (HTTPS et redirection,
   certificat, HSTS, CSP, anti-clickjacking, nosniff, Referrer-Policy, Permissions-Policy, aucune
   version de logiciel affichée, cookies sécurisés, pas de contenu mixte, scripts tiers avec
   empreinte SRI, formulaires chiffrés, consentement si traceurs, mentions légales, aucun fichier
   sensible exposé, security.txt).
2. Le skill **vibe-security** sur tout code écrit (clés, accès, formulaires, paiements).
3. `outils/audit_acces.py` (accessibilité et règles d'interface) → 0 défaut.
4. Aucune clé ni adresse email dans le code publié ; secrets uniquement dans les réglages de l'hébergeur.
5. **Paiement en ligne ou webhook** (ajout du 01/10, vidéo pZgw2WNOcHE) : tests d'abord en mode
   *sandbox* du prestataire ; **signature de chaque webhook vérifiée côté serveur** (secret dans les
   réglages de l'hébergeur, jamais dans le code) ; fichier `.env.local` exclu de Git ; limite de
   fréquence sur toute fonction qui appelle une IA payante (sinon facture qui explose).
6. Intégration d'un service tiers (paiement, authentification, suivi d'erreurs) : partir de la
   **documentation officielle lue directement**, jamais de mémoire.

**Audits de concurrents : mode PASSIF uniquement** (`audit_securite.py https://site`, sans
`--proprietaire`) : une lecture de la page d'accueil publique, comme n'importe quel visiteur.
Jamais de test d'intrusion, d'URL cachée essayée ni de formulaire envoyé sur un site sans l'accord
écrit de son propriétaire : accéder ou se maintenir frauduleusement dans un système informatique est
puni de 3 ans d'emprisonnement et 100 000 € d'amende (Code pénal, art. 323-1, version en vigueur
depuis le 26/01/2023, lu sur Légifrance le 30/09/2026). Résultats d'audits de concurrents : jamais
publiés ni utilisés pour dénigrer ; seulement pour montrer au prospect, factuellement, ce que Dig
fait mieux.

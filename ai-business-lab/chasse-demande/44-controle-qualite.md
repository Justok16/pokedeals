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

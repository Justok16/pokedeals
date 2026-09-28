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

## Outils
- Accessibilité et ergonomie (depuis le 28/09) : `outils/audit_acces.py page.html …` doit afficher « problèmes : 0 » (boutons et liens d'au moins 44 px sur téléphone, champs de formulaire avec étiquette, titres dans l'ordre, variante « réduire les animations », attribut lang, images avec alt).
- Démos : `outils/prospects/verif_maquettes.py`, `qa_maquettes.py`, captures d'écran relues une par une.
- Flyer / visuels Canva : export 1748 × 2480 px, mesure des marges et décodage du QR
  (`outils/prospects/controle_flyer.py`).

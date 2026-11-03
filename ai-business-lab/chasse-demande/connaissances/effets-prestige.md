# Catalogue des effets « haut de gamme » (sites Prestige et sur-mesure)

Demande de l'utilisateur du 02/11/2026 : « tout ce qui s'anime, qui fait haut de gamme, surtout quand il faudra
personnaliser ou faire du sur-mesure pour les sites Prestige, il faut faire en sorte de garder toutes les bonnes idées ».

**Règle** : toute idée d'animation ou d'effet vue dans une vidéo, un carrousel, une capture ou une veille est ajoutée
ici le jour même (même si l'outil d'origine est écarté, par exemple parce qu'il est en React), avec sa source et la
façon de la refaire chez nous. On l'utilise sur un site Prestige ou sur-mesure, ou ailleurs si elle reste légère.

**Comment on les fait** : HTML/CSS + GSAP 3.15 et ScrollTrigger (déjà hébergés dans `site-dig/moteur/anim/`), Lenis pour le
défilement doux. Les plugins officiels de GSAP (SplitText, ScrambleText, Flip, MorphSVG…) : licence à relire à la source
avant le premier usage. Skills installés : `gsap-core`, `gsap-scrolltrigger`, `gsap-plugins`, `gsap-timeline`,
`gsap-performance`, `review-animations`, `emil-design-eng`.

**Garde-fous (toujours)** :
- consigne du 28/10 : chaque animation visible sur téléphone fonctionne aussi sur PC, y compris quand Windows réduit
  les animations (seuls le zoom et le défilement fluide sont retirés) ; test sur PC avec et sans mouvement réduit ;
- rapidité sur téléphone d'abord (Google tient compte de l'expérience sur la page, aide officielle lue le 02/11) :
  animer seulement `transform` et `opacity`, rien de lourd au premier affichage ;
- sobriété : pas de « signes d'un site fait par l'IA » (`44`, 02/11) : pas de néon, de lueur partout, de faux compteurs,
  de faux témoignages, de logos de partenaires ;
- une seule « signature » forte par page (un effet mémorable), le reste discret ;
- objectif (consigne du 03/11) : dépasser, jamais seulement égaler, toute référence jugée plus belle : plus beau ET plus rapide sur téléphone.

| Effet | Ce que ça donne | Source de l'idée | Comment chez nous | Poids sur téléphone |
|---|---|---|---|---|
| Titre qui se révèle mot par mot ou lettre par lettre | Le titre « s'écrit » à l'arrivée ou au défilement | React Bits, Magic UI, Aceternity (carrousel DfCEyQvCFZK, 02/11) | GSAP (SplitText ou découpage maison en `<span>`) + ScrollTrigger | Faible |
| Texte qui se « brouille » puis se stabilise | Effet machine à écrire / décodage, pour un slogan | React Bits (DfCEyQvCFZK) | GSAP ScrambleText ou petit script | Faible |
| Fond animé doux (dégradé, aurora, grain) | Fond vivant derrière le haut de page | Aceternity, Magic UI (DfCEyQvCFZK) ; Shader Gradient (DeMO5D0AUBq) ; vidéo nkg3cquwKiw | CSS (dégradés animés) d'abord ; shader WebGL seulement en Prestige après test de vitesse | Faible (CSS) à fort (WebGL) |
| Fonds WebGL, 3D, effet « verre » | Objet 3D ou matière en verre qui réagit ; fonds animés en haut de page (vagues, nuages, oiseaux, réseau de points) | React Three Fiber, Liquidglass.js (DeMO5D0AUBq) ; img2threejs (Ddytkf2gBEj) ; vidéo CCUSpJkAfgU ; Vanta.js (reel Ddh2J6Zppgb, 03/11 : MIT d'après npm, mais dernière version en septembre 2022 → s'en inspirer, refaire en Three.js à jour) | Three.js sans React, chargé après le reste de la page | Fort : Prestige seulement |
| Cartes qui s'empilent au défilement | Réalisations ou étapes qui se superposent | Skiper UI, UI Layouts (DfCEyQvCFZK) ; skill `taste-redesign` | CSS `position: sticky` + GSAP | Faible |
| Avant / après avec curseur | Glisser pour voir le chantier avant et après | Déjà fait (démo RG Maçonnerie, 28/10) | En place | Faible |
| Images qui se dévoilent (masque, rideau) | La photo apparaît comme une porte qui s'ouvre | Aceternity, Kokonut UI (DfCEyQvCFZK) | GSAP `clip-path` + ScrollTrigger | Faible |
| Parallaxe légère | Photo et texte avancent à des vitesses différentes | Bibliothèques de la capture du 02/11 | GSAP ScrollTrigger `scrub` | Faible si modéré |
| Bouton « magnétique », carte qui suit le curseur | Le bouton attire la souris, la carte s'incline | Magic UI, Animate UI (02/11) | GSAP `quickTo` ; désactivé au doigt sur téléphone | Faible (PC seulement) |
| Bordure qui s'éclaire sous le curseur | Lumière qui suit la souris sur une carte | Skill `taste-redesign` (« spotlight borders ») | CSS variables + petit script | Faible (PC seulement) |
| Défilement d'un bandeau sans fin | Liste des services ou des communes qui défile | Magic UI (DfCEyQvCFZK) | CSS animation | Faible ; jamais de logos de partenaires |
| Transition entre pages | La page suivante arrive en glissant | Animate UI (02/11) | View Transitions du navigateur ou GSAP Flip | Faible |
| Vidéo pilotée par le défilement | Une vidéo du métier avance quand on descend | Sites « vitrines » ; Huashu Motion (De4lCPQJ2d4, 25/10) | ScrollTrigger + vidéo légère | Moyen |
| Film de lancement de 30 s | Petite vidéo animée de présentation du client | Huashu Motion (De4lCPQJ2d4) ; skill `cbh991/animate` | HTML/GSAP filmé (méthode déjà utilisée pour nos Shorts 3D) | Hors site |
| Effet « waouh » propre au métier | Fonction interactive du métier (essayage d'un motif, simulateur de couleur de façade…) | Reel DepgnIQT9_Q (tatouage) | Petit outil sur-mesure | Variable : Prestige |
| Éléments d'interface tout prêts (boutons, interrupteurs, chargements) | Gain de temps pour un détail | Uiverse (MIT vérifié le 02/11) | Copier l'élément sobre, garder la mention de licence | Faible |

# Chrome Web Store — relevé complet (24/09)

Données primaires : sitemap officiel (43 lots, **366 019 extensions**), page
de chaque extension (en-tête) — outil `outils/chrome_extensions.py`,
~339 000 lues à l'analyse. Les avis individuels ne sont **pas** collectés
(chemin `/reviews` exclu par le robots.txt, respecté).

- 8 381 extensions ≥ 10 000 utilisateurs ; **20 162 avec achats intégrés**.
- Argent concentré en « Workflow & Planning » (3 859 payantes, 129 M
  d'utilisateurs cumulés), « Tools » (9 341), « Privacy & Security ».

## Payantes, très utilisées, mal notées (≥ 50 000 util., ≤ 3,5)

Grands éditeurs (1Password 3,0 ; Smartsheet ; Xodo), VPN, téléchargeurs de
vidéos (conditions d'utilisation de YouTube/Vimeo : point 22), outils
d'abonnés Instagram (point 22), traduction de vidéos YouTube (YouTube double
nativement : point 14). Examinés :

| Extension | Util. | Note | Concurrence mesurée | Verdict |
|---|---|---|---|---|
| **Slides Timer** (minuteur dans Google Slides) | 100 000 | 3,4 (111) | suivant : 4 000 ; ExtPilot gratuit « sans mur payant » ; minuteurs en surimpression et vidéos YouTube gratuits | voir ci-dessous |
| Lightning Autofill | 600 000 | 3,4 | 1 186 extensions de remplissage, dont Magical 4,4 (300 000), Simplify 4,9 (500 000) | Écarté (8) |
| Record Google Meet | 70 000 | 3,5 | enregistrement natif Meet (Workspace payant), Tactiq, Fireflies, Otter… | Écarté (8, 14) |
| Save as PDF | 300 000 | 3,2 | 46 extensions, dont 2 à 4,7 ; impression PDF native du navigateur | Écarté (7, 8) |

## Slides Timer — le cas le plus net, et pourquoi il ne suffit pas

- Quasi-monopole (100 000 utilisateurs contre 4 000 pour le suivant) mal
  noté ; Google Slides n'a **pas** de minuteur natif (plusieurs sources
  concordantes, secondaire).
- Plainte dominante relevée par la presse spécialisée : **la version
  gratuite a été dégradée** au lancement de la version payante. Les
  utilisateurs (enseignants, formateurs) **refusent de payer** pour un
  minuteur — un concurrent gratuit (ExtPilot) s'est déjà placé sur ce
  créneau.
- Plafond : même en captant 2 % de 100 000 utilisateurs à 3 $/mois,
  ~6 000 $/mois — pour le titulaire, pas pour un nouvel entrant. Risque que
  Google ajoute la fonction (point 14).
- **Écarté comme projet en or.**

## Verdict Chrome

Le marché payant existe (20 000 extensions) mais les créneaux payants et mal
servis sont soit juridiquement gris, soit des besoins que les utilisateurs
refusent de payer, soit déjà concurrencés.

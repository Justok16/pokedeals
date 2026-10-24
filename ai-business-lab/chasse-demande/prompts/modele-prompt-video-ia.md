# Modèle de prompt pour une vidéo générée par IA (reçu le 24/10/2026)

Source : texte envoyé par l'utilisateur (auteur inconnu, en anglais, probablement copié d'un reel). Recopié tel quel,
puis la structure est extraite pour nos propres vidéos. Aucune vidéo fabriquée : pas d'outil gratuit disponible le
24/10 (crédits vidIQ épuisés jusqu'au 28/10 ; budget 0 €), et le sujet (une jeune femme qui fait sa valise) n'a pas
de lien avec DIG16.

## Texte reçu

> Create a premium cinematic stylized 3D animated comedy, exactly 15 seconds, vertical 9:16, 24fps, 4K-quality.
> CHARACTER LOCK: NAYA — 26-year-old Indonesian woman, warm medium skin, large expressive brown eyes, dark brown hair
> in a loose messy high bun, coral-pink T-shirt, loose cream pants, small gold hoops, delicate necklace, cream house
> sandals. Stylish, enthusiastic, perfectionist, hilariously determined to pack everything.

(Le texte s'arrête là : la suite, s'il y en avait une, n'a pas été reçue.)

## Ce que ce modèle apprend (structure réutilisable)

1. **Le cadre technique d'abord** : style (3D stylisé, cinéma), durée exacte, format vertical 9:16, 24 images/s,
   qualité. Même ordre que nos fabricants de vidéos (1080 × 1920, 30 i/s, durée contrôlée).
2. **« CHARACTER LOCK » : un personnage verrouillé** : âge, peau, yeux, coiffure, chaque vêtement, bijoux, chaussures,
   puis le caractère en 4 mots. But : que le personnage reste identique d'un plan à l'autre et d'une vidéo à l'autre.
   C'est l'équivalent de notre charte (couleurs, polices, voix « Algieba », empreinte dorée) : tout ce qui doit rester
   pareil est écrit noir sur blanc, une fois, et recopié dans chaque demande.
3. **Un seul ressort comique** (« décidée à tout emporter ») : une idée par vidéo, comme « une phrase = une scène »
   dans nos conseils.

## Si DIG16 en a besoin un jour

- Possible avec `vidiq_generate_video` (crédits vidIQ, 150 par renouvellement, le 28/10) ou tout autre générateur
  gratuit vérifié à la source : écrire le « verrouillage » de notre personnage (un artisan de Charente, atelier,
  tenue de travail, sans visage réel) et une seule idée par vidéo.
- Toujours signaler le contenu comme généré par IA (étiquettes Instagram, TikTok, YouTube déjà cochées dans nos
  publications) ; jamais de visage ou de personne réelle sans accord.

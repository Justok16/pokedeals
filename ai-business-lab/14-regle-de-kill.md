# Règle d'arrêt — DigCost

**Écrite le 21/09/2026, avant d'avoir le moindre visiteur.**

C'est volontaire. Une règle d'arrêt écrite après coup n'est pas une règle,
c'est une justification. Celle-ci est écrite pendant qu'elle ne coûte rien,
pour qu'elle coûte quelque chose plus tard.

Elle est importée d'une critique extérieure (Grok, 21/09/2026), qui reprochait
à ce dossier de ne pas en avoir. Le reproche était fondé.

---

## Le principe

> **Le temps déjà investi n'est pas un argument.**

Un projet qui rate ses seuils ne s'améliore pas indéfiniment : il s'arrête.
Le seul coût qui compte dans une décision d'arrêt est le coût *à venir*.

---

## Les trois échéances

| Échéance | Date | Question posée |
|---|---|---|
| **J+21** | 12/10/2026 | Google voit-il le site ? |
| **J+45** | 05/11/2026 | Quelqu'un arrive-t-il, et reste-t-il ? |
| **J+90** | 20/12/2026 | Y a-t-il un actif, ou seulement des pages ? |

---

## J+21 — l'indexation

**Mesure :** Search Console, onglet Indexation.

| Résultat | Décision |
|---|---|
| Les 5 pages sont indexées | **CONTINUER** |
| 1 à 4 pages indexées | **MODIFIER** — problème technique, pas éditorial. Corriger avant d'écrire une ligne de plus. |
| 0 page indexée après 21 jours | **MODIFIER** — la chaîne de publication est cassée. Ne pas produire de contenu tant qu'elle ne l'est pas. |

À cette échéance, **aucune décision d'arrêt n'est légitime** : 21 jours ne
disent rien sur la demande, seulement sur la plomberie.

---

## J+45 — l'arrivée

**Mesures :** impressions et clics dans Search Console, inscrits beehiiv.

| Résultat | Décision |
|---|---|
| ≥ 300 impressions **et** ≥ 10 clics **et** ≥ 3 inscrits | **AUGMENTER** — écrire les pages comparatives suivantes |
| ≥ 300 impressions mais < 5 clics | **MODIFIER** — on est vu et pas choisi : réécrire titres et descriptions, pas le contenu |
| < 100 impressions | **MODIFIER** — les requêtes visées sont mauvaises ou le site est trop jeune. Vérifier le positionnement avant de conclure. |
| 0 impression | **MODIFIER** — retour au problème technique |

**Seuils arbitraires, et assumés comme tels.** Personne ici ne sait ce qu'est
un volume normal pour un site de cinq pages sans notoriété. Ces nombres
existent pour forcer une décision, pas parce qu'ils sont fondés. Ils seront
révisés à J+45 **avec les données**, et la révision sera écrite ici, datée,
avec sa justification.

---

## J+90 — l'actif

**Mesures :** inscrits beehiiv, clics vers le calculateur, réponses reçues.

| Résultat | Décision |
|---|---|
| ≥ 50 inscrits **et** croissance continue sur 3 semaines | **AUGMENTER** — le média tient, passer à l'étape outil payant |
| 15 à 49 inscrits | **CONTINUER** — trop tôt pour trancher, prolonger de 45 jours, une seule fois |
| < 15 inscrits après 90 jours | **ARRÊTER** |

### Ce que « ARRÊTER » veut dire exactement

Arrêter, ce n'est pas tout effacer :

1. Le site reste en ligne. Il ne coûte rien et continue d'être indexé.
2. **Aucune nouvelle page n'est écrite.**
3. Le moteur de classement rejoue les 17 concepts et le prochain est choisi
   par calcul, pas par lassitude.
4. Ce qui a été appris est consigné dans `11-journal-des-tests.md` — c'est le
   seul actif qui survit à un arrêt, et il est réel.

---

## Ce que cette règle ne fait pas

Elle ne prédit rien. Atteindre un seuil ne prouve pas qu'il y aura un revenu ;
le rater ne prouve pas qu'il n'y en aurait jamais eu. Elle sert à une seule
chose : **empêcher que la décision soit prise par la fatigue ou par
l'entêtement.**

Elle ne remplace pas non plus `12-peut-on-devenir-riche.md`, dont la réponse
reste « non » et ne sera pas révisée à la hausse.

# Audit externe n° 4 — Mistral — contre-lecture

**Reçu le 23/09/2026, en deux parties.** Verdict : **MODIFIER**, confiance
80 %. Navigation géolocalisée en Suède : ses lectures de la grille Shopify
(prix en SEK, Klarna à 2,99 %, iDEAL à ~1,6 %) décrivent un autre marché et
sont écartées pour les tarifs français. Il l'a signalé lui-même.

Il a lu le site **avant** les corrections du 23/09 : l'incohérence
952 / 1 012 € et la section Sources qu'il relève étaient déjà corrigées à
réception.

## Retenu

- **Préciser le marché des taux** : une boutique belge ou suédoise ne paie pas
  les mêmes. ✅ Ajouté sur le calculateur et la page pilier (`digcost`
  `890a378`).
- Recalcul du scénario : conforme, comme pour les trois autres audits.
- Critères du programme d'affiliation (« site actif », « audience établie »,
  toutes les candidatures ne sont pas approuvées), cookie de 30 jours,
  400 jours en cas d'essai converti. Concordant avec Grok et ChatGPT.
- **Seuil chiffré pour le zéro clic** : CTR < 1 % avec au moins 500
  impressions. À intégrer à la règle d'arrêt si l'utilisateur la révise.

## Écarté ou à nuancer

- **« Basic à 33 € en 2026, 27 € date de 2023 »** (d'après un blog) et
  l'hypothèse 27 × 1,2 ≈ 33 = TTC : la lecture française de ChatGPT donne
  36 € sans engagement et 27 € en annuel, identique au relevé du 21/09. Les
  écarts entre blogs ne suivent pas un ratio constant (33/27 = 1,22 mais
  88/79 = 1,11) : ce n'est pas simplement une différence HT/TTC. Les captures
  de l'utilisateur trancheront.
- Créer un essai Shopify pour lire le back-office : exigerait un compte à son
  nom, pour une information que les conditions générales donnent déjà.
- EmpCo comme échéance du 27/09 : déclassée (voir `04-chatgpt.md`).

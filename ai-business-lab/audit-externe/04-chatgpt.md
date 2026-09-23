# Audit externe n° 3 — ChatGPT — contre-lecture

**Reçu le 23/09/2026.** Verdict : **MODIFIER**. Le plus rigoureux des trois :
grille française lue **depuis la France**, conditions générales de Shopify
citées par section, calculateur testé dans un navigateur, et une réserve
explicite sur chaque point non vérifié.

Sa grille Basic concorde **exactement** avec le relevé du 21/09 : c'est le
meilleur indice de fiabilité de ses autres lectures.

## Corrigé sur le site (`digcost` `168958c`, `efffadc`)

| Constat | Vérification | État |
|---|---|---|
| Mode « prestataire externe » : frais Shopify Payments conservés, puis 2 % ajoutés | **Bug réel.** Double comptage. | ✅ Seul le surcoût Shopify s'applique ; frais du prestataire signalés comme non inclus |
| Répartition > 100 % corrigée en silence | Exact | ✅ Corrigée à l'écran |
| Accueil : « écart de 1,5 à 3 fois » | Contredit par les chiffres du site (4,7 à 6,3 fois) | ✅ Remplacé par un ratio soutenu (≈ 3 fois l'abonnement) |
| Synchronisation marketplace appliquée à toutes les commandes | Le seuil porte sur les commandes synchronisées | ✅ |
| Ligne email « 300 contacts » | Unités différentes selon les outils, non relevé | ✅ Présentée comme hypothèse, comme la ligne applications |
| Pas de balise canonique | Exact | ✅ Ajoutée sur chaque page |
| Grille Grow / Advanced, Klarna, HT | Lecture tierce | ➕ Ajoutée à `_data/releves_tarifs.yml`, **statut à confirmer** |

## Corrigé dans le dossier

- **Erreur de calcul dans `13-strategie-patrimoine.md`** : « 3 à 5 fois le
  revenu annuel contre 30 à 45 fois le mensuel = facteur 10 » est faux.
  36 à 60 mois contre 30 à 45 mois : **0,8 à 2**. Le levier 2 et la grille
  patrimoine s'appuyaient dessus. Barré, expliqué, à réexaminer.
- **Adresses de test exposées** : le dossier écrivait les alias de test de
  l'adresse personnelle, alors qu'il prétendait ne pas l'écrire. Remplacées
  dans la version courante ; l'historique reste public.
- **Fin de l'essai beehiiv** : 21/09 + 14 jours = **05/10**, pas 02/10.
- **PayPal « seul moyen »** : le virement bancaire serait aussi prévu.
- **EmpCo** : trois mesures françaises notifiées sur EUR-Lex ; on ne peut
  écrire que « transposition complète non établie ». Échéance **déclassée**.

## Ce qui change la stratégie — pour la synthèse

1. **Shopify prévient ses marchands 30 jours avant toute modification de
   frais** (conditions générales, section 15.2, selon sa lecture). La
   promesse « on vous alerte quand un tarif change » a donc peu de valeur
   pour un marchand **Shopify** : l'éditeur le fait lui-même. Combiné à
   l'affiliation (prime unique pour un **nouveau** marchand, confirmée par
   Grok et ChatGPT), le modèle actuel est pris en tenaille : le lecteur
   retenu n'a pas besoin de l'alerte, et ne rapporte rien.
2. **Les prix Shopify sont hors taxes** (sections 5.5–5.6, selon sa lecture).
   Le trou « HT ou TTC » du site se referme — après confirmation.
3. **Conditions de GitHub Pages** : restrictions sur un usage principalement
   commercial. À vérifier avant toute monétisation active sur ce support.
4. **robots.txt** : sur un sous-répertoire github.io, il est sans effet. Non
   bloquant ; seul un dépôt `justok16.github.io` à la racine le corrigerait.
5. **Mesurer une chaîne**, pas un compteur : exposition qualifiée → usage du
   calculateur → inscription → réponse. Quinze inscrits sans dénominateur ne
   disent rien.
6. **Le prochain livrable attendu** : cinq problèmes réels de marchands,
   documentés, plutôt qu'une nouvelle analyse.

## Convergences des trois audits

| Point | DeepSeek | Grok | ChatGPT |
|---|:-:|:-:|:-:|
| Verdict MODIFIER | ✅ | ✅ | ✅ |
| Acquisition = goulot, contributions publiques sans message privé | ✅ | ✅ | ✅ |
| Mentions légales / RGPD absents, tension avec l'anonymat | ✅ | ✅ | ✅ |
| Anonymat : compte GitHub relie tout | ✅ | ✅ | ✅ |
| Arrêter l'analyse, passer au contact marché | ✅ | ✅ | ✅ |
| Affiliation Shopify = prime unique, pas du récurrent | — | ✅ | ✅ |
| EmpCo hors sujet pour DigCost | — | ✅ | ✅ |
| Rythme d'envoi à revoir | ✅ | ✅ | nuancé |

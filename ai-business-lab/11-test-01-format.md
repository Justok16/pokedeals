# Test 01 — le format soumis à un lecteur réel

**Date** : 21/09/2026
**Statut** : **terminé, résultat exploité**
**Coût** : 0 €, 3 minutes de lecture

> **C'est le premier test réel de ce projet.** Tout ce qui précédait était de
> l'analyse. Ici, un texte a été mis devant quelqu'un, et quelqu'un a répondu.

---

## Protocole

Le numéro 1 a été présenté à l'utilisateur tel qu'il arriverait dans une boîte
mail, avec une question unique et fermée : **« est-ce que vous vous abonneriez
à ça ? »**

Aucune mise en contexte, aucune justification préalable — pour éviter de
fabriquer la réponse souhaitée.

## Réponse obtenue, verbatim

> « Non, trop ennuyeux, trop juridique et personnellement j'évite ce genre de
> newsletters qui polluent nos boîtes mail. »

---

## Analyse — les trois reproches n'ont pas la même valeur

### « Trop ennuyeux », « trop juridique » — signal **faible**

L'utilisateur **n'est pas e-commerçant**. Il ne risque ni 15 000 € d'amende, ni
un délai de rétractation prolongé de douze mois sur son stock. Un lecteur pour
qui ces lignes sont un risque chiffré ne les lit pas comme un lecteur pour qui
elles ne sont rien.

**Mise en garde méthodologique** : « il n'est pas la cible » est *exactement*
l'argument qui sert à ignorer tout retour négatif. Il est retenu ici parce que
l'écart de situation est objectif, pas parce qu'il arrange. Il ne vaut **pas**
pour le troisième reproche.

### « J'évite ce genre de newsletters » — signal **fort**

Celui-ci ne porte pas sur le sujet. Il porte sur le **format**, et plus
précisément sur ce qu'il implique : un email de plus, chaque semaine, qu'on
n'a pas demandé aujourd'hui.

Et il émane de la personne qui devrait **l'écrire chaque mardi pendant douze
mois**. Un format que l'opérateur méprise ne survit pas à la semaine 6.

---

## Ce que ce test a cassé dans la méthode

La grille de notation comportait **dix-huit critères et aucun** ne mesurait ce
que le format exige de l'opérateur **semaine après semaine**. Elle notait le
marché ; elle ne notait pas la tenue.

C'est un angle mort sérieux : **un actif abandonné au mois 3 vaut zéro**, quel
que soit son potentiel économique.

### Critère ajouté — `tenue_dans_la_duree` (poids 2.0)

> 5 = l'actif continue de produire même si l'opérateur s'arrête un mois ;
> 1 = cadence forcée, une interruption détruit l'actif.

Il est noté sur une base **objective** — ce que le format impose — et non sur le
goût de l'utilisateur. Sinon il deviendrait un permis de choisir ce qui est
agréable, et le format le plus agréable du portefeuille (D3) est aussi le plus
inutile.

**Poids volontairement modéré** pour la même raison : il corrige un angle mort,
il ne renverse pas la hiérarchie économique.

---

## Ce que le calcul dit — et il ne dit pas ce que l'utilisateur voulait entendre

| | Avant | Après |
|---|---:|---:|
| A4 Newsletter hebdomadaire | 81.4 | **79.2** |
| B2 Comparateur SEO | 73.2 | **74.7** |
| **Écart** | **8.2 pts** | **4.5 pts** |

Test de sensibilité — en poussant l'aversion de l'opérateur au **maximum**
(`tenue_dans_la_duree` = 1 pour A4) :

| | Score |
|---|---:|
| A4 avec aversion maximale | **78.1** |
| B2 comparateur | 74.7 |
| **Écart résiduel** | **3.4 pts** |

**Conclusion qui s'impose** : le retour négatif **ne tue pas le concept**. Même
en supposant le rejet le plus fort possible, la newsletter reste devant le
comparateur. Le dire autrement serait céder au client contre les chiffres, ce
que le prompt maître interdit explicitement.

**Ce qu'il tue, c'est la CADENCE.**

---

## La variante qui en sort — A4b

Un numéro hebdomadaire à date fixe et un numéro envoyé **quand une échéance
tombe** ne sont pas le même produit. Le second a été noté séparément :

| Concept | Score | Rang |
|---|---:|---:|
| **A4b — newsletter sans cadence forcée** | **79.7** | **1ᵉʳ / 17** |
| A4 — newsletter hebdomadaire | 79.2 | 2ᵉ |
| B2 — comparateur SEO | 74.7 | 6ᵉ |

La variante **gagne 2 points** de tenue dans la durée et en **perd 1** sur
l'avantage défendable — l'habitude du rendez-vous est ce qui crée la relation,
et la relation est ce qu'un concurrent ne copie pas. Ce coût est réel et il est
payé dans la note. **Le solde reste positif.**

---

## Décision

1. **La verticale ne change pas.** Rien dans ce retour n'attaque le marché des
   e-commerçants français. Le réouvrir serait une réaction, pas une décision.
2. **La cadence hebdomadaire est abandonnée.** On envoie quand il y a une
   échéance — pas parce que c'est mardi.
3. **Le comparateur devient le point d'entrée.** C'est un actif SEO : il
   travaille sans cadence, il survit à une pause, et il ne demande à personne
   la permission d'arriver dans sa boîte mail. La newsletter devient la couche
   de **capture** posée dessus, pas le produit d'appel.
4. **Aucun contenu déjà rédigé n'est perdu.** Les six numéros et les treize
   pages de comparateur reposent sur la **même recherche**. Un numéro se
   convertit en page ; l'inverse aussi.

### Ce que cette décision coûte

La cadence hebdomadaire n'était pas une lubie : **l'habitude est le moteur
d'une newsletter**. En y renonçant, on accepte une croissance plus lente et une
relation plus faible. C'est écrit dans la note d'A4b, pas dissimulé.

Le pari est qu'un actif plus lent mais **tenu** bat un actif plus rapide et
**abandonné au mois 3**. Ce pari n'est pas démontré — c'est une hypothèse, et
elle est datée.

---

## Ce que ce test apprend sur le projet lui-même

Trois minutes de lecture ont produit **plus d'information** que la journée
d'analyse qui les a précédées : un critère manquant, un changement de
classement, et une décision de format.

**Règle qui en découle** : avant d'écrire le contenu suivant, faire juger le
contenu existant. Le coût d'un test est de trois minutes ; le coût d'une erreur
de format non détectée, de six semaines.

C'était déjà le reproche formulé dans
[`10-comparaison-chatgpt.md`](10-comparaison-chatgpt.md) §8. Il aura fallu le
formuler pour l'appliquer.

# Journal des tests

> Deux tests réels menés le 21/09/2026, sur le même lecteur, à quelques minutes
> d'intervalle. Coût total : 0 €, six minutes de lecture. Ils ont produit un
> critère de notation, un changement de cadence et un changement d'angle
> éditorial — c'est-à-dire plus que la journée d'analyse qui les a précédés.

---

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

---

# Test 02 — l'angle soumis au même lecteur

**Date** : 21/09/2026, quelques minutes après le test 01
**Statut** : **terminé, résultat exploité**
**Coût** : 0 €, 3 minutes de lecture

## Protocole

La page pilier du comparateur — *« Combien coûte vraiment une boutique en ligne
par mois »* — a été présentée au **même lecteur**, dans les mêmes conditions que
le numéro 1 : texte intégral, deux questions fermées (« cliqueriez-vous
dessus ? », « iriez-vous jusqu'au bout ? »).

**Pourquoi ce test précisément** : à la fin du test 01, une alternative restait
ouverte et non tranchée. Si le rejet portait sur le **format** (l'email), le
comparateur devait passer. S'il portait sur l'**angle** (le droit, les
obligations), il fallait rouvrir la verticale entière. Il fallait donc mettre
devant lui un texte qui change le format **et** l'angle, et voir.

## Réponse obtenue, verbatim

> « C'est déjà plus plaisant et on est dans le concret. »

## Ce que ça tranche

Comparés terme à terme, les deux textes ne diffèrent pas que par le support :

| | Numéro 1 (rejeté) | Page pilier (accepté) |
|---|---|---|
| Support | Email, cadence hebdo | Page web, sans cadence |
| Angle dominant | **Obligation** — ce que vous risquez | **Coût** — ce que vous payez |
| Registre | Textes, articles, sanctions | Calculs, tableaux, totaux |
| Ce que le lecteur en fait | Se met en conformité | Récupère de l'argent |

Le changement de format était déjà décidé au test 01. **Ce test isole la seconde
variable** : le passage de l'obligation au coût. Et c'est le mot « concret » qui
le dit — il ne qualifie pas un support, il qualifie une matière.

**Conclusion** : la verticale n'est pas à rouvrir. L'hypothèse alternative
laissée ouverte à la fin du test 01 — « le problème est peut-être l'angle, donc
la verticale » — est **écartée**, non par préférence mais parce que le même
lecteur accepte le même sujet dès qu'il est abordé par les chiffres.

## Limite de ce test, et elle est la même qu'au test 01

Le lecteur **n'est toujours pas e-commerçant**. Ce qu'il valide, c'est son
propre engagement — ce qui compte pour `tenue_dans_la_duree`, puisque c'est lui
qui produira ce contenu pendant douze mois, mais qui ne dit **rien** de ce qu'un
commerçant lira.

**Deux tests sur le même lecteur ne font pas une audience.** Le vrai test reste
un e-commerçant devant ces textes, et il n'a pas eu lieu.

Signaler aussi un biais propre à celui-ci : la page pilier lui a été présentée
**après** un refus, avec une question qui suggérait une amélioration possible.
Un « c'est mieux » obtenu dans cette position vaut moins qu'un « c'est bien »
obtenu à froid.

## Conséquence éditoriale — la hiérarchie des angles s'inverse

**Règle adoptée** : sur cette verticale, **le coût passe avant l'obligation**.

Concrètement, dans tout contenu du projet :

1. **Titre et accroche parlent d'argent** — ce que ça coûte, ce que ça rapporte,
   ce qu'on paie en trop. Jamais d'une obligation en première ligne.
2. **L'obligation arrive en second**, comme cause du coût — pas comme menace.
   « Cette obligation vous coûte X » plutôt que « vous risquez Y ».
3. **Un chiffre calculé dans les trois premières lignes.** C'est ce que le
   lecteur a appelé « concret » : pas un fait, un **calcul** qu'il peut refaire.

**Ce que cette règle ne change pas** : la rigueur de vérification. Un contenu
qui mène par les chiffres a *davantage* besoin de sources que l'inverse — un
tarif faux se vérifie en trente secondes et détruit la crédibilité de toute la
page.

**Ce que cette règle coûte** : les sujets purement réglementaires sans dimension
financière (le DSA, l'accessibilité) deviennent difficiles à titrer. Ils ne sont
pas abandonnés, mais ils cessent d'être des sujets d'accroche.

## Réordonnancement qui en découle

| | Avant | Après |
|---|---|---|
| Premier contenu publié | Numéro 1 (rétractation) | **Page pilier du comparateur** (coût réel) |
| Premier envoi email | Numéro 1 | **Numéro 4** (« Combien coûte vraiment une boutique ») |
| Numéros réglementaires | 1, 2, 3, 5, 6 | Conservés, mais **retitrés par le coût** |

**Tension à ne pas escamoter** : le numéro 4 est aussi celui qui **monétise** —
il porte les liens d'affiliation. La règle éditoriale d'origine disait de ne
rien vendre avant trois numéros, pour installer la crédibilité.

**Résolution** : l'angle peut être l'argent sans que le contenu soit monétisé.
La page pilier le démontre — elle n'est que chiffres, et la mention
« Publicité » est en bas, avec la méthode de classement publiée. On garde donc
**l'angle argent** et **la retenue commerciale**. Ce n'est pas une contradiction,
mais il faut le tenir volontairement, parce que la pente naturelle est inverse.

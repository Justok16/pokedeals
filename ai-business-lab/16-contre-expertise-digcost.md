# Contre-expertise — DigCost

**Date : 22/09/2026, 03h00.** Exercice demandé par le prompt n° 2 fourni par
l'utilisateur : chercher **pourquoi ce projet pourrait échouer** malgré une
bonne exécution.

Le site a été mis en ligne il y a six heures. C'est le bon moment pour ça :
rien n'est encore engagé.

---

## Les six angles du prompt

### 1. Le problème est-il assez important pour déclencher un achat ?

**Faiblesse réelle.** DigCost ne vend rien. Le revenu supposé viendrait de
l'affiliation. Or **aucun programme d'affiliation n'a été vérifié** : ni sa
disponibilité, ni ses conditions, ni si un site neuf y est accepté.

Toute la thèse de revenu repose sur une hypothèse jamais testée.
**À vérifier avant J+45**, pas après.

### 2. Les solutions existantes suffisent-elles déjà ?

Partiellement. Les tests 03 et 06 montrent que les pages concurrentes
existent et que plusieurs portent les bons chiffres. L'écart trouvé — des
prix périmés dans le résumé automatique de Google — est réel mais **il peut
se corriger tout seul** : Google réindexe, la page tierce fautive se met à
jour, et l'angle disparaît.

**Un avantage qui dépend de l'erreur d'un autre n'est pas un avantage
défendable.**

### 3. La différence est-elle utile, ou seulement spectaculaire ?

« Aucune place achetable » est une promesse que **le lecteur ne peut pas
vérifier**, et dont rien ne prouve qu'il la valorise. Elle protège la valeur
de revente et la conscience de l'auteur — pas forcément la conversion.

Le calculateur, lui, est une différence utile et vérifiable en trente
secondes. **C'est le seul vrai atout du site à ce jour.**

### 4. Peut-on atteindre les acheteurs à un coût compatible avec la marge ?

Le coût d'acquisition est nul (référencement naturel), donc oui
mécaniquement. Mais **une menace structurelle a été observée et sous-estimée
jusqu'ici** :

> Sur les deux marchés relevés, **le résumé automatique de Google répond
> directement à la question « combien ça coûte »**, sur la page de résultats.

Un internaute peut obtenir sa réponse **sans jamais cliquer**. Être bien
classé ne garantit donc pas le trafic. Ce risque touche le cœur du
positionnement, puisque le site répond précisément à la question que ces
résumés traitent le mieux : un prix.

**C'est le risque le plus sérieux identifié à ce jour.**

### 5. L'intégration, les données et le support sont-ils réalistes ?

**Non, à terme.** Chaque page publiée crée une dette de vérification
permanente : les tarifs changent plusieurs fois par an. À 4 pages, c'est
tenable. À 13 pages, c'est un travail récurrent qui ne produit aucun contenu
neuf.

Le critère `tenue_dans_la_duree`, ajouté au test 01, s'applique ici et
n'avait pas été appliqué au comparateur lui-même.

### 6. Une plateforme concurrente peut-elle absorber la fonctionnalité ?

**Oui, trivialement.** Un calculateur de coût est quelques heures de travail.
Shopify peut le publier. NerdWallet, classé 5e aux États-Unis, aussi. Rien
ne l'empêche.

La seule barrière possible est l'**accumulation de relevés datés dans le
temps** — un historique des prix que personne d'autre n'a. Ce n'est pas
encore construit, et ça devrait l'être : chaque relevé devrait être conservé,
pas remplacé.

---

## Le défaut que la contre-expertise fait remonter, et qui n'avait pas été vu

**L'audience visée prend une décision unique.**

Quelqu'un qui cherche « combien coûte Shopify » choisit une plateforme. Une
fois choisie, **il n'a plus jamais besoin de DigCost.** Il ne reviendra pas,
et il n'a aucune raison de rester sur une liste d'emails.

C'est incompatible avec l'actif visé — une liste, un revenu récurrent, un
site qui se revend sur sa régularité.

**Le calcul est juste, l'audience est mal définie.**

L'audience durable n'est pas « celui qui choisit une plateforme », c'est
**le marchand déjà installé dont les coûts changent sans qu'il le sache** :
hausse de tarif, changement de taux, nouvelle obligation. Celui-là a un
problème qui revient, donc une raison de rester abonné.

---

## Verdict

**MODIFIER.** Ni abandonner, ni tester en l'état.

Le site, le calculateur et la méthode sont bons. **La cible est à
reformuler**, et deux vérifications manquent avant d'investir davantage.

### Ce qui change

1. **La page pilier reste** : c'est la porte d'entrée par le référencement,
   même si son lecteur ne revient pas.
2. **La newsletter doit s'adresser aux marchands installés**, pas aux
   futurs. La promesse « un email quand un tarif change » est déjà la bonne :
   c'est l'angle des pages qui ne l'est pas encore.
3. **Conserver l'historique des relevés** au lieu de les écraser. C'est la
   seule barrière que personne ne peut copier rétroactivement.

### Les deux vérifications à faire avant J+45

- **Un programme d'affiliation accepte-t-il ce site ?** Sans réponse, la
  thèse de revenu est creuse.
- **Le résumé automatique de Google absorbe-t-il le clic ?** Mesurable dès
  les premières données de Search Console : beaucoup d'impressions et très
  peu de clics serait le signal.

### Ce qui ferait abandonner

Inchangé : moins de 15 inscrits au 20/12/2026 (`14-regle-de-kill.md`).
**S'y ajoute** : un taux de clic durablement inférieur à 1 % malgré des
impressions correctes signifierait que le résumé automatique répond à la
place du site — et alors le positionnement « donner un chiffre » est mort,
quelle que soit la qualité du travail.

---

## Suites données — 22/09/2026, le jour même

Une contre-expertise qui ne change rien n'est qu'un exercice de style. Les
trois points du verdict ont été traités dans la journée.

| Ce qui changeait | Fait | Où |
|---|---|---|
| Conserver l'historique des relevés | ✅ | `_data/releves_tarifs.yml` et `_data/resumes_automatiques.yml` — commit `44929da` |
| Vérifier qu'un programme d'affiliation accepte ce site | ⚠️ partiel | Vérifié en source secondaire seulement (`bf8b891`). Reste à confirmer à la source, et un compte PayPal vérifié est requis. |
| La newsletter doit s'adresser aux marchands installés | ✅ | Bloc d'inscription réécrit — commit `b2b1c20` |
| Mesurer si le résumé automatique absorbe le clic | ⏳ | Impossible avant les premières données de Search Console. Le site a moins de 48 h. |

### Ce que la réécriture du bloc d'inscription change concrètement

Le bloc parlait de « recevoir les prochains calculs ». Il s'adressait, sans
le vouloir, à celui qui n'a plus besoin du site dès qu'il a choisi.

Il s'adresse maintenant au marchand déjà en ligne, et il s'appuie sur le
seul relevé daté que nous possédions : le 21/09, le résumé automatique de
Google annonçait 66 €/mois pour la formule Grow quand la grille de
l'éditeur affichait 79 € — **156 € sur une année, pour qui se fiait au
chiffre le plus visible.**

C'est le seul argument du site qu'un concurrent ne peut pas écrire : il
faut l'avoir relevé ce jour-là.

Le calculateur a gagné une ligne de sensibilité calculée sur le volume du
lecteur — deux dixièmes de point de plus sur le taux standard, et voilà le
surcoût annuel. Elle arrive à l'instant précis où il vient d'obtenir son
total. Elle dit explicitement qu'aucune hausse n'est annoncée : c'est un
ordre de grandeur, pas une prévision.

### Ce qui reste non résolu, et il faut le dire

Le risque n° 4 — **le résumé automatique répond à la place du site** — n'est
pas traité par cette modification. Il ne peut pas l'être par l'écriture :
il se mesure. Si les impressions montent et que les clics ne suivent pas,
le positionnement « donner un chiffre » est mort, et aucune qualité
rédactionnelle n'y changera quoi que ce soit.

La réécriture du bloc d'inscription ne fait qu'une chose : **elle rend
l'abonné utile s'il vient.** Elle ne le fait pas venir.

---

## Note sur l'exercice

Cette contre-expertise a produit **deux failles réelles non vues en six
heures de travail** : l'audience à décision unique, et le risque de réponse
sans clic. Le prompt qui l'a déclenchée venait de ChatGPT.

C'est l'apport le plus utile reçu d'un modèle concurrent depuis le début du
projet — non pas une stratégie, mais **une méthode pour attaquer la sienne.**

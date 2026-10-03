# Comparaison — même prompt maître, deux sorties

**Date** : 21/09/2026
**Objet** : l'utilisateur a soumis le **même prompt maître** à ChatGPT et à ce
dossier. Ce document compare les deux sorties, y compris là où celle-ci perd.

> **Règle appliquée ici** : le prompt maître interdit de flatter l'utilisateur.
> Il interdit aussi, implicitement, de flatter l'auteur de ce document. Ce qui
> suit commence donc par ce que ChatGPT a fait de mieux.

---

## 1. Ce que chacun a produit

| | ChatGPT | Ce dossier |
|---|---|---|
| **Verticale retenue** | Revendeurs **Vinted** | **E-commerçants** français |
| **Forme** | Chaîne Shorts faceless + calculateur de marge | Newsletter + comparateur + affiliation récurrente |
| **Justification du choix** | Affirmée | **Calculée** : 15 concepts, 18 critères, code + 10 tests, contre-épreuve sous grille « revenu maximal » |
| **Livrables** | 2 vidéos montées, 1 moteur de voix installé, 1 veille | 6 numéros, 13 pages de comparateur, 31 scripts, moteur de classement, 3 fiches radar |
| **Soumis au réel** | **Oui** — et rejeté deux fois | **Non.** Rien n'a été publié ni même relu |
| **Revenu généré** | 0 € | 0 € |

---

## 2. Ce que ChatGPT a fait mieux — et c'est le point décisif

### Il a produit quelque chose à regarder, et il a appris de l'échec

En une session, l'utilisateur a **vu deux vidéos** et a pu dire « moche » et
« voix robot ». C'est un signal réel, obtenu en heures, sur le seul sujet qui
comptait vraiment : *est-ce que la production faceless atteint un niveau
acceptable avec 0 € et aucune compétence vidéo ?* Réponse obtenue : **non**.

Ce dossier a produit **7 400 lignes** et n'a obtenu **aucun signal de la
réalité**. Zéro. Le prompt maître demandait un laboratoire de test (§8) et la
règle « tester beaucoup, tuer vite ». **J'ai construit le laboratoire et je n'ai
jamais lancé d'expérience.** C'est le reproche le plus sérieux que cette
comparaison m'adresse, et il est fondé.

Nuance qui ne l'annule pas : ce qu'il a appris porte sur **sa propre chaîne de
production**, pas sur le marché. Aucune vue, aucun abonné, aucun euro n'a été
mesuré. Le signal est réel mais interne.

### Il s'est corrigé à voix haute, deux fois

> « Cette version est ratée. J'ai changé les couleurs et les animations sans
> résoudre le manque de qualité visuelle. »
> « Je retire aussi Kokoro comme voix retenue pour cette chaîne. »

Abandonner un outil qu'il venait d'installer et de présenter comme une réussite,
c'est exactement la discipline demandée au §19. C'est bien fait.

### Sa veille est méthodologiquement propre sur trois points

1. Elle sépare **annonces datées** et **offres simplement revérifiées**.
2. Elle écrit ce qu'elle n'a **pas** mesuré : *« Aucun volume de recherche ni
   résultat commercial privé n'a été mesuré. »*
3. Elle relève une **contradiction dans sa propre source** — Make affiche 35 %
   sur 12 mois à un endroit, 24 mois à un autre — et retient prudemment 12.

Le point 1 est meilleur que mon Niche Radar, qui ne fait pas cette distinction.
**Je l'adopte** (voir §6).

---

## 3. Ce que ce dossier fait mieux

### Le choix de verticale est calculé, pas affirmé

ChatGPT a choisi Vinted et ne montre pas contre quoi. Ici, le classement est
reproductible et **contestable avec des chiffres** : changez un poids dans
`outils/criteres.yaml`, tout le classement se rejoue.

C'est ce qui permet de trancher la question posée par cette comparaison
autrement qu'à l'opinion — ci-dessous.

### Il a choisi le format le plus difficile pour ce profil précis

L'utilisateur se déclare **2/5 en vidéo**, avec **0 €**. La vidéo faceless de
qualité exige des images réelles, du montage et une voix convaincante. La
conversation le **démontre** : deux versions rejetées, et le goulot est
exactement ce qui coûte de l'argent.

Le format retenu est aussi celui du pire RPM (**0,50-2,50 $** sur les Shorts
grand public, contre **5-12 €** en B2B francophone). Et la veille de ChatGPT
signale elle-même le risque YouTube sur les contenus produits en masse — le
risque du format qu'il a choisi.

### Contradiction interne de sa propre sortie

Sa veille identifie la **facturation électronique** comme une opportunité datée
et vérifiée sur impots.gouv.fr — puis la classe *« surveillance, pas de
lancement supplémentaire »*, tout en gardant Vinted comme **seul test actif**.

Sa veille a trouvé le bon sujet et ne l'a pas joué. Ce dossier a mis sa mise
dessus : **A1 « facture électronique » est 3ᵉ sur 16** en grille de référence,
**4ᵉ** en grille « revenu maximal », et le sujet irrigue quatre des six numéros.

---

## 4. Le verdict, calculé

« Marge Claire » a été entrée dans le moteur (`concepts.yaml`, id **F1**), notée
selon la **même grille** que les quinze autres, en s'appuyant largement sur les
constats de ChatGPT lui-même.

| Grille | Score | Rang |
|---|---:|---:|
| Référence | **42,5 / 100** | **16ᵉ sur 16** |
| « Revenu maximal » | **42,5 / 100** | **14ᵉ sur 16** |

Dernier du portefeuille en grille de référence — **sous la chaîne faceless de
divertissement**, qui avait déjà été écartée.

Les quatre notes qui l'enfoncent, et leur source :

| Critère | Note | Fondement |
|---|:--:|---|
| `valeur_commerciale` | 1/5 | Audience de particuliers revendant des vêtements : RPM et pouvoir d'achat au plus bas |
| `concurrence_faible` | 1/5 | ChatGPT : *« Concurrence : forte, y compris sur les outils gratuits et les guides »* |
| `facilite_production` | 1/5 | Démontré par la conversation : deux versions rejetées |
| `avantage_defendable` | 1/5 | ChatGPT : *« le tableur générique payant n'a toujours pas de différenciation démontrée »* |

### Test de robustesse — et si j'étais de mauvaise foi ?

La note a été rejouée avec des corrections délibérément généreuses :

| Hypothèse | Score |
|---|---:|
| Tel que noté | 42,5 |
| Les trois notes à 1 remontées à **3/5** | 50,4 |
| \+ `valeur_commerciale` à **3/5** | 53,8 |
| \+ automatisation 4, indépendance 3, **vitesse de validation 5/5** | **61,7** |

Même avec **sept corrections favorables**, dont la vitesse de validation au
maximum, le concept plafonne à 61,7 — **sous E2 (68,7)**, qui n'est que 8ᵉ.
Il n'entre pas dans la première moitié du portefeuille.

**Conclusion** : le désaccord entre les deux sorties ne tient pas à une
divergence d'opinion rattrapable par un ajustement de notation. Le verdict
survit à toute notation défendable.

> **Ce que ce verdict ne dit pas** : que la chaîne ne ferait aucune vue. Une
> chaîne Vinted peut très bien marcher en audience. Il dit qu'elle convertit mal
> une audience en revenu récurrent, et que c'est cela que l'utilisateur a
> demandé.

---

## 5. Là où les deux sorties convergent — et ça compte

Deux exécutions indépendantes du même prompt, par deux modèles différents, sont
arrivées aux mêmes sujets forts :

| Sujet | ChatGPT | Ici |
|---|---|---|
| **Facturation électronique** | Signal daté, vérifié sur impots.gouv.fr | Concept **A1**, 3ᵉ/16 — et 4 numéros sur 6 |
| **Automatisations** | *« Réserve prioritaire »* n° 1 | Concept **E2**, 68,7 — 8ᵉ/16 |
| **Calendrier de la réforme** | Réception 09/2026, émission 09/2027 | **Identique** |

Le troisième point a une valeur directe : le calendrier publié dans les numéros
1 et 5 a été **vérifié deux fois, indépendamment, sur la source officielle**.
C'est le fait le plus solide du dossier. Consigné dans `lancement/verifications.md`.

---

## 6. Ce que j'intègre de son travail

| Apport | Ce que j'en fais |
|---|---|
| Distinction **annonce datée / offre revérifiée** | Adoptée dans le Niche Radar |
| **Règles YouTube** : pas de persona IA se présentant comme expert humain sur sujets sensibles | **Risque réel pour ce dossier** — contenu réglementaire, sous pseudonyme, rédigé par IA. Règle éditoriale écrite (§7) |
| Le **concurrent gratuit** tue le produit payant (VintedCRM) | Ajouté comme test préalable : *qui le fait déjà gratuitement ?* |
| Priorité à **l'extrait de référence validé** avant la série | Transposé : faire juger **un** numéro avant d'en écrire d'autres |

---

## 7. Règle éditoriale ajoutée — persona et sujets sensibles

Déclenchée par la veille de ChatGPT, qui a relevé ce que ce dossier avait
manqué : les plateformes sanctionnent les **personas IA se présentant comme des
experts humains** sur des sujets sensibles.

Ce dossier publie du **contenu réglementaire**, sous **pseudonyme**, **rédigé par
IA**. Les trois conditions sont réunies.

**Règle** — dans tout contenu de ce projet :

1. Ne **jamais** revendiquer un titre professionnel : ni avocat, ni
   expert-comptable, ni conseil.
2. **Dire** ce qu'on n'est pas quand le sujet le touche. Le numéro 6 le fait
   déjà : *« je ne suis pas avocat »*. Ce n'était qu'un réflexe — c'est
   désormais une règle.
3. Renvoyer à la **source officielle** et à un professionnel pour toute
   application à un cas particulier.
4. Ne **jamais** produire en série des contenus interchangeables.

Cette règle n'est pas une précaution cosmétique : elle est aussi la **meilleure
protection juridique** du projet, et elle renforce la position éditoriale déjà
retenue — *on ne promet aucun revenu, on ne vend aucune méthode.*

---

## 8. Ce que je retiens contre moi

Le classement me donne raison sur le **choix**. Il ne me donne pas raison sur la
**méthode de travail**, et les deux sont indépendants.

ChatGPT a fait regarder quelque chose à l'utilisateur en quelques heures. Ce
dossier lui a demandé, pendant tout ce temps, de **créer un dépôt GitHub** —
c'est-à-dire de l'administratif — sans jamais lui demander de **juger le
produit**.

Les six numéros sont lisibles **maintenant**, sans compte, sans dépôt, sans
outil. Le bon équivalent de sa vidéo, c'est
[`lancement/numeros/numero-01.md`](lancement/numeros/numero-01.md) : trois
minutes de lecture, et la seule question qui compte — *est-ce que je
m'abonnerais à ça ?*

Correction appliquée : voir [`PREMIER-ENVOI.md`](PREMIER-ENVOI.md), réduit au
chemin le plus court entre ici et un premier envoi réel.

**Le point commun des deux sorties reste le plus important : après une journée
de travail des deux côtés, rien n'est publié et personne n'a payé un euro.**
Sur ce terrain, aucune des deux n'a d'avance sur l'autre.

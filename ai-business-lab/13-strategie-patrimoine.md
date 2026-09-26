# Stratégie recalculée pour le patrimoine

**21/09/2026.** Consigne explicite de l'utilisateur, après lecture de
[`12-peut-on-devenir-riche.md`](12-peut-on-devenir-riche.md) :

> « Je vais être clair, c'était LA seule vraie volonté de ma part donc fais en
> sorte que ce soit le cas. »

**Ce que je ne peux pas faire** : garantir ce résultat. Personne ne le peut, et
[`12`](12-peut-on-devenir-riche.md) n'est pas révisé.

**Ce que je peux faire, et qui est fait ici** : changer la **fonction
objectif**. Jusqu'ici la stratégie optimisait le rapport potentiel/risque/effort.
Elle optimise désormais la **valeur patrimoniale de l'actif** — ce qui est une
stratégie différente, pas la même en plus ambitieux.

---

## 1. La troisième grille

`outils/criteres-patrimoine.yaml`. Elle pèse lourd sur ce qui fait un actif
vendable — `revente_actif` **5.0**, `revenu_recurrent` 4.0, `avantage_defendable`
4.0, `international` 4.0 — et **neutralise** `facilite_production`, `cout_faible`
et `vitesse_validation` à 0.5.

> **Ce qu'elle accepte en échange, et qui doit être assumé** : une probabilité
> d'échec **plus élevée**, un délai plus long avant le premier euro, un effort
> plus lourd. Elle n'optimise pas l'espérance de gain. **Elle optimise le
> plafond.**

### Un enseignement est tombé en l'écrivant

`affiliation` reçoit le poids **1.5**, contre 2.0 dans la grille de référence.
L'affiliation est une excellente source de **revenu** et un mauvais actif
**patrimonial** : elle dépend d'un programme tiers qui peut changer ses taux,
elle ne crée aucune relation contractuelle avec le client final, et un acheteur
la décote lourdement.

**Elle finance la phase 1. Elle ne construit pas le patrimoine.** Ce n'était
écrit nulle part avant.

---

## 2. Ce que le classement dit — et ce n'est pas ce que j'attendais

| # | Concept | Patrimoine | Rang de référence |
|---|---|---:|---:|
| 1 | A4 Newsletter hebdomadaire | 79.3 | 2 |
| 2 | A4b Newsletter sans cadence | 78.8 | 1 |
| 3 | A2 IA appliquée à un métier | 78.6 | 3 |
| **4** | **E1 Micro-SaaS no-code B2B** | **78.6** | **8** ⬆ |
| **5** | **B3 Outils gratuits → freemium** | **77.1** | **7** ⬆ |
| 6 | B2 Comparateur | 76.6 | 6 |

**Le classement bouge à peine.** Même en optimisant uniquement la valeur de
l'actif, la même famille de concepts gagne. Deux remontent — le micro-SaaS et
les outils gratuits en freemium — et c'est cohérent : ce sont les deux seuls qui
produisent un **logiciel**.

### Le vrai résultat est ailleurs, et il est plus important

J'ai calculé le **plafond** de chaque concept : son score si tout son potentiel
était réalisé (international, revente et récurrence au maximum).

```
A4   plafond 85.1     A1   plafond 84.3
A2   plafond 84.8     B3   plafond 83.4
A4b  plafond 84.6     A3   plafond 83.1
```

**Aucun des 17 concepts ne dépasse 85**, même en supposant tout réussi.

Ce n'est pas un défaut de la grille : c'est le constat central. **Le choix du
concept n'est pas le levier.** Ces dix-sept options appartiennent toutes à la
même catégorie — solo, 0 €, sans capital — et cette catégorie a un plafond.
Choisir A4 plutôt que B2 change un rang, pas un ordre de grandeur.

**Donc : arrêter de chercher le bon concept. Les leviers sont ailleurs.**

---

## 3. Les trois leviers réels, dans l'ordre de leur effet mesuré

### Levier 1 — La langue. **C'est le plus gros, et il était invisible.**

Ce que la contrainte francophone coûte, sous la grille patrimoine :

| Concept | `international` | Score FR | Si anglophone | Écart |
|---|:--:|---:|---:|---:|
| A3 | 1/5 | 73.0 | 80.7 | **+7.7** |
| A4b | 2/5 | 78.8 | 84.6 | **+5.8** |
| A1 | 2/5 | 76.1 | 81.9 | **+5.8** |
| B2 | 3/5 | 76.6 | 80.5 | +3.9 |
| E1 | 4/5 | 78.6 | 80.5 | +1.9 |

**Le français seul est le plafond que vous vous êtes imposé.** C'est de loin le
facteur le plus déplaçable du dossier, et il ne coûte rien à changer tant que
rien n'est publié.

**Conséquence adoptée** : l'anglais n'arrive plus « plus tard, si ça marche ».
Il arrive au **mois 6**, et la structure du site le prévoit dès la première
page. Les tarifs, les frais de paiement, les comparatifs de plateformes sont
les mêmes objets dans tous les marchés — c'est du contenu traduisible, pas à
réécrire. Les pages réglementaires françaises, elles, ne se traduisent pas :
elles restent un actif local.

### Levier 2 — La destination. **Le média n'est pas l'actif.**

E1 passe 8ᵉ → 4ᵉ dès qu'on note la valeur patrimoniale. La raison est
arithmétique et figure dans [`12`](12-peut-on-devenir-riche.md) : un logiciel
B2B se revend **3 à 5 fois son revenu annuel**, un site de contenu **30 à 45
fois son revenu mensuel**. ~~À revenu égal, un facteur proche de **10**.~~

> **❌ ERREUR DE CALCUL, relevée le 23/09/2026 par un audit externe (ChatGPT,
> `audit-externe/04-chatgpt.md`).** 3 à 5 fois le revenu annuel, c'est 36 à
> 60 fois le revenu mensuel. Face à 30 à 45 fois pour un site de contenu,
> l'écart à revenu égal est de **0,8 à 2**, pas de 10. Le levier 2 reste
> défendable sur d'autres motifs (récurrence, relation contractuelle), mais
> **pas sur celui-ci**, et la grille `criteres-patrimoine.yaml` a été pondérée
> en le croyant. À réexaminer avant toute décision qui s'appuie dessus.

**Conséquence adoptée** : le comparateur et la newsletter cessent d'être le but.
Ils deviennent le **canal d'acquisition et l'instrument de découverte** du
problème que le logiciel résoudra.

Concrètement, et c'est nouveau : chaque contenu publié doit servir **deux** fins.
Informer, et **collecter le problème**. Un journal des questions récurrentes est
ouvert dès la première page publiée — c'est lui qui désignera le SaaS, pas une
intuition.

### Levier 3 — Le temps passé dans le jeu

Ni la niche ni la grille ne décident. **La durée décide.** L'affiliation
récurrente, la valeur SEO et la connaissance du marché composent toutes les
trois sur plusieurs années.

Et c'est ici que le dossier porte son propre avertissement : le **test 01** a
montré que l'utilisateur n'aime pas le format qu'il devrait produire. C'est
précisément le risque n° 1 de [`12`](12-peut-on-devenir-riche.md) §1, et aucune
grille ne le corrige.

---

## 4. Le plan révisé

| | Avant | Après |
|---|---|---|
| **But** | Un actif à 1 500 €/mois | Un **logiciel B2B revendable** |
| **Rôle du média** | Le produit | Le **canal** vers le produit |
| **Langue** | FR, anglais « plus tard » | FR puis **anglais au mois 6** |
| **Affiliation** | Monétisation principale | **Financement de la phase 1** |
| **Horizon** | 24 mois | **4 à 5 ans** |
| **Mesure de succès** | Revenu mensuel | **Valeur de revente** |

**Ce qui ne change pas** : la verticale (e-commerçants), les six numéros, les
treize pages, la discipline de vérification. Rien du travail fait n'est perdu —
ce qui change est ce à quoi il **sert**.

**Ce qui change dès la première ligne publiée** :
1. Le site est structuré pour accueillir une version anglaise (`/fr/`, `/en/`).
2. Un journal des questions de lecteurs est tenu à partir du premier contact.
3. La capture d'emails est prioritaire sur le clic d'affiliation — une liste est
   un actif, un clic ne l'est pas.

---

## 5. Ce que ce plan coûte, et il faut le lire avant de dire oui

- **Le premier euro arrive plus tard.** La grille neutralise explicitement la
  vitesse de validation.
- **La probabilité d'échec augmente.** Optimiser un plafond, c'est accepter une
  variance plus grande. Le résultat médian reste **zéro**, et il l'est davantage
  qu'avec la grille de référence.
- **L'horizon double**, de 24 mois à 4-5 ans.
- **L'anglais impose un standard plus dur** : le marché anglophone est plus
  concurrentiel et plus exigeant que le francophone.

**Ce qui ne change pas non plus** : atteindre un SaaS à 30 000 €/mois est rare.
Ce plan maximise la probabilité d'y arriver ; il ne la rend pas élevée. Aucune
ligne de ce dossier ne promet ce résultat, et aucune ne le promettra.

---

## 6. La seule chose qui déciderait vraiment

Aucune des trois grilles ne mesure ce qui compte le plus : **le nombre de
tentatives**.

Quelqu'un qui lance un projet et l'abandonne à six mois a une probabilité de
richesse proche de zéro, quelle que soit la qualité du plan. Quelqu'un qui reste
cinq ans, apprend de trois échecs et tente une quatrième fois a une probabilité
faible mais **réelle**.

**C'est la seule variable sur laquelle ce dossier n'a aucune prise, et c'est la
plus déterminante.** Elle est entièrement de votre côté.

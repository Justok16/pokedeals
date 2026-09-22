# Échéances à surveiller

Toutes les dates du projet, au même endroit. Un projet automatisé meurt
rarement d'un choix stratégique : il meurt d'une date que personne n'a vue
passer.

**Dernière mise à jour : 22/09/2026.**

---

## Les échéances fermes

| Date | Quoi | Conséquence si c'est raté |
|---|---|---|
| **27/09/2026** | Directive (UE) 2024/825 « EmpCo » applicable | Le numéro 6 de la newsletter porte dessus. Vérifier l'état du texte **le jour même** avant d'envoyer quoi que ce soit. Rien ne doit être affirmé sans source officielle relevée ce jour-là. |
| **~02/10/2026** | **Fin de l'essai Max beehiiv** (démarré le 21/09, 14 jours) | Deux risques distincts, voir ci-dessous. |
| **12/10/2026** | J+21 — indexation | Décision : continuer ou corriger la plomberie. Aucun arrêt légitime à cette date. |
| **05/11/2026** | J+45 — arrivée | Décision : augmenter, modifier, ou réviser les seuils avec les données. |
| **20/12/2026** | J+90 — actif | **Seule date où « arrêter » est une décision possible.** Seuil : moins de 15 inscrits. |

Les trois dernières sont détaillées dans `14-regle-de-kill.md`.

---

## Fin de l'essai beehiiv — deux risques, pas un

Budget du projet : **0 €**. L'essai a été activé sans intention de payer.

### Risque 1 — le prélèvement

Vérifier **avant** l'échéance ce qui se passe le dernier jour : bascule
automatique vers le plan gratuit, ou prélèvement sur une carte enregistrée ?

→ https://app.beehiiv.com/settings/workspace/billing

### Risque 2 — la panne silencieuse, et c'est la plus dangereuse

L'email de bienvenue est construit avec les **Automations** (déclencheur
« Signed up »). Si cette fonction est réservée au plan payant, elle
**s'arrêtera sans alerte** à la fin de l'essai.

Personne ne sera prévenu. Les nouveaux inscrits cesseront simplement de
recevoir le message d'accueil, et le premier signe visible sera une
délivrabilité dégradée plusieurs semaines plus tard, sans cause apparente.

**Vérification à faire le jour J :** s'inscrire avec une adresse de test
(`justokseize+verif@gmail.com`) et confirmer que l'email de bienvenue
arrive toujours.

**Si la fonction est perdue :** replier le message d'accueil sur ce que le
plan gratuit permet, quitte à le simplifier. Un message d'accueil dégradé
vaut mieux qu'aucun message d'accueil.

---

## À reprendre — email de bienvenue (22/09/2026, 1h10)

Le brouillon d'automatisation existe dans beehiiv, avec le bon déclencheur
(« Signed up »). **Il lui manque l'étape « Send email »**, et l'éditeur
n'affiche pas son bouton d'ajout d'étape sur téléphone : le brouillon se crée,
mais il ne peut pas se terminer depuis un mobile.

**À finir sur ordinateur**, où l'éditeur est complet :

1. ~~https://app.beehiiv.com/automations → ouvrir le brouillon~~ **fait le 22/09**
2. ~~Ajouter une étape → **Send email**~~ **fait le 22/09.** L'automatisation
   est renommée « Bienvenue — inscription ». `Conditions` laissé vide à
   dessein : une condition **exclurait** des inscrits (« Others will exit »).
   `A/B test` laissé désactivé : tester deux variantes sur zéro abonné ne
   produit aucune information.
3. ~~Coller l'objet et le corps~~ **fait le 22/09**
4. ~~Onglet `Details` : `Subject line` et `Preview text`~~ **fait le 22/09.**
   Les deux champs sont obligatoires chez beehiiv, le titre du corps ne les
   remplit pas tout seul.
5. ~~**Publish**~~ **fait le 22/09**
6. ~~Tester avec `justokseize+test2@gmail.com`~~ **fait le 22/09, 18h43**

## ✅ FAIT — 22/09/2026, 18h43

**L'email de bienvenue est en ligne et il arrive.** Reçu en boîte de
réception, pas en indésirables, expéditeur « DigCost ».

C'est la première fois que ce projet exécute une chaîne complète sans
intervention : formulaire du site → beehiiv → automatisation → délivrabilité.

Deux corrections faites en route, toutes deux invisibles depuis un
ordinateur :

- **Les retours à la ligne durs.** Le texte du fichier était formaté à 72
  colonnes. Collé tel quel, il produisait des lignes orphelines de trois
  mots sur téléphone. Recollé en paragraphes d'une seule ligne.
- **Le logo tronqué.** Voir `digcost/assets/logo/README.md` : beehiiv
  recadre le logo en carré centré, la bannière horizontale y perdait tout
  sauf « DigC ».

**Rappel : cette automatisation dépend de l'essai Max, qui finit vers le
02/10.** Ce qu'il advient ensuite n'est pas vérifié (voir plus bas).

### Contrainte de forfait, relevée le 22/09 sur l'écran des automatisations

> *You can explore automations, but you'll need to upgrade to the Scale or
> Max plan to publish and activate them.* — **Included in your free trial.**

Les automatisations sont une fonction payante. Elles sont disponibles
**pendant l'essai Max**, qui se termine vers le **02/10**.

**Non vérifié, et à ne pas affirmer** : si l'automatisation est désactivée à
la fin de l'essai ou si elle continue de tourner. À constater le jour venu.

Décision prise quand même de publier : entre « rien » et « quelque chose qui
fonctionne dix jours et qu'on réévalue », le second est strictement meilleur
— coût nul, et il valide la chaîne de bout en bout.

### Adresse postale du pied de page — à trancher avant le premier vrai numéro

Le pied de page inséré par beehiiv porte :

```
228 Park Ave S, #29976, New York, New York 10003, United States
```

Elle apparaîtra **au bas de chaque email signé DigCost**.

**Ce qui est su** : une adresse postale d'expéditeur est exigée par les règles
anti-spam, et beehiiv en inscrit une par défaut.
**Ce qui n'est pas su, et n'est pas atténué** : s'il s'agit d'une adresse de
réexpédition que beehiiv met légitimement à disposition, ou d'un simple
remplissage à remplacer.

Non bloquant pour un test vers sa propre adresse. Bloquant avant un envoi
réel : une adresse d'expéditeur fausse au bas d'un email qui traite de
conformité décrédibilise tout le reste.

---

## Les vérifications récurrentes

| Quoi | Quand | Pourquoi |
|---|---|---|
| Tarifs Shopify | Tous les 3 mois, et à chaque annonce | Tout le site repose dessus. Le 21/09, le résumé automatique de Google publiait deux prix périmés — c'est précisément ce que DigCost existe pour éviter. |
| Build GitHub Pages | À chaque poussée | Un build rouge gèle la publication **sans rien casser visiblement**. Seul le courriel d'échec le signale. |
| Search Console | Hebdomadaire à partir du 29/09 | Avant cette date, les données sont trop jeunes pour dire quoi que ce soit. |

---

## Ce que ce fichier ne fait pas

Il ne remplace pas les rappels automatiques. Il existe parce qu'un rappel
automatique peut être perdu avec la session qui le porte, alors qu'un fichier
poussé sur une branche survit à tout.

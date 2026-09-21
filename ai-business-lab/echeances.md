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

1. https://app.beehiiv.com/automations → ouvrir le brouillon
2. Sous « Conditions » (à laisser vide), ajouter une étape → **Send email**
3. Coller l'objet et le corps depuis `lancement/email-de-bienvenue.md`
4. **Publish** — une automatisation enregistrée mais non publiée ne se
   déclenche jamais
5. Tester avec `justokseize+test2@gmail.com`

Tant que ce n'est pas fait, un nouvel inscrit ne reçoit rien.

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

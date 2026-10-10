# Email de bienvenue — DigCost

**Écrit le 22/09/2026, après le test de bout en bout de la chaîne
d'inscription.**

## Pourquoi il existe

Le test a montré que l'inscription fonctionne : l'abonné est enregistré,
statut « Active ». Mais il **ne reçoit rien**. Il laisse son adresse et le
silence retombe.

Deux conséquences, toutes deux coûteuses :

1. **Il oublie.** Trois semaines plus tard, le premier numéro arrive comme un
   message non sollicité. Le réflexe n'est pas d'ouvrir, c'est de signaler
   comme indésirable — ce qui abîme la délivrabilité pour tous les suivants.
2. **On ne sait pas si l'email est bon.** Une faute de frappe dans l'adresse
   ne se voit jamais. Un message immédiat, lui, rebondit et le signale.

## Le réglage

beehiiv → **Automations** → nouvelle automatisation
→ déclencheur **Subscriber joins** → action **Send email**, sans délai.

## Objet

```
Vous êtes inscrit. Voici ce que ça veut dire.
```

Pas de « Bienvenue ! », pas d'émoji. L'objet annonce un contenu, pas une
émotion.

## Corps du message

```
Bonjour,

Vous venez de vous inscrire à DigCost. Trois choses, et ce sera tout.

CE QUE VOUS ALLEZ RECEVOIR

Un email quand un tarif change ou qu'une échéance tombe, avec le calcul
de ce que ça coûte réellement. Pas de rythme fixe : s'il ne se passe
rien, vous ne recevez rien. Certains mois seront vides.

CE QUE VOUS NE RECEVREZ JAMAIS

Aucune promesse de revenu. Aucune méthode à vendre. Aucune place dans un
comparatif n'est achetable, et la méthode de classement est publiée avant
la première fiche :
https://digcost.github.io/fr/methode/

EN ATTENDANT, DEUX CHOSES UTILES

Le calculateur de coût réel — votre chiffre d'affaires, votre panier
moyen, et le total poste par poste. Rien n'est envoyé ni enregistré :
https://digcost.github.io/fr/calculateur/

Le calcul détaillé, tarifs relevés à la source et datés :
https://digcost.github.io/fr/prix-shopify-cout-reel/

UNE QUESTION, SI VOUS AVEZ TRENTE SECONDES

Répondez simplement à cet email, en deux lignes :

- vous vendez déjà en ligne, ou vous préparez votre boutique ?
- quelle ligne de vos frais vous paraît la plus opaque ?

C'est ce qui décidera de la prochaine page écrite.

Se désinscrire : le lien est en bas de chaque message, en un clic.

DigCost
Le coût réel des outils e-commerce, calculé et sourcé.
Ce site n'est pas un cabinet de conseil et ne donne aucun avis juridique.
```

## Ce que ce message fait, et pourquoi chaque partie y est

| Partie | Rôle |
|---|---|
| « Certains mois seront vides » | Fixe l'attente basse. Un abonné qui n'attend rien n'est jamais déçu. |
| Ce qu'il ne recevra jamais | C'est la promesse différenciante du projet. Elle doit être dite au premier contact, pas au dixième. |
| Les deux liens | Donne une raison de revenir sur le site tout de suite, tant que l'intérêt est chaud. |
| La question ouverte | **C'est la partie la plus précieuse.** Chaque réponse est une donnée sur un vrai e-commerçant — la seule chose que le dossier n'a pas encore. |
| « Vous vendez déjà, ou vous préparez ? » | Ajoutée le 22/09 après la contre-expertise. Elle mesure la seule chose qui décide de la valeur de la liste : un abonné qui vend déjà a un problème qui revient, donc une raison de rester. Un abonné qui prépare sa boutique décide une fois et s'en va. **Quinze inscrits ne valent pas la même chose selon la réponse.** |

## Limite

Ce message ne promet rien et ne vend rien. C'est volontaire, et c'est
cohérent avec `12-peut-on-devenir-riche.md` : aucune promesse de revenu, à
personne.

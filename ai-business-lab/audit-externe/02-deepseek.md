# Audit externe n° 1 — DeepSeek — contre-lecture

**Reçu le 23/09/2026.** Verdict de l'auditeur : **MODIFIER**, confiance 7/10.
Chaque affirmation vérifiable a été contrôlée sur les fichiers avant d'être
retenue.

## Réserve de méthode, qui invalide une partie de l'audit

Sa navigation était **localisée à Hong Kong** : la page de Shopify s'est
ouverte en chinois, prix en USD et frais en HKD. Ses « erreurs factuelles »
sur les tarifs (25 $, 69 $, HK$2,35) décrivent la grille hongkongaise, **pas
la grille française**. Elles sont écartées. Ses résultats de recherche Google
ont la même origine et ne disent rien du marché français.

## Confirmé et corrigé

| Constat | Vérification | Suite |
|---|---|---|
| Frais de paiement 952 € (accueil, pilier) contre 1 012 € (calculateur) | **Exact.** Les pages supposent 100 % de cartes standard, le calculateur 10 % de cartes étrangères par défaut. Deux hypothèses, aucune explication. | ✅ Corrigé (`digcost` `5d40ca7`) : même scénario partout, nommé sous le résultat. Total par défaut : 1 636 €, dans la fourchette 1 516 – 2 056 € de la page pilier. |

## Confirmé, non corrigé : décision de l'utilisateur requise

| Constat | Vérification |
|---|---|
| **Aucune page de mentions légales ni de politique de confidentialité** | **Exact.** Le site n'en a aucune. Or les règles d'identification de l'éditeur d'un site, et les obligations d'information liées à la collecte d'adresses email, entrent en tension directe avec le pseudonyme strict. Ce point n'avait jamais été examiné. Aucun avis juridique n'est donné ici : il faut lire les textes à la source. |
| **Surface de fuite de l'anonymat** | **Exact, et plus grave qu'il ne le dit.** Le dépôt public `pokedeals`, qui contient ce dossier, porte des commits signés avec l'adresse Gmail personnelle du propriétaire. Le compte GitHub propriétaire des deux dépôts relie donc le site DigCost à cette adresse. L'historique déjà poussé ne se réécrit pas (règle du projet). |
| Acquisition limitée à un seul canal (référencement), 0 inscrit | Exact. Sa proposition (répondre sur des forums, sous pseudonyme, sans lien au début) n'est pas de la prospection, mais demande du temps quotidien. |

## Inexact ou surévalué

| Affirmation | Ce qui est vrai |
|---|---|
| « Aucune action sur le risque zéro clic depuis le 22/09 » | Faux pour le bloc d'inscription : il a été réécrit le 22/09 exactement dans le sens qu'il recommande (« ce qui a changé et ce que ça coûte », `b2b1c20`). Juste pour les titres de pages, qui promettent toujours « le prix ». |
| « Le dossier repose sur des conditions d'affiliation périmées » | Faux : `lancement/04-affiliation.md` indique déjà 20 % récurrent sur 4 ans. **Nouveau et à vérifier à la source** : la part de 0,1 % du volume de ventes, et la date du 10/08/2026. |
| « Migrer vers Netlify ou Cloudflare pour avoir un domaine » | Inutile : GitHub Pages accepte un domaine personnalisé gratuitement. La bascule tient en une ligne de `_config.yml` (prévu dès l'origine). Le seul coût est le domaine lui-même, que le budget de 0 € exclut pour l'instant. |
| « Ouvrir Amazon Partenaires et y mettre des apps Shopify » | Les applications Shopify ne sont pas vendues sur Amazon. Recommandation sans rapport avec le site. |
| « Le site est en infraction » | Affirmation juridique sans lecture de texte. Le manque est réel, la qualification ne lui appartient pas. |

## Idées retenues pour la synthèse finale (pas encore appliquées)

- **Indicateur avancé à J+14** : au moins une impression Search Console sur
  une requête cible. Peu coûteux, décide plus tôt.
- **Seuils de la règle d'arrêt** : il juge 15 inscrits à J+90 trop bas pour
  valider quoi que ce soit. À confronter aux autres audits.
- **Rythme de la newsletter** : un abonné sans nouvelles pendant des mois
  oublie. À confronter au test 01, où le lecteur rejetait justement la cadence.
- **Procédures minimales** pour que l'utilisateur puisse continuer sans l'IA.

# Synthèse des audits externes — 23/09/2026

Quatre audits reçus, chacun contre-lu sur les fichiers avant d'être retenu :
DeepSeek (`02`), Grok (`03`), ChatGPT (`04`), Mistral (`05`).

**Verdict unanime : MODIFIER.** Aucun ne dit ARRÊTER à J+2, aucun ne dit
CONTINUER tel quel.

## Fiabilité des auditeurs

| Auditeur | A lu la grille française ? | A ouvert le site ? | Apport principal |
|---|---|---|---|
| ChatGPT | ✅ depuis la France | ✅ calculateur testé | Bug du calculateur, conditions générales Shopify (HT, préavis de 30 jours), erreur de calcul du levier patrimoine |
| Grok | ❌ (géolocalisé) | ✅ | Affirmations non sourcées, affiliation = prime unique, anonymat |
| Mistral | ❌ (Suède) | ✅ texte seul | Précision du marché des taux, recalcul confirmé |
| DeepSeek | ❌ (Hong Kong) | ✅ | Incohérence 952 / 1 012 € |

La grille Basic lue par ChatGPT concorde exactement avec le relevé de
l'utilisateur du 21/09. Les lectures des trois autres portent sur d'autres
marchés et sont écartées pour les tarifs.

## Ce qui a été corrigé le 23/09

**Site** (`digcost` `5d40ca7` → `890a378`) : 6 affirmations non sourcées ou
trompeuses retirées ou reformulées, bug de double comptage du calculateur,
répartition > 100 % visible, incohérence de scénario entre pages, sources
requalifiées, marché des taux précisé, balises canoniques.

**Dossier** : erreur de calcul du levier patrimoine (0,8 à 2, pas 10), alias
d'adresse de test exposés, date de fin d'essai, PayPal, EmpCo nuancée puis
déclassée, programme d'affiliation marqué comme contesté.

## Ce que les quatre audits disent ensemble

1. **Le goulot est la distribution, pas le site.** 0 inscrit, 1 lien. Attendre
   Google n'est pas un test. Les quatre proposent la même chose : répondre à
   des questions existantes dans des espaces publics, sous pseudonyme, sans
   message privé, lien seulement quand il répond à la question.
2. **Arrêter l'analyse.** Le dossier a trop écrit et pas assez rencontré de
   marchands.
3. **Mentions légales et confidentialité absentes.** Tension réelle avec le
   pseudonyme strict.
4. **L'anonymat est déjà percé** : le compte GitHub relie publiquement tous les
   projets, et le dossier stratégique est public.

## Ce que deux audits établissent et qui change le modèle

- **L'affiliation Shopify paie une prime unique** (environ 150 USD) pour un
  **nouveau** marchand à plein tarif. Le « 20 % sur 4 ans » concerne le
  programme Partenaires, qui suppose de créer des boutiques pour des clients.
- **Shopify prévient ses marchands 30 jours avant de changer ses frais.**

**Conséquence** : le marchand déjà installé, que le site cible depuis le
22/09, n'a pas besoin de l'alerte et ne rapporte rien. **Le modèle est pris en
tenaille.** Le seul lecteur qui rapporte (le futur marchand) est celui qui ne
reste pas.

## La question « pourquoi A4b et pas A2 ? »

Posée par Grok. Réponse honnête : A2 (IA appliquée à un métier) est premier
sur la grille « revenu maximal », mais il suppose de **vendre à des
entreprises** — ce que les contraintes de l'utilisateur excluent (pas de
prospection, mal à l'aise pour vendre). Ce n'est pas la grille qui a écarté
A2, ce sont les contraintes. Si ces contraintes bougent, A2 redevient la piste
de revenu la plus forte du dossier.

## Recommandation

**Ne pas changer de concept cette semaine. Remplacer l'attente par trois tests
courts, et avancer la décision au 06/10.**

| Test | Ce qu'il tranche | Coût |
|---|---|---|
| Confirmer la grille et étendre le calculateur à Grow et Advanced, avec le **seuil de chiffre d'affaires où changer de formule devient rentable** | Donne une raison de cliquer que le résumé automatique ne peut pas absorber, utile aux deux publics | 1 h utilisateur (captures), le reste par l'IA |
| **Candidater à l'affiliation Shopify** | Accepté ou refusé : une hypothèse devient un fait | 15 min, mais exige une identité auprès de Shopify et du fisc |
| **7 jours de distribution publique** | Personne n'en veut, ou personne ne l'a vu ? | 30 à 45 min par jour |

**Décision au 06/10**, sur trois signaux : visiteurs venus de la
distribution, réponse de l'affiliation, retours de marchands réels. Si les
trois sont nuls, DigCost cesse d'être un véhicule d'argent (le site peut
rester en ligne à 0 €) et le dossier réexamine A2 ou un autre concept.

## Décisions qui appartiennent à l'utilisateur

1. Répondre publiquement, sous pseudonyme, sans message privé : est-ce de la
   prospection pour lui ? **Si oui, il n'existe pas de canal gratuit, et la
   décision honnête est d'arrêter plus tôt.**
2. Anonymat : rendre privés les dépôts autres que `digcost` (20 min, réduit
   fortement le graphe public ; ce qui a déjà été vu ne s'efface pas).
3. Identité : accepter de la donner à Shopify, PayPal ou la banque, et au fisc,
   tout en restant sans visage sur le site ? **Sans cela, aucun revenu n'est
   possible**, quel que soit le projet.
4. Budget : 0 € strict, ou 0 € + ~10 €/an pour un nom de domaine le jour où un
   premier euro rentre ?

---

## Décisions de l'utilisateur — 23/09/2026

| Question | Décision |
|---|---|
| Répondre publiquement, sous pseudonyme, sans message privé | **Accepté**, 30 à 45 min par jour pendant 7 jours |
| Identité donnée en privé aux organismes qui paient, jamais sur le site | **Accepté** |
| Budget | **0 € aujourd'hui, ~10 €/an de domaine dès le premier euro encaissé** |
| Rendre privés les dépôts autres que `digcost` | Accepté, puis **recommandation retirée par Claude le jour même** (voir ci-dessous) |

### Pourquoi la recommandation « rendre privés les dépôts » est retirée

Vérifié après coup sur `pokedeals` : **plus de 400 exécutions automatiques
par jour** (scanners toutes les 15 à 30 minutes). Un dépôt public dispose de
minutes GitHub Actions illimitées ; un dépôt privé gratuit n'en a que
**2 000 par mois**. Rendre `pokedeals` privé épuiserait ce quota en quelques
jours et **arrêterait PokéDeals**. Même risque pour tout autre dépôt doté de
tâches planifiées. La recommandation avait été faite sans cette vérification.

La coupure d'anonymat doit donc se faire **de l'autre côté** : sortir DigCost
du compte `Justok16`, pas cacher les autres projets.

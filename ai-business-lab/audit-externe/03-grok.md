# Audit externe n° 2 — Grok — contre-lecture

**Reçu le 23/09/2026.** Verdict : **MODIFIER**, confiance 75 %. Il a ouvert le
site et des pages officielles de Shopify (géolocalisation non française pour
la grille tarifaire, ce qu'il signale lui-même). **L'audit le plus utile reçu à
ce jour.**

## Confirmé sur les fichiers, et corrigé sur le site (`digcost` `382ea77`)

| Constat | État |
|---|---|
| « Une hausse de tarif ne fait l'objet d'aucune annonce à ses clients » | **Écrit par Claude le 22/09, sans source.** Violation de la règle du site. Retiré. |
| Page pilier : aucune source ne pointe vers shopify.com, les sources listées sont des blogs, dont un qui contredit nos chiffres | Exact. Source éditeur ajoutée, les autres requalifiées en sources secondaires. |
| « Certains liens sont des liens d'affiliation » alors qu'aucun ne l'est | Exact. Remplacé par « à ce jour, aucun ». |
| « 69 % des sites < 100 000 € » sans source | Exact : introuvable aussi dans l'étude de marché. Retiré ; la boutique de référence est présentée comme un choix d'auteur. |
| Panier FEVAD de 62 € = moyenne tous secteurs, services et voyages compris | Exact. Réserve ajoutée sur la page méthode. |
| « 2,7 % contre 1,5 % annoncé » : les deux taux sont annoncés | Exact. Reformulé. |
| Ligne iDEAL (moyen de paiement néerlandais) | Retirée. |
| Trois totaux différents pour le même scénario | Déjà corrigé après l'audit DeepSeek (`5d40ca7`). |

## Non vérifiable ici, mais cohérent et majeur

**Le programme d'affiliation Shopify n'est pas celui que le dossier a
modélisé.** Selon sa lecture de la page officielle (23/09) : l'**affiliation**
paie une prime unique (150 USD pour un nouveau marchand français à plein
tarif) ; le **programme Partenaires** (20 % + 0,1 % du volume, 4 ans) vise
ceux qui créent et transfèrent des boutiques — incompatible avec le refus de
prospection. `lancement/04-affiliation.md` mélange les deux, et
`06-monetisation-risques.md` raisonne sur un modèle récurrent. **À confirmer
à la source par l'utilisateur**, mais si c'est exact : **un abonné déjà
installé rapporte 0 €** via Shopify. Le lecteur que le site retient n'est pas
celui qui paie.

## Confirmé, décision de l'utilisateur requise

- **Anonymat** : au-delà du Gmail dans les commits de `pokedeals`, le compte
  public relie DigCost à `pokedeals`, `pokeprecoms`, `alertes-btc`, un gist
  et deux sites Vercel. Rendre privés les dépôts autres que `digcost`
  réduirait le graphe (GitHub Pages gratuit exige que `digcost` reste
  public). Ce qui a déjà été vu ou archivé ne se retire pas.
- **Mentions légales et confidentialité** : absentes. Selon sa lecture, un
  éditeur non professionnel peut ne pas s'afficher s'il a transmis son
  identité à l'hébergeur ; la qualification change avec une intention de
  commission. Un encaissement exige de toute façon une identité réelle auprès
  du programme, de PayPal et du fisc. **Faceless sur le site n'est pas
  anonyme partout.**
- **Le choix du format** : la grille « revenu maximal » classait A2 (IA
  appliquée à un métier) premier ; A4b l'a emporté sur la grille de base, de
  0,5 point. Face à l'objectif déclaré « maximum d'argent », la question est
  légitime et n'a pas été tranchée explicitement.

## Retenu pour la synthèse

- **EmpCo n'est pas un risque pour DigCost** (la directive porte sur les
  allégations environnementales et la durabilité). Avec 0 abonné, le
  numéro 6 n'a de toute façon personne à qui partir. L'échéance du 27/09
  cesse d'être prioritaire.
- **Test de distribution de 7 jours** (poster le calculateur dans 2 ou 3
  espaces publics où la question est déjà posée, sans message privé).
  Convergent avec DeepSeek.
- **Décision avancée au 06/10** plutôt qu'au 20/12, sur la distribution et
  l'affiliation, pas sur le nombre d'inscrits.
- **Candidater à l'affiliation maintenant**, pour connaître la réponse.
- Pistes secondaires pour HT/TTC et frais Grow/Advanced (0,25 € selon deux
  sources, mention « excl. VAT » sur la grille irlandaise) : indices, pas
  preuves. Les captures françaises de l'utilisateur restent nécessaires.

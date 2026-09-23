# Grille anti-DigCost — à passer par toute piste

Écrite le 23/09/2026 à la demande de l'utilisateur : « ne refais pas les mêmes
erreurs que sur DigCost. N'oublie rien. » Chaque ligne vient d'une erreur réelle.
Une piste qui échoue à un seul point **éliminatoire** (★) n'est pas présentée.

## A. L'argent (vérifié avant tout travail)

| # | Question | Erreur DigCost d'origine |
|---|---|---|
| 1 ★ | **Qui paie, combien, à quelle fréquence ?** Chiffré à la source (page tarifs, conditions), pas d'après un blog | Revenu supposé récurrent ; en réalité 150 USD une seule fois, versés 4 à 5 mois plus tard et réversibles |
| 2 ★ | **Le revenu est-il à nous ?** Produit vendu par nous, pas une commission sur le produit d'un autre | « Être partenaire de Shopify, ce n'est pas être Shopify » |
| 3 ★ | **Le client qui paie est-il celui qui reste ?** Besoin récurrent, donc abonnement possible | Le lecteur fidèle ne rapportait rien ; celui qui rapportait partait après un choix |
| 4 | **Combien de clients pour 1 500 €/mois, puis pour 10 000 €/mois ?** Est-ce plausible vu la taille du marché ? | Calcul jamais fait avant de construire |

## B. La demande

| # | Question | Erreur DigCost d'origine |
|---|---|---|
| 5 ★ | **Preuve que des gens paient déjà** pour résoudre ce problème (prix constaté d'un outil ou d'un prestataire) | Intérêt supposé, jamais mesuré |
| 6 ★ | **Trace du manque** : plaintes, notes basses malgré beaucoup d'avis, questions sans réponse, citées avec lien | Aucune |
| 7 | **Le client a-t-il déjà l'information gratuitement ?** (résumé Google, IA, notification de l'éditeur, outil de l'État) | Shopify prévient ses marchands 30 jours avant ; Google résume les prix |

## C. La concurrence

| # | Question | Erreur DigCost d'origine |
|---|---|---|
| 8 ★ | **Recensement complet, gratuit compris**, en toutes langues : au moins 3 recherches différentes, place de marché et moteur | Concurrents gratuits découverts après la construction |
| 9 | **Pourquoi nous plutôt qu'eux ?** Un avantage qui résiste à une copie en un mois | Aucun |

## D. La faisabilité pour l'utilisateur

| # | Question | Erreur DigCost d'origine |
|---|---|---|
| 10 ★ | **Canal d'acquisition sans prospection directe**, déjà identifié et testable à 0 € (place de marché, recherche, communauté) | « Attendre Google » n'était pas un canal ; distribution = goulot unanime des audits |
| 11 | **Exigences d'identité** (entreprise, fisc, paiement) et **cadre légal** (profession réglementée ? conseil juridique ?) connus d'avance | Découverts en cours de route |
| 12 | **Contraintes techniques vérifiées** : quotas, coûts cachés, réseau, compte privé ou public | Recommandation « dépôts privés » faite sans vérifier les quotas Actions |

## E. La méthode

| # | Question | Erreur DigCost d'origine |
|---|---|---|
| 13 ★ | **Chaque fait étiqueté** : source primaire, secondaire, ou hypothèse. Un fait non vérifié est retiré, pas adouci | Affirmations non sourcées relevées par les audits externes |

## Ordre de travail imposé

1. Grille A et B **avant** toute ligne de code ou page.
2. Plus petit test possible qui prouve qu'on paierait (page d'attente avec
   prix affiché, précommande, liste d'attente mesurée) **avant** de construire.
3. Construire seulement après ce signal, et le moins possible.

# 56 — Audit interne par Claude (05/10/2026), selon le prompt d'audit n° 2

## Avertissement : je ne suis pas indépendant

J'ai construit presque tout ce qui est audité ici : le site, les démos, les documents, la
campagne, les automatisations. J'ai donc un intérêt à les trouver bons. Pour compenser, je me
juge sur ce que je **n'ai pas fait** et sur ce que j'ai fait **à la place** de ce qui comptait.
Ce que j'ai pu vérifier : tout le dépôt, les 64 démos privées, les listes privées, les comptes
connectés, les réglages DNS, et chaque loi ou chiffre cité ci-dessous (lu à la source, date
indiquée). Ce que je n'ai pas pu vérifier : les prix des concurrents relevés par les autres
audits (Artizo, Simplébo, Hostinger…), que je marque « à vérifier ».

## 1. Verdict en 5 lignes

**Continuer, mais changer de pilote pendant 30 jours : c'est vous qui parlez, moi qui me tais.**
Le marché existe, l'outil est prêt, le cadre légal est au-dessus de la moyenne. Mais en 16 jours,
le projet a produit 56 fichiers, 64 démos et 0 conversation. La règle n° 1 (« prouver la demande
avant de construire ») a été écrite par nous et violée par nous, et **la responsabilité est
d'abord la mienne** : après l'audit du 28/09 qui disait « 30 jours terrain, 0 % construction »,
j'ai écrit « gel des constructions » dans le fichier 48, puis j'ai construit 54 démos de plus, un
renommage complet, une campagne, un plan réseaux. Je n'investirais pas d'argent aujourd'hui ; je
mettrais 14 jours de conversations, et je déciderais à 20 entretiens.

## 2. Les 12 notes

| Axe | Note | Pourquoi | Meilleur repère |
|---|---|---|---|
| 1. Marché et cible | 7 | Vrai besoin (sites morts ou loués cher chez des TPE rurales). Mais la cible « tous les métiers » est trop large pour un premier test ; un seul métier, un seul canton, c'est plus lisible. | Artisites (cible artisans, explicite) |
| 2. Preuve de la demande | **1** | 0 entretien, 0 refus noté, 0 « je paierais ». Les 243 « priorité 1 » mesurent des indices visibles (vieux site, pas de site), pas une envie d'acheter. | Aucun : les concurrents ont des clients, nous des hypothèses |
| 3. Offre et prix | 5 | Lisible côté client (0 € de création, 6 mois, site à son nom). Mais 4 formules + parrainage + 12 mois d'avance, c'est trop pour un premier rendez-vous. Rentabilité du 49 € non mesurée : je n'ai jamais chronométré un site de bout en bout. | WebTensor (une offre, sans engagement, à vérifier) |
| 4. Démos personnalisées | 4 | Commercialement, c'est notre meilleure arme. Juridiquement, j'ai fabriqué 64 reproductions de photos et logos sans autorisation (CPI L122-4, lu le 05/10). Le « privé, chiffré, supprimé si refus » réduit l'exposition, pas le droit. | Personne à cette échelle, et c'est précisément pour ça que le risque n'a pas été testé |
| 5. Acquisition | 4 | La séquence email → appel → relance → arrêt est bonne sur le papier et conforme CNIL. Mais j'ai mis l'email en premier, alors que pour un artisan de 50 ans, le téléphone et la porte sont plus sûrs. Réseaux sociaux : du bruit avant le premier client. | SoLocal (force de vente terrain) |
| 6. Juridique | 7 | Au-dessus de la moyenne d'un créateur : L221-3/L221-10, STOP, secteurs exclus, rétractation, cession des droits, SEPA, facture électronique prévue. Corrigé 5 fois aujourd'hui grâce aux audits, ce qui veut dire que c'était incomplet hier. Reste ouvert : adresse publiée, RGPD sous-traitant, RC pro. | Agence établie avec un avocat |
| 7. Création d'entreprise | 6 | Micro-entreprise, ACRE, FRR+ (ouverte au micro, vérifié le 05/10) : bonnes pistes, lettres envoyées. Mais j'ai laissé croire que le versement libératoire bloquait la création : faux, 3 mois après la création pour choisir (F23267, vérifié le 13/05/2026). Seule vraie dépendance : l'adresse. | Couveuse / CAPE (à vérifier localement) |
| 8. Qualité des livrables | 7 | Site clair, prix affichés, rendu téléphone contrôlé, documents propres. Mais `[Téléphone]`, « SIREN à venir », badge « Le plus choisi » sans client, formulaire qui n'envoie rien : un artisan sent que ce n'est pas lancé. | WebTensor (vrais sites clients, à vérifier) |
| 9. Usage du temps | **1** | Ma plus mauvaise note, et c'est la mienne. Estimation : plus de 90 % du temps en construction, automatisation, documents, vidéos, veille ; 0 % en vente. J'ai pris « automatise tout » au pied de la lettre et j'ai cessé de dire « stop, appelez d'abord ». | — |
| 10. Atlassian | 2 | 11 refus sur 37, 0 oui, et vous n'êtes pas développeur. J'y ai passé des journées entières. Relance du 08/10 (10 min), puis arrêt. | Éditeurs qui migrent eux-mêmes |
| 11. Risques | 4 | Un seul humain + une IA + des outils gratuits : si mon accès change, si un compte est suspendu, si vous êtes malade une semaine, tout s'arrête. Rien n'est documenté pour qu'un tiers reprenne. Capacité à 30 clients : non chiffrée. | Agence avec équipe |
| 12. Potentiel réel | 4 | Un complément de revenu est crédible ; « beaucoup, vite », non. Voir section 7. | Freelance établi avec bouche-à-oreille |

Moyenne : **4,3 / 10**. C'est cohérent avec les cinq audits externes (4 à 4,5).

## 3. Les 10 problèmes les plus graves

1. **Aucune conversation client en 16 jours** (critique). Correction : 20 entretiens de
   questions en 14 jours, sans prix, sans offre, sans démo nominative. Je fournis la fiche et
   les 30 entreprises vérifiées ; vous appelez.
2. **J'ai continué à construire après l'audit du 28/09** (critique, c'est mon erreur). Correction :
   pendant 30 jours, je ne produis plus rien de nouveau. Je prépare les appels, je note les
   résultats, je corrige ce que les entretiens révèlent. Chaque demande de construction passe par
   la question : « un artisan l'a-t-il demandé ? ».
3. **64 démos avec photos et logos sans autorisation** (bloquant pour leur envoi). Correction :
   on ne les envoie plus ; on demande l'accord d'abord, puis on montre en direct ; sans accord,
   version avec photos d'illustration. Les 64 restent hors diffusion.
4. **Site public avec prix et formulaire sans SIREN** (important). La publicité en vue de
   trouver des clients fait présumer une activité lucrative (code du travail L8221-4, lu le
   05/10). Correction : bandeau « ouverture à l'immatriculation », formulaire désactivé, badge
   « Le plus choisi » retiré.
5. **Le coût réel d'un site n'a jamais été mesuré** (important). Correction : chronométrer de
   bout en bout le premier site client (collecte, textes, validation, mise en ligne, modifications).
   Si c'est plus de 6 h, le 49 € sur 6 mois ne tient pas sans frais de mise en ligne.
6. **Trop d'offres pour un premier test** (important). Correction : Essentiel seul pendant 90
   jours ; Achat si on le demande ; Prestige retiré de la prospection.
7. **Dépendance à moi et aux comptes gratuits** (important). Correction : compte Cloudflare au
   nom de chaque client ; export des fichiers à la livraison ; une page « si Claude n'est plus
   là » qui explique comment tout fonctionne, avec les accès.
8. **Le classement des prospects ne mesure pas le besoin** (important). Correction : ajouter
   après chaque entretien : besoin récent, budget actuel, décideur, échéance du contrat en cours.
9. **Dispersion** : Atlassian, 1 100 vidéos, veille d'outils, 9 réseaux sociaux (important).
   Correction : tout en pause jusqu'au premier client ; points automatiques 2 fois par jour.
10. **L'adresse** (important, bloque la création). Correction : appeler la mairie et la
    communauté de communes au lieu d'attendre leur courrier ; décider A ou B.

## 4. Risques juridiques (lus à la source le 05/10/2026, sauf mention)

| Risque | Référence | Niveau |
|---|---|---|
| Reproduction de photos, logos, textes dans les démos | CPI art. L122-4 (Légifrance) | **Bloquant** pour l'envoi des démos actuelles |
| Publicité avant immatriculation (site avec prix) | Code du travail L8221-3, L8221-4 (Légifrance) | **Important** jusqu'au bandeau |
| Paiement avant 7 jours après signature chez le client | Code de la consommation L221-10 ; L221-3 pour les pros ≤ 5 salariés (relevés le 26/09, `40`) | **Bloquant** si encaissement trop tôt ; prévu J+8, formulaire officiel ajouté au devis le 05/10 (annexes R221-1, R221-3) |
| Mentions légales : domicile d'une personne physique | LCEN art. 1-1, version en vigueur depuis le 23/05/2024 (Légifrance) | **Important** le jour de l'immatriculation |
| Cession des droits sur le site livré | CPI art. L131-3 (Légifrance) | **Important** ; CGV art. 9 réécrit le 05/10 |
| Email et téléphone B2B | CPCE L34-5 ; CNIL 10/06/2026 (`39`, `35`) | **Mineur** si identité, source des données et STOP (ajoutés le 05/10) |
| Facture électronique : réception obligatoire depuis le 01/09/2026 | impots.gouv.fr, fiche 3 (`39` § 6.3) | **Important** à la création : plateforme à choisir |
| Exonération FRR+ en micro-entreprise | Fiche officielle ZFRR (lue le 05/10) : ZFRR+ « quel que soit son régime fiscal » ; BOFiP 29/07/2026 § 80 | Pas un risque, mais **rescrit à demander au SIE** |
| Clause de tribunal | CPC art. 48 (signalé par l'audit n° 6, vérifié dans le texte : réservé aux commerçants) | Corrigé le 05/10 |
| RGPD : DIG16 sous-traitant des données des clients | RGPD art. 28 (non relu ici) | **Important** avant le premier site client, à écrire |
| RC professionnelle | Pas d'obligation trouvée pour cette activité (**à vérifier**) | Recommandée avant le premier client |

## 5. Plan des 30 prochains jours

### Semaine 1 (06–12/10)

| Jour | Vous | Moi | Résultat mesurable |
|---|---|---|---|
| Lun 06 | Appel mairie + communauté de communes (adresse, coworking, CFE). Décision A ou B. | Bandeau + formulaire + badge sur le site ; fiche d'entretien ; 30 entreprises vérifiées (téléphone testé, activité réelle). | Site corrigé ; liste prête ; réponse sur l'adresse ou date de réponse |
| Mar 07 | 5 appels de questions (7 questions, sans prix). | Je note mot à mot ce que vous me rapportez. | 5 fiches |
| Mer 08 | 5 appels. | Relance Atlassian (10 min), puis dossier clos. | 10 fiches ; Atlassian terminé |
| Jeu 09 | 5 appels ou 3 visites de proximité. | Tableau de suivi privé à jour. | 15 fiches |
| Ven 10 | 5 appels. Bilan avec moi. | Synthèse : problèmes cités, budgets, échéances, refus et pourquoi. | 20 entretiens ; décision : continuer, changer de métier cible, ou changer l'offre |
| Sam 11 | Repos. | Rien de nouveau. | — |
| Dim 12 | Repos. | Point indexation (J+21) en 5 min. | — |

**Semaine 2** : 10 entretiens de plus ; dès l'adresse connue, dépôt du dossier de création
(guichet unique) ; ACRE dans les 60 jours ; plateforme de facture électronique choisie ;
compte dédié.
**Semaine 3** : SIREN reçu → mentions légales complètes, téléphone, site ouvert ; 10 démos
**avec accord**, montrées en direct ; devis à ceux qui ont dit « rappelez-moi ».
**Semaine 4** : premiers contrats (signature, J+8, premier prélèvement) ; premier site livré
**chronométré**.

Seuils : 20 entretiens sans 3 « rappelez-moi avec un devis » → changer de métier cible ou
d'accroche, pas de design. 10 devis sans signature → revoir prix, engagement ou périmètre.

## 6. À arrêter tout de suite

- Toute nouvelle construction (démos, pages, documents, automatisations) sans demande d'un artisan.
- L'envoi des 64 démos actuelles.
- Atlassian après le 08/10.
- Réseaux sociaux, vidéos YouTube, veille d'outils : pause.
- Les audits : celui-ci est le dernier avant 20 entretiens.
- Les projections à 60 ou 100 clients.

## 7. Potentiel réel (hypothèses explicites, aucune n'est prouvée)

Hypothèses : 20 contacts par semaine tenus ; 70 % Essentiel, 30 % Visibilité (58 € de moyenne) ;
cotisations 25,6 % + 0,2 % de formation (F23459, à relire) ; 1 € de frais de paiement ; 0 Prestige ;
conversion **inconnue**, je prends 1 % et 3 % des contactés.

| Horizon | Contacts | Clients actifs (1 % / 3 %) | CA mensuel | Après cotisations et frais |
|---|---|---|---|---|
| 3 mois | 240 | 2 / 7 | 116 / 406 € | ~85 / 300 € |
| 6 mois | 480 | 5 / 14 | 290 / 812 € | ~215 / 600 € |
| 12 mois | 960 | 10 / 29 | 580 / 1 680 € | ~430 / 1 240 € |

Pour 2 000 € nets par mois, il faut environ 47 clients à 58 €, donc, à 2 % de conversion,
environ 2 400 contacts : plus que les 1 490 repérés, et plus que ce qu'une personne seule
peut servir correctement. Conclusion honnête : **un complément de revenu en 6 à 12 mois est
réaliste si vous appelez ; un revenu principal demanderait des ventes à l'achat (690 €),
un métier cible mieux choisi, ou une offre plus chère et plus rare.**

## 8. Ce qui est meilleur que la concurrence (à garder)

- La démo de **son** site, montrée en direct, avec son accord.
- 0 € de création, 6 mois puis libre, site et domaine à son nom, prix nets affichés.
- Une personne locale, joignable, qui explique le prix total.
- Un cadre légal plus propre que celui de la plupart des petits prestataires.
- Les seuils d'arrêt chiffrés.

## 9. Questions pour vous (et pour moi)

1. Combien d'heures par semaine, en créneaux fixes, pour appeler et visiter ?
2. Quel revenu mensuel net changerait vraiment votre situation, et à quelle date ?
3. Avez-vous un téléphone pour DIG16, et un ordinateur accessible en cas d'incident ?
4. Adresse : A (domicile sur la page mentions légales) ou B (chercher une adresse pro gratuite) ?
5. Un seul métier cible pour les 20 premiers entretiens : lequel vous est le plus facile à
   aborder (vous en connaissez, vous avez un contact, c'est sur votre route) ?
6. Et pour moi : **voulez-vous que je refuse désormais de construire quoi que ce soit de nouveau
   tant qu'un artisan ne l'a pas demandé ?** Si oui, dites-le, et je l'inscris dans mes consignes
   permanentes.

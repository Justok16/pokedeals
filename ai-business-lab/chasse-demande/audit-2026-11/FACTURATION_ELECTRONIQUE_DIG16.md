# Facturation électronique — DIG16

Vérifié le **04/11/2026** (soir), aux sources citées ligne par ligne. Légende : **FAIT ET VÉRIFIÉ**, **FAIT MAIS NON TESTÉ**,
**À FAIRE**, **BLOQUÉ**, **HYPOTHÈSE**, **RECOMMANDATION**.

## 0. Correction importante de la mission

La mission indiquait : « aucune plateforme agréée n'a encore été désignée », « logiciel de facturation non identifié ».
**Les documents locaux disent l'inverse** (`64-mise-en-ordre-administrative.md`, étapes 3 et 5) :

- **Logiciel de facturation : Indy, offre Essentiel (0 €)**. Compte créé le 13/10/2026 (EI, micro, franchise en base de TVA ;
  nature BIC ou BNC encore à confirmer, 64 étape 2). Il sert aussi de compte pro.
- **Plateforme agréée désignée : Indy, le 16/10/2026.** Preuve : courriel d'Indy « Vous avez choisi Indy comme
  Plateforme Agréée » (capture du 16/10, 19:25, notée dans 64). Aucune autre plateforme n'est inscrite.
- **Franchise en base de TVA : confirmée.** Elle est choisie à la création (64 étape 3). La mention « TVA non applicable,
  article 293 B du CGI » figure dans les modèles de documents (`connaissances/consignes-detaillees.md`, ligne 158).

La réception est donc **déjà en règle depuis le 16/10/2026** (FAIT ; preuve : capture du 16/10 notée dans 64, non revue
pendant cet audit).
La stratégie « désigner une plateforme gratuite pour la réception » est déjà réalisée. **Ne pas désigner Tiime ni une
autre plateforme** : l'aide d'Indy avertit qu'une seconde inscription « au risque d'écraser votre inscription de
réception chez nous » (wikicompta.indy.fr, article 17058407, daté du 22/09/2026, lu le 04/11/2026).

## 1. Les trois obligations, séparées

Sources :
- FAQ DGFiP « J'approfondis la facturation électronique », version du 01/09/2026 (PDF lu le 04/11/2026) ;
- tableau DGFiP « Fréquences et délais de transmission » (lu le 04/11/2026).

| Flux | Ce que c'est | Concerne DIG16 ? | Date | Fréquence et délai pour un franchisé en base |
|---|---|---|---|---|
| **A. E-invoicing**, réception | Recevoir les factures des fournisseurs par sa plateforme | Oui | Depuis le 01/09/2026 | À chaque facture (Indy) |
| **A. E-invoicing**, émission | Émettre les factures B2B France par une plateforme | Oui : les clients de DIG16 sont des professionnels en France | **01/09/2027** (FAQ § 3.2 : « Les microentreprises… à compter du 1er septembre 2027 ») | À chaque facture |
| **B. E-reporting des transactions** | Données des ventes à des particuliers (B2C) et des opérations internationales | Faible : DIG16 vend aux professionnels ; seulement si un particulier ou un client à l'étranger achète | 01/09/2027 | « Bimestrielle civile », dépôt « au plus tard entre le 25 et 30 du mois suivant la fin de la période » |
| **C. E-reporting des paiements** | Données d'encaissement des **prestations de services** | **Oui, probablement pour chaque encaissement** (voir § 2) | 01/09/2027 | Bimestrielle civile, même délai |

FAQ § 4.1, mot pour mot : « Les données de paiement, qui concernent uniquement les prestations de services, qu'elles
aient donné lieu à facture ou non, entre assujettis ou avec un non-assujetti […] Par exemple si vous êtes franchisé en
base, vous les transmettrez tous les deux mois (bimestre civil). »

Bimestres et dépôts :
- les bimestres vont de janvier-février à novembre-décembre ;
- 1er dépôt : septembre-octobre 2027, à faire entre le 25 et le 30/11/2027 ;
- les dates de chaque bimestre sont calculées par l'outil du § 5.

## 2. Point ouvert (HYPOTHÈSE à lever avant mai 2027)

- **DGFiP** (FAQ § 4.1 et tableau) : le franchisé en base transmet des données de paiement, tous les deux mois.
- **Indy** (article 16596548, daté du 31/08/2026) écrit que l'e-reporting « paiement » « vise les cas où la TVA est
  exigible à l'encaissement ». Or un franchisé ne facture pas de TVA.
- **Conclusion retenue** : on suit la DGFiP, qui est la source officielle. On se prépare donc à transmettre les paiements.
- Un rappel du **04/05/2027** (tâche programmée `trig_01NtmbRzdCZSdDdsMK21ikx1`) cherchera la réponse écrite officielle.

## 3. Plateformes : statut officiel (FAIT ET VÉRIFIÉ le 04/11/2026)

Page impots.gouv.fr « Je consulte la liste des plateformes agréées » : « modifié le 03/11/2026 ». Deux fichiers y sont
publiés (le premier porte un nom de fichier ancien contenant « attente », mais la page le présente bien comme la liste
des opérateurs ayant réussi tous les tests) :
- `liste_pa_attente_rapport_audit.xlsx` : opérateurs « satisfaisant à l'ensemble des conditions, incluant les tests
  d'interopérabilité », 158 lignes de données ;
- `liste_pa_attente_test_interop.xlsx` : opérateurs « en attente de leur immatriculation définitive », 8 lignes.

| Plateforme | Liste définitive | Date d'immatriculation (fichier officiel) |
|---|---|---|
| **INDY** (Lyon) | Oui | 09/01/2026 |
| TIIME PDP (Paris) | Oui | 18/12/2025 |
| ABBY (Nancy) | Oui | 29/01/2026 |
| Dougs Facturation gratuite (Fay-aux-Loges) | Oui | 12/12/2025 |

Aucune des quatre ne figure dans la liste « en attente de tests ».

## 4. Comparaison fonctionnelle et tarifaire

Pages lues le 04/11/2026 par téléchargement direct. Un « ? » signifie : non trouvé sur la page publique. Il faut le
vérifier dans le compte avant toute décision (leçon du 30/10 sur Postnify : « offre gratuite annoncée, pas tenue dans le
compte »).

| Critère | Indy Essentiel (choisi) | Tiime Free | Abby Basique | Dougs gratuit |
|---|---|---|---|---|
| Prix | 0 € HT/mois (indy.fr/tarifs) | 0 € (« Plateforme Agréée pour tous, sans engagement, Gratuit ») | 0 € (« Gratuit ») | ? (page vide en lecture directe : contenu chargé en JavaScript) |
| Réception | **Oui, active pour DIG16 depuis le 16/10** | Oui (« Réception de Factures électroniques fournisseurs ») | Oui (« Facturation électronique Plateforme Agréée ») | ? |
| Émission PA à PA | **Pas encore** (« n'est pas encore disponible », Indy, 22/09/2026) ; factures PDF par courriel toujours conformes jusqu'au 01/09/2027 | Annoncée (« Émission de Factures électroniques conformes ») ; ouverture réelle ? | ? | ? |
| E-reporting transactions | Annoncé « bien avant l'échéance » (Indy, 31/08/2026) | Cité (« statuts, e-reporting ») ; offre gratuite ? | ? | ? |
| E-reporting paiements | Idem | ? | ? | ? |
| Acomptes, paiements partiels, avoirs | Avoirs : oui (page tarifs : « création d'avoirs ») ; acomptes ? | « Acomptes, avoirs » cités | ? | ? |
| Livre des recettes | Offre Autonomie, payante (lu le 10/10) → **remplacé par l'outil du § 5** | « Livre de recettes - Registres » | « Livre des recettes » (gratuit) | ? |
| Compte bancaire pro | Oui (IBAN et carte) | Oui | Non | ? |
| Export comptable et archivage | « Conformité et archivage » | « Valeur probante sur l'archivage » | ? | ? |

**Décision recommandée** (RECOMMANDATION) : **garder Indy**. C'est déjà le logiciel et la plateforme, c'est gratuit, et
tout migrer n'apporterait rien aujourd'hui. Il y a une seule réserve : l'émission et l'e-reporting ne sont pas encore
ouverts chez Indy.

En mai 2027, deux cas se présenteront :
- **si Indy gratuit les ouvre** : rien ne change ;
- **sinon** : choisir une solution d'émission seule (Tiime Free est le premier candidat à revérifier), **sans** l'étape
  « inscription plateforme agréée », pour ne pas écraser la réception chez Indy.

## 5. Outil livré : livre des recettes et préparation du e-reporting (FAIT ET VÉRIFIÉ en local)

`outils/compta/livre_recettes.py` (bibliothèque standard Python, aucune dépendance) :
- il tient le **livre des recettes obligatoire**, dans l'ordre des dates, avec le montant, le client, le mode de
  règlement, la référence de la pièce et un total par trimestre. Ce sont les exigences de la fiche
  entreprendre.service-public.gouv.fr/vosdroits/F23266, « Vérifié le 07 septembre 2026 », lue le 04/11/2026. Il
  remplace l'offre payante d'Indy ;
- il contrôle la saisie (date, montant, mode, client, numéro de pièce) et les acomptes ou paiements partiels ;
- il vérifie les **seuils de la franchise** (37 500 € et 41 250 €, lus dans `connaissances/fiscal-valeurs.json`) ;
- il prépare, **par bimestre et avec l'échéance**, les totaux des **données de paiement** (services) et des **données de
  transaction** (particuliers et étranger), séparément, à partir du 01/09/2027. Il ne transmet rien : il sert à
  contrôler ce que la plateforme enverra ;
- il **refuse** d'écrire ou de lire dans un dossier suivi par git (le dépôt public ou tout autre dépôt), car les données
  des clients sont privées ; si la vérification échoue, il refuse aussi.

Tests :
- `python3 -m unittest discover -s outils/compta -p "test_*.py"` : **tous les tests réussis** (nombre dans le CHANGELOG), données fictives ;
- ajoutés aux tests automatiques de GitHub (job `outils_dig16` de `.github/workflows/tests.yml`), vert sur GitHub le
  04/11/2026.

Utilisation : au premier encaissement, créer le fichier CSV privé dans le **Drive « Dig »** (copie de référence, durable) et
le copier dans le scratchpad `prive/compta/` pour lancer l'outil. Puis lancer :
`python3 outils/compta/livre_recettes.py <csv> --sortie <dossier privé> --annee 2026`.

**Intégration avec Indy (BLOQUÉ)** : Indy ne publie pas d'API ouverte, aucune n'a été trouvée sur ses pages publiques le
04/11/2026. Un import automatique n'est donc pas possible sans se connecter au compte de l'utilisateur, ce qui est
interdit par les consignes. Pour éviter la double saisie : un **export CSV d'Indy**, s'il existe dans le compte, pourra
être converti pour l'outil. À vérifier sur une capture au premier encaissement (À FAIRE, avec l'utilisateur).

## 6. Ce qui reste à l'utilisateur

- Rien avant mai 2027 pour la facturation électronique : la réception est faite.
- Au premier client : envoyer une capture de l'export des factures d'Indy (une minute), pour brancher l'outil sans
  double saisie.
- **Aucun mandat, aucune inscription, aucun compte** n'a été créé pendant cet audit.

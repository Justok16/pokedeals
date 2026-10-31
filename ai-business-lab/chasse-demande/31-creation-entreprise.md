# Création de l'entreprise DIG16 — micro-entreprise, fiscalité, aides

Repris du kit du 24/09 (08/10 : la partie Atlassian est abandonnée et supprimée à la demande de
l'utilisateur ; seules les sections sur la création de l'entreprise sont gardées). Tout ce qui
n'est pas vérifié à la source est marqué **[à vérifier]**.

## 2. Micro-entreprise (France)

- Création en ligne, gratuite, sur le guichet unique :
  https://formalites.entreprises.gouv.fr
- Activité à déclarer : édition de logiciels / applications en ligne.
  Nature (commerciale BIC ou libérale BNC) et code APE (vraisemblablement
  58.29C « Édition de logiciels applicatifs ») **[à vérifier au moment de
  la déclaration]** : cela change le taux de cotisations et le plafond.
- Cotisations : pourcentage du chiffre d'affaires encaissé, déclaré chaque
  mois ou trimestre sur autoentrepreneur.urssaf.fr ; taux **[à vérifier]**.
- TVA : franchise en base sous un seuil de chiffre d'affaires **[à
  vérifier, seuils modifiés en 2025]** ; ventes à des entreprises hors de
  France : règles d'autoliquidation **[à vérifier avec un conseiller
  gratuit : CCI, URSSAF ou chambre des métiers]**.
- Compte bancaire dédié : obligatoire si le chiffre d'affaires dépasse
  **10 000 € pendant 2 années consécutives** ; il peut s'agir d'un simple
  compte personnel distinct, qui doit porter la mention « EI » (source :
  Service Public Entreprendre, fiche F35991, « Vérifié le 28 mai 2026 »,
  lue le 05/10/2026). Recommandé dès le départ ; en refus, droit au compte
  par la Banque de France. Comparatif des comptes pros gratuits : voir
  moneyradar.org (site d'affiliation : tarifs à revérifier chez la banque).

### Rappel à faire à l'utilisateur juste après la création (demande du 26/09)

- Compléter le **flyer Canva** (design « DAHWQBvgVuI ») : téléphone, email,
  prénom et nom, SIREN, adresse ; remplacer le lien du QR code par la
  démo définitive (`42-flyer-et-prompt.md`).
- Même chose pour les textes et l'email de `41-prospection-questionnaire-et-textes.md`.
- **Nom commercial et domaine (décision de l'utilisateur, 05/10/2026)** :
  marque publique **DIG16** (« Création de sites internet en Charente »),
  domaine **`dig16.fr`**, email `contact@dig16.fr`, registrar envisagé :
  OVHcloud. Remplace `digsite.fr` (accord du 26/09). `dig16.fr` et
  `dig-16.fr` non enregistrés le 05/10 d'après l'AFNIC (RDAP 404) :
  revérifier juste avant l'achat. Aucune entreprise nommée DIG16 au
  registre (recherche-entreprises.api.gouv.fr, 05/10) ; recherche de
  marque INPI « DIG16 » : **aucun résultat** le 05/10 (faite par l'utilisateur sur
  data.inpi.fr). Décision du 05/10 : réserver `dig16.fr` **tout de suite**,
  au nom du particulier (l'AFNIC masque par défaut les données des personnes
  physiques dans le Whois du .fr), puis le transférer à l'entreprise si besoin.
  **Fait le 05/10** : `dig16.fr` réservé chez OVHcloud (5,99 € TTC la 1re année,
  renouvellement annoncé à 7,79 €/an), DNSSEC et compte e-mail Zimbra Starter
  inclus ; boîte `contact@` créée (MX Plan, 5 Go). DNS public vérifié le 05/10 :
  serveurs OVH, MX OVH, SPF `v=spf1 include:mx.ovh.com -all` ; DMARC
  `p=quarantine` et DNSSEC (enregistrement DS) **publiés et vérifiés le 05/10** ;
  webmail testé en réception ; double authentification du compte OVH activée (05/10). Sécurité
  du domaine : 2FA, renouvellement automatique, DNSSEC, verrouillage ;
  email : SPF, DKIM, DMARC. Ensuite : site vitrine sur Cloudflare Pages,
  QR du flyer vers `dig16.fr`, renommer « Dig » en « DIG16 » dans
  `site-dig/` et les supports.

### Formulaire du guichet : réponses préparées (08/10/2026)

Décision de l'utilisateur (08/10) : l'entreprise est domiciliée **chez lui** (pas de domiciliation
payante). **Correction du 08/10 (écran du guichet INPI lu par l'utilisateur)** : quand l'adresse de
l'entreprise est le domicile, elle est **publiée au RNE** (art. L123-50 et L123-52 du code de commerce,
D411-1-3 du CPI) et réutilisable par tous ; la non-diffusion ne protège que l'adresse personnelle
**distincte** de celle de l'entreprise. Seule parade : domiciliation (payante) ou local. Version
complète avec ses coordonnées : document privé « DIG16 – Création de la micro-entreprise pas à pas »
du Drive « Dig ». Sources lues le 08/10 : Service-Public F36746 et F23282 (« Vérifié le 18 mars
2026 »), INSEE NAF 62.01Z (mise à jour du 19/12/2025).

- Guichet gratuit pour une activité libérale ; dépôt au plus tôt 1 mois avant et au plus tard
  15 jours après le début d'activité (F36746, F23282).
- Pièces : pièce d'identité, justificatif de domicile (facture d'eau, d'électricité ou de gaz),
  déclaration de non-condamnation et attestation de filiation signée (F36746).
- Nature : libérale non réglementée (BNC). Description : « Conception, réalisation, mise en ligne et
  maintenance de sites internet pour les professionnels ». Code APE attribué par l'INSEE, attendu
  62.01Z (la sous-classe cite la création de « pages web ») ; remplace l'hypothèse 58.29C ci-dessus.
- Nom commercial DIG16, site dig16.fr, email contact@dig16.fr.
- **Activité à ajouter (décision du 19/10, `70` § 7 bis)** : « assistance administrative aux professionnels : préparation de devis, établissement de factures sous mandat de facturation, suivi des règlements ». Si le dossier du 08/10 est encore à régulariser, l'ajouter à la description ; sinon, formalité de modification au guichet unique INPI (à déclarer sous un mois, payante selon tarif réglementé ; page INPI lue le 19/10). Nature : **BNC**, par adjonction d'activité (réponse de l'URSSAF au téléphone, 20/10/2026). Jamais le mot « comptabilité » dans la description (activité réservée aux experts-comptables).
- Versement libératoire : **non** (l'exonération FRR+ porte sur l'impôt sur le bénéfice ; à faire
  confirmer par le SIE). Déclarations URSSAF trimestrielles (mensuelles possibles). Franchise en base de TVA. ACRE demandée.
- **Dossier déposé au guichet le 08/10/2026** (décision de l'utilisateur de ne pas attendre la CPAM ni
  l'Agefiph ; l'aide Agefiph, à demander avant l'immatriculation, est donc probablement perdue).
- **Classement par le greffe (08/10/2026)** : la réclamation du greffe du tribunal de commerce d'Angoulême
  porte sur une « immatriculation principale dématérialisée **RCS** » : l'activité a été classée
  **commerciale** (prestations de services BIC), sans doute par le choix « hébergement » au guichet, et non
  libérale. Cotisations micro (Service-Public F36232, « Vérifié le 01 janvier 2026 », lu le 08/10) :
  **21,2 %** du chiffre d'affaires pour les prestations de services commerciales ou artisanales (22,9 % avec
  versement libératoire), contre 25,6 % en libéral non réglementé : **classement conservé**, plus favorable.
  Factures : Service-Public F31808 (lu le 08/10/2026) demande pour un entrepreneur individuel « nom et prénom
  de l'entrepreneur individuel précédé ou suivi de la mention « Entrepreneur individuel ou EI » - adresse -
  numéro Siren » ; aucune mention RCS n'y est citée. Les modèles (EI, adresse, SIREN) sont donc conformes :
  **pas d'ajout « RCS Angoulême »**. Corrections demandées : nom de domaine du document de
  synthèse (à supprimer) et déclaration de non-condamnation non signée ; délai 15 jours.
- **ACRE (formulaire Urssaf « Demande-ACRE_2026 », lu le 08/10/2026)** : à transmettre « dès la création
  d'activité » sur autoentrepreneur.urssaf.fr, au plus tard 60 jours après le début d'activité. Cas retenu :
  « Exercice de l'activité au sein d'une zone France ruralités revitalisation (ZFRR) ou … (ZFRR+) », pièce :
  justificatif de l'adresse de l'établissement dans la zone ; joindre aussi le justificatif de création du
  guichet. Attestation sur l'honneur : pas d'ACRE dans les 3 dernières années. Attention : l'ACRE « sera
  considérée comme utilisée sur la période d'exonération, même en l'absence de chiffre d'affaires ».
  Réponse : silence d'un mois vaut accord (à revérifier sur la fiche Urssaf) ; attestation dans « Mes attestations ».
- **Accord de l'utilisateur (08/10, « Oui »)** : à la validation de la formalité, ses coordonnées (nom,
  adresse, téléphone, SIREN) sont publiées sur les mentions légales de dig16.fr, donc aussi dans ce dépôt
  (obligation LCEN ; adresse déjà publique au RNE) : `DIG16_IDENTITE=<json privé> python3
  outils/ouverture_site.py --ecrire`, puis `outils/test_pages.py`. Flyer et documents commerciaux remplis :
  versions privées seulement (`outils/marque/identite.py`).

## 2 bis. Création parfaite et fiscalité optimisée (exigence de l'utilisateur, 25/09)

Claude prépare **tout** (choix, formulaires pré-remplis, calendrier des
déclarations, calculs) ; l'utilisateur valide et signe (identité). Chaque
point est vérifié à la source officielle **au moment d'agir**, puis
confirmé gratuitement auprès de l'URSSAF, de la CCI ou des impôts ; les
effets sur les aides sont simulés avec la CPAM (36 46) et la CAF **avant**
la création.

Faits vérifiés le 05/10/2026 (sources officielles lues ce jour) :
- **TVA** : franchise en base pour les services en 2026 : 37 500 € ;
  seuil majoré 41 250 € (TVA due dès le jour du dépassement) ; mention
  « TVA non applicable - article 293 B du CGI » (Service-Public F21746,
  « Vérifié le 01 janvier 2026 »).
- **Cotisations micro, libéral non réglementé (BNC)** : 25,6 % du CA ;
  27,8 % avec versement libératoire (Service-Public F36232, « Vérifié le
  01 janvier 2026 »).
- **Taux avec ACRE (page officielle « L'essentiel du statut », autoentrepreneur.urssaf.fr, lue le 20/10/2026)** : BNC 12,8 % pour un début jusqu'au 30/06/2026, **19,2 %** à compter du 01/07/2026 (cas de DIG16, début le 08/10/2026 : jusqu'au 30/09/2027), puis 25,6 % ; BIC services 10,6 % / 15,9 % / 21,2 %. L'URSSAF a annoncé au téléphone le 20/10 « BNC, 12,8 % » : chiffre à faire confirmer (ancien taux). Nature retenue par l'URSSAF : BNC, alors que le greffe a classé en RCS (voir plus haut) : à vérifier dans l'espace URSSAF.
- **ACRE 2026** : demande à l'URSSAF **dans les 60 jours** suivant le début
  d'activité ; l'implantation dans une commune en zone FRR ou FRR+ est un
  des critères ; pour une micro-entreprise créée à partir du 01/07/2026 :
  taux égal à 75 % du taux normal jusqu'à la fin du 3e trimestre civil
  suivant le début d'activité (Service-Public F11677, « Vérifié le
  01 juillet 2026 » ; exemple officiel : début le 03/09/2026 → 30/06/2027).
- **Zone FRR+** (arrêté du 9 juillet 2025, Légifrance JORFTEXT000051871914) :
  exonération d'impôt sur les bénéfices totale jusqu'au 59e mois, puis
  abattements de 75 %, 50 % et 25 % sur trois périodes de 12 mois
  (art. 44 quindecies A du CGI) ; ouverte aux micro-entreprises, le
  bénéfice exonéré se reporte sur la 2042-C-PRO (BOFiP
  BOI-BIC-CHAMP-80-10-75-40, 29/07/2026, § 80). Implantation **réelle**
  exigée. Articulation avec le versement libératoire : **non précisée par
  le BOFiP → à faire confirmer par écrit par le SIE** avant toute option.
- **Adresse publiée (vérifié le 05/10/2026)** : un entrepreneur individuel peut domicilier son
  entreprise chez lui et demander la non-diffusion publique de son adresse personnelle dans les
  registres (Service-Public F2160, « Vérifié le 02 juillet 2026 ») **[corrigé le 08/10 : la
  non-diffusion ne vaut pas quand l'entreprise est domiciliée au domicile ; voir § 2]**. Mais le **site** d'un éditeur
  professionnel doit afficher « nom, prénoms, domicile et numéro de téléphone » (LCEN art. 1-1, I, 1°,
  version en vigueur depuis le 23/05/2024, lue sur Légifrance) ; l'anonymat (II) est réservé aux
  éditeurs « à titre non professionnel ». Le texte ne dit pas qu'une adresse de domiciliation
  commerciale remplace le domicile. **Décision de l'utilisateur** : publier son adresse sur la page
  « Mentions légales » de dig16.fr, ou payer une domiciliation (budget 0 € → à éviter), ou chercher une
  domiciliation gratuite (pépinière, CCI) **[à vérifier]**. Flyer et emails : l'adresse postale n'est
  pas exigée par L34-5 ni par l'art. 20 de la LCEN (identité + moyen de refuser) **[à confirmer]**.
- Commune visée, situation et modèles de lettres (SIE, URSSAF, mairie,
  communauté de communes) : document privé « DIG16 – Synthèse création »
  du Drive « Dig », jamais dans ce dépôt.

Points à trancher, dans l'ordre :
1. Statut le plus avantageux compte tenu des aides perçues (micro-entreprise
   ou autre) : comparer le **gain net** après baisse éventuelle des aides.
2. Nature d'activité (BIC ou BNC) et code APE : ils fixent le taux de
   cotisations et l'abattement fiscal **[à vérifier]**.
3. ACRE (cotisations réduites la première année) : éligibilité **[à vérifier]**.
4. Versement libératoire de l'impôt : utile ou non selon le revenu fiscal
   du foyer **[à vérifier]** — souvent défavorable aux revenus modestes.
5. TVA : franchise en base ; ventes de services à des entreprises de l'UE
   ou hors UE (autoliquidation, numéro de TVA intracommunautaire) **[à vérifier]**.
6. CFE (cotisation foncière des entreprises) : exonération la première
   année, puis montant selon la commune **[à vérifier]**.
7. Domiciliation (ne pas publier l'adresse personnelle) et option de
   non-diffusion au répertoire SIRENE.
8. Compte bancaire dédié, livre des recettes, factures conformes.
9. Calendrier : déclaration URSSAF (mensuelle ou trimestrielle), déclaration
   de ressources éventuelles (CPAM, CAF : voir le document privé du Drive),
   déclaration de revenus annuelle (formulaire 2042-C-PRO).

Claude tient ce calendrier dans une routine de rappels et prépare chaque
déclaration à l'avance.

## 2 ter. Plan d'optimisation fiscale et sociale (31/10/2026, demande de l'utilisateur : « le moins de choses à payer »)

Tout ce qui suit est **légal** et vient de pages officielles lues le 31/10/2026 (valeurs et sources :
`connaissances/fiscal-valeurs.json`, calculs : `python3 outils/fiscal/simulateur.py <CA>`). Aucun
montage, aucune minoration de recettes : toute recette encaissée est déclarée. Les décisions qui
engagent l'utilisateur sont marquées **À TOI**. Correction du 31/10 : la phrase du § 2 bis
« articulation avec le versement libératoire non précisée » est tranchée ci-dessous (levier 3).

| # | Levier | Gain | État | Source lue le 31/10/2026 |
|---|---|---|---|---|
| 1 | **Rester en BIC « prestations de services »** (classement actuel : immatriculation RCS, compte Indy « BIC services ») et non en BNC | cotisations 15,9 % au lieu de 19,2 % avec ACRE, 21,2 % au lieu de 25,6 % ensuite ; formation 0,1 % au lieu de 0,2 % ; abattement 50 % au lieu de 34 %. Pour 30 000 € de CA : **≈ 1 000 € par an** avec ACRE, **≈ 1 340 €** ensuite | Classement à faire **confirmer par écrit** par le SIE (message préparé le 03/11). Arguments : offre vendue en **abonnement** comprenant hébergement géré, maintenance, mises à jour et référencement (prestations de services commerciales répétées), et non une œuvre intellectuelle isolée. Le classement suit les faits : on ne le « choisit » pas, on le fait reconnaître | F36232, F23459, page impots.gouv « régime unique des micro-entreprises » |
| 2 | **Ne pas ajouter d'activité BNC** (« assistance administrative ») tant que le SIE n'a pas répondu | évite une activité mixte et une part de CA au taux BNC (25,6 %) | brouillon INPI laissé en l'état (décision du 27/10 maintenue) | F36232 |
| 3 | **Exonération d'impôt sur le revenu ZFRR+** (art. 44 quindecies A) : bénéfice exonéré à 100 % pendant 59 mois, puis 75 %, 50 %, 25 % | impôt sur le revenu du bénéfice DIG16 **à 0 €** jusqu'à septembre 2031 environ (59 mois après octobre 2026) | **Micro admis en ZFRR+** (« quel que soit son régime fiscal », F31139) — attention, en ZFRR simple le micro est **exclu sauf option pour un régime réel** (BOFiP 75-10 § 100) : vérifier que la commune est bien sur la liste **ZFRR+** (arrêté du 9 juillet 2025, fait le 05/10). Bénéfice exonéré reporté chaque année sur la **2042-C-PRO** (BOFiP 75-40 § 80). Sécuriser par une **prise de position écrite** du correspondant ZFRR de la DDFIP de la Charente (art. L. 80 B du LPF, BOFiP 75-40 § 90) : demande préparée avec le message au SIE | F31139 ; BOFiP BOI-BIC-CHAMP-80-10-75-10 et -40 (29/07/2026) |
| 4 | **Ne jamais opter pour le versement libératoire** | le versement libératoire ferait payer 1,7 % du CA (BIC) alors que le bénéfice est exonéré par le levier 3 | à garder ; le rappeler si l'URSSAF le propose | F36232 (22,9 % au lieu de 21,2 % en BIC) |
| 5 | **CFE : 0 € en 2026, 2027 et 2028** | CFE minimum évitée (base 2026 entre 250 € et 597 € selon la commune pour un CA ≤ 10 000 €, F23999) | 2026 : année de création exonérée. 2027 et 2028 : exonération si le CA HT de **2026**, ramené à 12 mois, ne dépasse pas 5 000 €, soit **≤ 1 164 € HT encaissés en 2026** (85 jours d'activité). **Décision de l'utilisateur (31/10) : « oui, mais seulement si on approche de la limite »** : Claude suit le total (skill `nouveau-client`, étape 7, et veille du 3 du mois) et ne propose un **démarrage et une facture en janvier 2027** que si le total de 2026 approche 1 164 € ; un client pressé reste prioritaire ; sinon dépasser n'est pas grave si l'exonération ZFRR+ de CFE (levier 6) est votée | F23999, impots.gouv « dois-je payer une CFE » (14/10/2026), art. 1647 D CGI |
| 6 | **CFE ZFRR+ (art. 1466 G)** : 5 ans d'exonération puis abattements | CFE à 0 € jusqu'en 2031 environ | **Seulement si la commune ou la communauté de communes a voté la délibération** (non trouvée en ligne le 31/10) : question ajoutée au message au SIE ; sur la **1447-C-SD** (version « CFE 2027 », imprimé 5568) cocher la ligne 1466 G **uniquement** si la délibération existe (option définitive, une seule ligne). Dépôt **avant le 31/12/2026** (rappel du 10/12) | BOFiP BOI-IF-CFE-10-30-40-60 (29/07/2026), F31139, imprimé 1447-C-SD 2027 |
| 7 | **Taxe CCI** (0,044 % du CA en services) | 0 € en 2026 (année de création), 0 € chaque année où la CFE n'est pas due (elle lui est additionnelle) et tant que le CA ≤ 5 000 € ; sinon quelques euros | automatique | F36244, F32847 |
| 8 | **ACRE** : cotisations à 75 % du taux normal jusqu'au 30/09/2027 | ≈ 25 % de cotisations en moins pendant 4 trimestres | **acquise** (attestation URSSAF du 23/10) ; rappel de fin le 01/09/2027 | attestation privée, F11677 |
| 9 | **Franchise de TVA** (TVA non facturée, « TVA non applicable, art. 293 B du CGI ») | prix 20 % plus bas que des concurrents assujettis | rester sous **37 500 € HT** par an (au-delà : TVA l'année suivante ; au-delà de 41 250 € : dès le jour du dépassement) ; garde-fou à 33 000 € dans le livre des recettes | F21746 |
| 10 | **Rester au régime micro** (pas de régime réel) | pas de comptable payant ; le régime réel n'apporterait rien puisque le bénéfice est exonéré (levier 3) et que les charges sont presque nulles | à garder ; à réexaminer seulement si les charges dépassent 50 % du CA | impots.gouv « puis-je déduire des charges » |
| 11 | **Déclarations sans pénalité** : URSSAF même à 0 € (trimestrielle), 2042-C-PRO en mai, CFP prélevée en novembre | évite les majorations | rappels programmés (05/01/2027 pour le 4e trimestre 2026) | F23257 (à revérifier), F23459 |
| 12 | **Frais bancaires et outils à 0 €** (Indy Essentiel, plateforme agréée gratuite) | 0 € d'abonnement | en place | page tarifs Indy (10/10) |

**Ce qui n'est pas possible (vérifié)** : déduire des frais réels en micro ; réduire les cotisations
autrement que par l'ACRE et le bon classement ; « choisir » BIC pour une activité qui serait
réellement libérale (le SIE tranche sur les faits) ; cumuler l'exonération ZFRR+ de CFE avec une
autre exonération de zone (option unique et définitive).

**À surveiller** : budget 2027 (rien de prévu pour les micro-entrepreneurs d'après la presse
spécialisée lue le 31/10, à confirmer au vote de décembre), taux BNC (relevé chaque année depuis 2025),
seuil de TVA (projet de seuil unique supprimé en 2025, peut revenir). Veille mensuelle programmée.

**Point d'attention (privé)** : le bénéfice exonéré reste compté dans le revenu fiscal de référence
(brochure IR, cases des bénéfices exonérés) ; effets éventuels traités dans le document privé du Drive.

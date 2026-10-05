# Kit « un éditeur a dit oui » — préparé le 24/09

But : le jour où un éditeur accepte, l'utilisateur n'a qu'à valider et
signer. Tout ce qui n'est pas vérifié à la source est marqué **[à vérifier]**
et le sera au moment d'agir (les règles et montants changent).

## 1. Ordre des opérations

| # | Étape | Qui | Durée estimée |
|---|---|---|---|
| 1 | Répondre à l'éditeur : remerciement, demande du rapport de ventes des 12 derniers mois (disponible dans son espace partenaire) et du code source | Claude rédige, l'utilisateur valide | jour 0 |
| 2 | Vérifier les chiffres réels (installations payantes, revenu) avant tout engagement | Claude | 1-2 jours |
| 3 | Appeler le 36 46 (CPAM) pour une simulation personnalisée, puis créer la micro-entreprise, nom commercial « Dig » (validé le 25/09) | l'utilisateur (en ligne, gratuit) | 1 à 3 semaines pour le numéro SIRET [à vérifier] |
| 4 | Acheter un nom de domaine + adresse email professionnelle (exigée par le portail partenaire Atlassian) | l'utilisateur paie ~10 €/an ; Claude guide | 1 heure |
| 5 | Créer le compte partenaire Atlassian (« Marketplace Partner ») et passer la vérification (« Partner Verification ») | l'utilisateur (identité) ; Claude prépare les réponses | quelques jours [à vérifier] |
| 6 | Signer l'accord de partage de revenu (modèle §3) | l'utilisateur + l'éditeur | jour ~7 |
| 7 | L'éditeur ouvre le ticket de transfert d'app auprès d'Atlassian et l'approuve | l'éditeur | variable |
| 8 | Portage Forge, tests, publication de la nouvelle version | Claude | 2 à 6 semaines selon l'app |
| 9 | Support client (documentation, réponses types) | Claude prépare, l'utilisateur envoie ou délègue | continu |

Date butoir absolue : **31/01/2027** (fin de support de Connect).

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
  registres (Service-Public F2160, « Vérifié le 02 juillet 2026 »). Mais le **site** d'un éditeur
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

## 3. Modèle d'accord de partage de revenu (anglais, à faire relire)

> **App Transfer and Revenue Share Agreement**
>
> Between **[Vendor legal name]** (“Original Vendor”) and **[micro-entreprise
> name, SIRET]** (“New Vendor”).
>
> 1. **Scope.** The Original Vendor transfers to the New Vendor the
>    Atlassian Marketplace listing(s) **[app names and keys]**, together
>    with the source code, documentation, trademarks used in the listing,
>    and any assets needed to operate the app(s).
> 2. **Transfer process.** The Original Vendor initiates and approves the
>    transfer through Atlassian's standard app transfer process within
>    **[10]** business days of signature.
> 3. **Intellectual property.** Upon completion of the transfer, the
>    Original Vendor assigns to the New Vendor all rights in the app(s)'
>    code and listing content, and warrants that it has the right to do so
>    (including for third-party and open-source components, which remain
>    under their own licences).
> 4. **Revenue share.** For **24 months** from the completion of the
>    transfer, the New Vendor pays the Original Vendor **30%** of the net
>    revenue received from Atlassian for the app(s) (after Atlassian's
>    revenue share, refunds and taxes), quarterly, within 30 days of the
>    end of each quarter, with the corresponding Atlassian sales report.
> 5. **Customers and data.** The New Vendor becomes responsible for support,
>    maintenance and the processing of customer data from the completion of
>    the transfer. The Original Vendor deletes or transfers any customer data
>    it holds, as agreed in writing, and cooperates in good faith on
>    open support requests for **[30]** days.
> 6. **No other payment.** No upfront payment is due. **[Option : an
>    additional fixed amount of [X] paid out of future revenue.]**
> 7. **Liability.** Each party is liable for its own acts. The Original
>    Vendor remains responsible for events before the transfer; the New
>    Vendor for events after it.
> 8. **Term.** The agreement ends when the last revenue-share payment is
>    made. Clauses 3, 5 and 7 survive.
> 9. **Governing law.** **[To agree — e.g. the law of the Original Vendor's
>    country or French law.]**
>
> Signed on **[date]**, by **[names, titles]**.

**Relecture recommandée** avant signature (contrat entre deux pays, cession
de propriété intellectuelle, données personnelles des clients).

## 4. Réponses types aux questions probables des éditeurs

- *Qui êtes-vous ?* Un éditeur indépendant (micro-entreprise française)
  spécialisé dans le portage d'apps Connect vers Forge ; pas d'autres apps
  publiées à ce jour — le dire honnêtement.
- *Quelles garanties ?* Le transfert ne se fait qu'après signature ; le
  code n'est demandé qu'une fois l'accord signé ; l'éditeur garde le droit
  de refuser le transfert dans le ticket Atlassian jusqu'au bout.
- *Quel calendrier ?* Portage visé dans les 6 semaines suivant le
  transfert, en tout cas avant le 31/01/2027.
- *Et nos clients ?* Même fiche, même clé d'app si Atlassian le permet
  **[à vérifier : conservation de la clé et des licences lors d'un
  transfert]**, donc pas de réinstallation pour eux.

# 68 — Prévenir les trois risques d'un site client (18/10/2026)

Demande de l'utilisateur (18/10, 23 h 45), après la question de la RC Pro : « fais en sorte que ça n'arrive jamais »
pour trois risques : site en panne plusieurs jours, problème de droits d'auteur sur une photo ou un texte, fuite de
données personnelles par un formulaire. Principe : **empêcher** (technique et méthode), **limiter** (contrat),
**réagir vite** (procédure écrite). Chaque fait ci-dessous vient d'une source officielle lue le 18/10/2026.

## Sources lues le 18/10/2026

| Sujet | Source | Ce qu'elle dit |
|---|---|---|
| Assurance | service-public, fiches F23667 et F23668 | RC Pro obligatoire seulement pour les activités et professions réglementées |
| Limitation de responsabilité | Code civil, art. 1170 (Légifrance) | « Toute clause qui prive de sa substance l'obligation essentielle du débiteur est réputée non écrite. » |
| Dommages | Code civil, art. 1231-3 (Légifrance) | le débiteur n'est tenu que des dommages prévus ou prévisibles « sauf lorsque l'inexécution est due à une faute lourde ou dolosive » |
| Photos d'illustration | unsplash.com/license | usage gratuit, commercial compris, sans autorisation ni mention obligatoire ; interdit : revendre les images sans modification importante |
| Sous-traitance RGPD | CNIL, « Sous-traitance : exemple de clauses » et guide du sous-traitant | le sous-traitant prévient le responsable ; notification à la CNIL « si possible, 72 heures au plus tard » |
| Formulaire sans stockage | Cloudflare Email Service, page Pricing (mise à jour du 09/06/2026) | l'envoi vers des adresses de destination **vérifiées** du compte est gratuit sur tous les plans, Workers Free compris |

## 1. Site en panne plusieurs jours

**Empêcher**
- Sites **statiques** (pages HTML, pas de base de données ni d'extensions à mettre à jour) hébergés sur Cloudflare
  Pages, dans un compte gratuit au nom du client (décision du 05/10) : la principale cause de panne des sites
  d'artisans (extension ou CMS non mis à jour, piratage) n'existe pas.
- **Copie complète** de chaque site dans un dépôt Git (historique de chaque version) + archive ZIP remise au client à
  chaque mise en ligne : un site peut être republié en quelques minutes, chez Cloudflare ou ailleurs.
- **Surveillance automatique toutes les 3 heures** : étendre `outils/sentinelle_dig16.py` (déjà en place pour
  dig16.fr) à chaque site client dès le premier client (page, certificat, nom de domaine) ; une alerte crée une
  issue GitHub et un email.
- **Nom de domaine** au nom du client, renouvellement automatique activé et vérifié à la livraison ; date
  d'expiration notée et rappelée par le garde-fou mensuel (`64` § 0 bis).
- Aucune modification de DNS ou de configuration sans test préalable (`outils/test_pages.py`, contrôle en ligne).
- Le client reste joignable même pendant une panne : téléphone sur sa fiche Google et ses annuaires.

**Réagir** — procédure : alerte → diagnostic (site, DNS, certificat, domaine) → republier depuis Git ou basculer
vers un second hébergeur gratuit → prévenir le client par téléphone et par écrit → noter la cause dans
`connaissances/lecons.md`. Objectif : site rétabli dans la journée ouvrée. **[Bascule vers un second hébergeur : à
tester sur le premier site client avant de la promettre.]**

**Limiter (CGV, à valider par l'utilisateur)** — voir § 4, articles 10 et 12.

## 2. Photo ou texte qui pose un problème de droits d'auteur

**Empêcher**
- **Photos du client d'abord** (déjà la règle des démos) ; dans le questionnaire de lancement, le client confirme par
  écrit qu'il en est l'auteur ou qu'il a l'autorisation de l'auteur.
- **Photos d'illustration : uniquement Unsplash** (licence lue le 18/10), jamais Google Images, jamais un site
  concurrent ; pas de visage reconnaissable sans accord écrit de la personne (droit à l'image).
- **Registre des médias** par client (privé, Drive « Dig ») : pour chaque image, l'origine (photo du client avec
  date de l'attestation, ou lien de la page Unsplash et date de téléchargement).
- **Textes rédigés par DIG16** à partir de l'entretien avec le client, jamais copiés ; vérification par recherche de
  phrases exactes avant la mise en ligne ; le client relit et valide (CGV art. 8).
- Logos de labels et de marques (Qualibat, fabricants…) seulement si le client en a vraiment le droit (certificat).

**Réagir** — toute réclamation : retrait du contenu visé **sous 24 heures**, sans discuter, puis examen avec le
client ; réponse écrite à la personne qui réclame.

**Limiter (CGV)** — garantie du client sur les contenus qu'il fournit (§ 4, art. 8).

## 3. Fuite de données personnelles par un formulaire

**Empêcher**
- **Le moins de données possible** : par défaut, bouton « Appeler » et adresse email ; si un formulaire est utile,
  seulement nom, téléphone ou email, message ; **jamais** de données de santé ou bancaires (secteurs exclus, `40` § C).
- **Aucun stockage** : le formulaire envoie le message par email au client, via une petite fonction Cloudflare dans
  son propre compte (envoi gratuit vers son adresse vérifiée, page Pricing du 09/06/2026) ; pas de base de données,
  pas de service tiers en plus (le formulaire de dig16.fr passe aujourd'hui par FormSubmit : à remplacer de la même
  façon). **[Modèle de fonction à construire et tester au premier client qui demande un formulaire.]**
- Sécurité des comptes : double authentification sur Cloudflare, le registraire du domaine et GitHub ; DIG16 membre
  du compte Cloudflare du client, jamais propriétaire ; mots de passe chez le client.
- HTTPS partout, en-têtes de sécurité déjà en place sur dig16.fr (audit du 14/10), repris sur chaque site client.
- Mentions d'information sous chaque formulaire et page « données personnelles » sur chaque site (`40` § B).

**Réagir** — fuite constatée ou soupçonnée : prévenir le client tout de suite ; l'aider à notifier la CNIL dans les
72 heures si un risque existe (modèle de clauses CNIL) ; corriger, puis noter la leçon.

**Limiter (CGV)** — annexe de sous-traitance RGPD (§ 4, art. 11).

## 4. Propositions de modification des CGV (à valider par l'utilisateur avant tout changement)

Les CGV privées (Drive « Dig », version du 08/10) prévoient déjà : client responsable des contenus qu'il fournit,
« meilleurs efforts » pour la disponibilité, responsabilité limitée aux 12 derniers mois. Ajouts proposés :

- **Art. 8 (contenus)** : « Le client garantit qu'il détient les droits sur les textes, photos, logos et vidéos qu'il
  fournit, et garantit DIG16 contre toute réclamation d'un tiers à leur sujet. Sur simple réclamation, DIG16 retire
  le contenu concerné sans délai et en informe le client. »
- **Art. 10 (disponibilité)** : « DIG16 est tenu d'une obligation de moyens. En cas d'interruption, DIG16 s'efforce de
  rétablir le site dans la journée ouvrée qui suit le signalement. »
- **Art. 11 (données)** : « Pour les formulaires du site, DIG16 agit comme sous-traitant du client au sens de
  l'article 28 du RGPD, selon l'annexe de sous-traitance jointe ; DIG16 informe le client sans délai de toute
  violation de données dont il a connaissance. » + annexe reprenant le modèle de clauses de la CNIL.
- **Art. 12 (responsabilité)** : ajouter « DIG16 ne répond pas des préjudices indirects, notamment perte de
  clientèle, de chiffre d'affaires ou d'image », en gardant le plafond des 12 derniers mois. Limites légales : la
  clause ne peut pas vider l'obligation essentielle de sa substance (art. 1170) et ne joue pas en cas de faute lourde
  ou dolosive (art. 1231-3).

**[Relecture par un professionnel du droit conseillée avant le premier client : CCI Charente ou permanence gratuite
d'avocats, à vérifier.]**

**18/10 (23 h 50)** : l'utilisateur veut être « irréprochable » en cas de litige et « ne pas perdre d'argent à
cause d'une erreur ou d'un oubli » → projet **« DIG16 – CGV v2 (PROJET à relire, 18-10-2026) »** créé dans le Drive
« Dig » (la version du 08/10 reste intacte) : les 4 ajouts ci-dessus + validation avant mise en ligne (art. 4 bis),
suspension après impayé et mise en demeure (art. 7), preuve par écrits et signature électronique (art. 12 bis),
amiable de 30 jours et conciliateur de justice (art. 13), annexe de sous-traitance RGPD.

## 5 bis. Litiges : ne jamais perdre d'argent par erreur ou oubli

**Les preuves, à chaque client** (rangées dans le dossier privé du client, Drive « Dig ») :
1. devis-bon de commande et CGV **signés** (signature électronique valable : Code civil, art. 1367, Légifrance) ;
2. vérification du client avant signature (annuaire officiel + BODACC, `outils/verif_entreprises.py`) ;
3. contenus et photos reçus, avec l'attestation de droits sur les photos ;
4. **accord écrit** du client sur la prévisualisation avant mise en ligne (art. 4 bis) ;
5. chaque demande de modification et sa date de réalisation (email), pour prouver le délai de 3 jours ouvrés ;
6. factures, mandat SEPA, relances et mises en demeure (`45-impayes-se-proteger.md`).
Règle : **tout accord important passe par écrit** (un appel est suivi d'un email récapitulatif le jour même).

**Les rappels automatiques** (déjà en place ou à créer au premier client) : impayé → procédure `45` ; échéance
de domaine du client ; fin d'engagement ; délai des modifications (alerte si une demande a plus de 2 jours ouvrés).

**En cas de désaccord** : réponse écrite sous 48 heures, calme et factuelle, sans reconnaître de faute avant d'avoir
vérifié ; Claude rédige, l'utilisateur valide (règle du brouillon validé) ; puis conciliateur de justice (gratuit) ;
conseil juridique gratuit avant toute réponse engageante :
- **Point-Justice, Maison de Justice et du Droit d'Angoulême**, rue René Pajot, 05 45 24 68 01 : consultation gratuite
  d'avocat le mercredi de 14 h à 17 h sur rendez-vous ; conciliateur de justice les 1er et 3e vendredis matin sur
  rendez-vous (fiche justice.gouv.fr, lue le 18/10/2026).

**La meilleure protection financière restante** : RC Pro (et éventuellement protection juridique) à comparer à la
première signature (`64`), car un contrat bien écrit limite une condamnation mais ne paie pas un avocat.

## 5. Ce qui reste à faire

| Quoi | Qui | Quand |
|---|---|---|
| Demande de rendez-vous par email (adresse officielle de la fiche justice.gouv.fr et du CDAD Charente, lue le 19/10) : envoyée le 18/10, puis **annulée** : l'utilisateur ira à la permanence de Ruffec ; confirmation de la date demandée à France Services Val de Charente ; dossier complet préparé (privé) | Claude | fait |
| Aller au rendez-vous avec le projet CGV v2 imprimé (l'avocat conseille sur place mais « n'accomplit aucun acte ni courrier » : pas de relecture par email, page du CDAD Charente lue le 18/10) : **permanence de Ruffec, jeudi 19/11/2026, 14 h 30-17 h 30, sans rendez-vous** | utilisateur | 19/11 |
| Intégrer les corrections de l'avocat et faire de la v2 la version officielle | Claude | après la relecture |
| Ajouter l'attestation « droits sur les photos » au questionnaire de lancement | Claude | avec les CGV |
| Étendre la sentinelle aux sites clients ; registre des médias ; modèle de formulaire sans stockage | Claude | au premier client |
| Remplacer FormSubmit sur dig16.fr par la fonction Cloudflare | Claude | après test du modèle |

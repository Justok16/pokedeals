# Audit total DIG16 du 11/11/2026 (8 lots)

Mission : `supports/prompt-audit-total-dig16.md`. Fait dans une conversation de service, entre 21 h et minuit (heure de
Paris), par Claude et 4 relecteurs en lecture seule (prix et prospection, juridique et fiscal, outils, organisation).
Point de départ : l'audit du 04/11 (`AUDIT_GLOBAL_DIG16.md`) et le ménage du 10/11 ; on ne reprend ici que ce qui a
changé ou leur a échappé. Aucun nom de prospect ni de client dans ce fichier.

Gravité : **CRITIQUE** (argent, loi, données personnelles, client perdu), **IMPORTANT**, MINEUR.
État : **CORRIGÉ** (fait et vérifié le 11/11), **OUI ATTENDU** (préparé, visible du public ou engageant : attend
l'accord de l'utilisateur), **AVOCAT** (question pour le 19/11), **À FAIRE** (inscrit dans `64` § 0), **À VÉRIFIER**
(non confirmé).

## Mesures du jour (preuves)

| Mesure | Résultat (11/11/2026) |
|---|---|
| `outils/test_pages.py` | 0 ALERTE, code 0 |
| `outils/controle_global.py` | 15/17 : 2 alertes dues à la machine neuve (module `playwright` absent, cookie du relais) |
| `outils/audit_securite.py https://dig16.fr` | 100/100 |
| `outils/test_formulaire.py site-dig` | OK, aucun refus CSP (essai local) |
| Site en ligne, téléphone 390 px (Playwright) | accueil : affichage principal en 0,8 s, aucun décalage ; 7 pages sans débordement |
| Site en ligne, ordinateur 1440 px, avec et sans mouvement réduit | accueil : 1,8 s et 0,8 s ; rien d'invisible après défilement |
| Liens des 8 pages publiques | 52 liens, aucun mort (Facebook répond 400 aux robots : normal) |
| Base des messages du formulaire (D1) | 2 messages (10/11), tous deux marqués lus |
| Search Console, 28 jours (12/10 au 08/11) | 7 pages indexées ; accueil 65 affichages et 9 clics ; requêtes : presque uniquement « dig16 » ; page Charente : 0 affichage |
| Tests GitHub de la PR 118 | 4 sur 4 verts ; aucune issue « Alerte DIG16 » ouverte |
| Kit client, 3 clients fictifs (Essentiel, Visibilité, Achat) | produit après correction de l'outil ; aucun marqueur `[...]` restant |
| Sauvegarde du journal privé (Drive « Dig ») | un document par jour depuis le 09/11, dernier le 11/11 à 19 h 53 |

Non vérifié, et pourquoi : envoi réel d'un message d'essai sur le formulaire en production (refusé par la protection
de l'outil : non contourné) ; Indy et GoCardless (aucune connexion possible) ; journal privé `ETAT.md` (il vit dans
LA conversation) ; historique complet du dépôt (copie partielle : 51 derniers commits, aucun secret trouvé dedans) ;
restauration réelle du journal depuis le Drive (les documents existent, la reconstitution n'a pas été rejouée).

## Lot A — Parcours du prospect

| # | Constat | Gravité | Preuve | Correction | État |
|---|---|---|---|---|---|
| A1 | Cloudflare ajoute seul son script « Web Analytics » sur chaque page ; la règle de sécurité le bloque (aucune donnée ne part), mais chaque page affiche une erreur dans le navigateur. L'audit du 04/11 avait retiré ce service de la règle sans couper l'injection | IMPORTANT | Playwright sur dig16.fr : erreur « violates Content Security Policy » sur 7 pages ; `curl` avec un navigateur : balise `beacon.min.js` présente ; absente de `site-dig/index.html` | Couper « Web Analytics » dans le compte Cloudflare (l'en-tête `no-transform` le couperait aussi, mais désactive la compression : écarté ; aide Cloudflare « Web Analytics FAQ », lue le 11/11) | OUI ATTENDU (compte de l'utilisateur) |
| A2 | `audit_securite.py` annonce « 0 script tiers » : il lit la page sans se présenter comme un navigateur, donc ne voit pas le script ajouté par Cloudflare | MINEUR | sortie du 11/11 comparée à A1 | Lire la page avec un vrai navigateur dans cet outil | À FAIRE |
| A3 | Plan du site : dates de modification périmées (accueil et « Le projet » datés du 18/10, modifiés le 11/11) | MINEUR | `site-dig/sitemap.xml` | Mettre les dates à jour à la prochaine mise en ligne | OUI ATTENDU (site) |
| A4 | Paiement des formules payées en une fois : 3 règles différentes (CGV et devis : 30 jours après facture, sans acompte ; fiche 45 : acompte 30 à 50 % puis solde avant la mise en ligne ; kit : les deux dans la même phrase) | **CRITIQUE** | `supports/cgv-dig.html:46` ; `45-impayes-se-proteger.md:20` ; `outils/kit_client.py` (« acompte convenu au devis ») | Une seule règle, à choisir ; fiche 45 annotée | AVOCAT, fiche 45 CORRIGÉE |
| A5 | Les CGV en vigueur ne contiennent pas la « mise en pause du site en cas d'impayé » que la fiche 45 annonçait ; elle n'est que dans le projet v2 privé | **CRITIQUE** | 0 occurrence de « pause » ou « suspen » dans `supports/cgv-dig.html` et `outils/documents_commerciaux.py` | Valider la v2 le 19/11, puis régénérer CGV, devis et PDF ; fiche 45 annotée | AVOCAT, fiche 45 CORRIGÉE |
| A6 | Promesse retirée encore écrite : « mise en ligne à J+7 » dans le guide de prospection (et son PDF) | IMPORTANT | `supports/guide-prospection.html:267` | « date de mise en ligne écrite sur le devis » ; régénérer le PDF | À FAIRE (avec A7) |
| A7 | Démo « déjà refaite » et « envoyée par SMS ou email » encore dans les textes d'appel, contre la règle « accord d'abord, montrée en direct » ; la page d'accueil dit aussi « je vous l'envoie » | IMPORTANT | `41-prospection-questionnaire-et-textes.md:46-48` ; `50-campagne-lancement.md:70` ; `site-dig/index.html` (question « La démo est-elle vraiment gratuite ») | Aligner 41, 50 et le guide ; le site : « je vous la montre » | À FAIRE (fiches), OUI ATTENDU (site) |
| A8 | Nom de domaine : « payé par vous directement » dans les textes d'appel, « avancé par DIG16 et refacturé » dans les CGV, le devis et le kit. Avancer l'argent contredit le budget 0 € et la refacturation compte dans le chiffre d'affaires (seuil CFE de 1 164 € en 2026) | IMPORTANT | `supports/cgv-dig.html` art. 3 ; devis fictif du 11/11 ; `41:174` | Avis : le client paie lui-même le registraire pendant le rendez-vous de 20 minutes (compte déjà à son nom) | OUI ATTENDU (CGV) |
| A9 | Parrainage : le site promet « un mois offert » sans plafond ; la fiche 47 plafonne à 79 € et se contredit (ligne 28) | IMPORTANT | `47-parrainage.md:28` et `:84-88` | Écrire le plafond partout, ou le supprimer | OUI ATTENDU |
| A10 | Offre aux adhérents de l'association des professionnels (Essentiel à 29 €/mois à vie, sans durée ni nombre) : absente du kit, qui sortirait un devis à 49 € avec 6 mois | IMPORTANT | `47-parrainage.md:93-101` ; `outils/kit_client.py` | Ajouter le cas au kit avant le premier adhérent. Avis franc : sans plafond ni date, ce prix peut devenir le prix de fait à Ruffec (−41 % à vie) ; proposer « les 10 premiers » ou une date limite | OUI ATTENDU |
| A11 | Prix hors grille déjà envoyés à un prospect (page en plus 90 €, galerie automatique 190 €, carnet de 5 modifications 150 €) : écrits nulle part comme référence | IMPORTANT | `64` § 0, ligne du 29/10 | Petite grille « suppléments » dans `39` | À FAIRE |
| A12 | Rapport mensuel : « combien d'appels » promis à l'oral, le site ne promet que visites et demandes | MINEUR | `supports/guide-prospection.html:242` | Dire « visites et demandes » | À FAIRE |
| A13 | Fiche presse, réseaux abandonnés encore cités comme priorités (LinkedIn, Pinterest, Bluesky) dans `50`, « 7 jours » au lieu de « 8 jours » sans paiement dans le guide et `41` | MINEUR | `50:194-198` ; `guide-prospection.html:100` | Mise à jour des fiches | À FAIRE |
| A14 | Antisèche : la source (`antiseche.py`) et le fichier produit ne disent plus la même chose (réponses 5, 32, 49) | À VÉRIFIER | signalé par le relecteur ; « 7 jours » non retrouvé par recherche exacte | Comparer, corriger la source, régénérer | À FAIRE |

Zones propres : prix et formules identiques entre le site, la facture, `documents_commerciaux.py`, la fiche presse,
les publications à venir, les textes YouTube, les annuaires, le service devis-factures. Aucun « le plus choisi »,
« satisfait ou remboursé », Malt ni Udemy.

## Lot B — Prospection

| # | Constat | Gravité | Preuve | Correction | État |
|---|---|---|---|---|---|
| B1 | La fiche d'appels fait dire « Je ne vends rien aujourd'hui » et finit par « d'ici quelques semaines » : texte de l'étude de marché d'avant la création. Aucun appel ne demande une démo ni une date, alors que le guide dit l'inverse | **CRITIQUE** (client perdu) | `outils/prospects/fiche_appel.py:226-229` ; `supports/guide-prospection.html:94` et `:99` | Nouvelle ouverture et nouvelle fin proposées à l'utilisateur le 11/11 au soir (aucun prix au téléphone) | OUI ATTENDU |
| B2 | Trop peu d'appels : 0 appel à froid en octobre, quelques-uns le 03/11, contre 10 par semaine décidés le 01/11 | **CRITIQUE** (client perdu) | `archives/64-liste-unique-terminees.md:14` ; `64` § 0 | Tenir les deux créneaux (mardi, jeudi) : c'est l'action n° 1 | utilisateur |
| B3 | Aucun endroit unique avec, par prospect, un état et une date de relance (5 supports différents) ; résultats du 03/11 jamais reportés dans `64` | IMPORTANT | `50` § 8 ; `57:95-110` ; `64` § 0 « aucun appel noté depuis le 21/10 » | Une seule feuille privée (état, prochaine action, date) ; rattrapage depuis le 03/11 | À FAIRE (LA conversation) |
| B4 | L'ouverture de la fiche 57 parle encore d'une entreprise « en préparation » | IMPORTANT | `57-entretiens-etude-de-marche.md:36-37` | Réécrire au présent, citer l'article du 10/11 | avec B1 |
| B5 | La fiche d'appels part à 13 h 11 pour des appels à 14 h, et 3 autres tâches tombent dans la même heure le jeudi 12/11 | IMPORTANT | tâches planifiées lues le 11/11 (`list_triggers`) | Préparer la fiche le matin ; déplacer les 2 suivis de 14 h 23 après 16 h | proposé le 11/11 |
| B6 | Les 3 pistes ouvertes sont des proches ou des petits prix (site offert, −50 %, attente de trésorerie) : aucune ne valide le prix public | IMPORTANT | `64` § 0 | Voir les 3 actions ci-dessous | — |

Les 3 actions les plus rentables d'ici 30 jours :
1. **Des appels qui demandent quelque chose** : un seul texte d'une page, 10 appels par semaine (environ 40 en 30 jours),
   but mesurable : 5 démos acceptées, 2 rendez-vous. Claude : 1 h. Utilisateur : 4 h par semaine.
2. **Le réseau chaud avant le froid** : adhérents de l'association des professionnels, article de presse du 10/11 comme
   preuve, soirée des entreprises du 30/11, relance du maçon le 25/11. Claude : 1 h. Utilisateur : 6 à 7 h.
3. **Un seul tableau de suivi et des papiers sûrs avant de signer** (A4, A5, A10 réglés après l'avocat du 19/11).
   Claude : 3 à 4 h. Utilisateur : 30 minutes de validation, puis 2 minutes par appel.

## Lot C — Parcours client (essai à blanc)

| # | Constat | Gravité | Preuve | Correction | État |
|---|---|---|---|---|---|
| C1 | `kit_client.py` plantait au premier champ manquant (`KeyError`), sans modèle public : le seul exemple était le fichier privé d'un ancien dossier, perdu à chaque changement de machine | IMPORTANT | essai du 11/11 : `KeyError: 'numero_facture'` | Contrôle de tous les champs d'un coup + `supports/kit-client/exemple-dossier-fictif.json` et `exemple-prestataire-fictif.json` ; skill mis à jour | CORRIGÉ (2 essais : refus clair, puis kit complet) |
| C2 | Fiche « Vos comptes », point 3 : « vous recevez un email de confirmation : un clic suffit pour activer le formulaire ». C'est l'ancien service, retiré le 05/11. Aucune solution n'est décidée pour le formulaire des sites clients | IMPORTANT | PDF fictif du 11/11 ; `supports/kit-client/vos-comptes.html` ; `64` § 0 ligne « Site » | Décider avant le premier client : fonction Cloudflare sur le compte du client, avec envoi du message à son adresse vérifiée (à lire dans l'aide Cloudflare avant de promettre) | À FAIRE (première signature) |
| C3 | Le contrôle du client avant signature passe par le relais Vercel (réservé à l'usage non commercial, cookie expiré sur machine neuve) | IMPORTANT | skill `nouveau-client`, étape 1.3 ; `controle_global.py` du 11/11 | Lire le BODACC par son accès public direct, sans relais | À FAIRE (première signature) |
| C4 | Facture émise le jour de la mise en ligne, mais premier mois réglé avant : un paiement sans facture | IMPORTANT | `72-kit-client-complet.md:20` ; `kit_client.py` (LISEZMOI) | Facture du premier mois à la demande de paiement (à partir du 8e jour) | AVOCAT puis À FAIRE |
| C5 | Devis, facture et CGV : « SIREN » seul, sans « RCS Angoulême » (présent sur le site) | IMPORTANT, à confirmer | `supports/modele-devis.html:39`, `modele-facture.html:39`, `cgv-dig.html:40` ; article R123-237 du code de commerce (extrait lu le 11/11) | Ajouter la mention une fois la nature de l'activité tranchée (D4) | AVOCAT |
| C6 | Limites gratuites : DocuSeal 10 demandes de signature par mois (relu le 10/11), 4 modèles présents dans le compte (vérifié le 11/11) ; un kit = 2 à 4 envois | MINEUR | `search_templates` du 11/11 ; `.claude/hooks/quotas.json` | Compter avant chaque kit (déjà dans le garde-fou) | — |
| C7 | Indy et GoCardless : rien n'a pu être essayé (pas de connexion) ; le premier vrai prélèvement et la première vraie facture n'ont jamais été joués | À VÉRIFIER | — | Essai à 1 € sur soi-même ou sur le site offert, le jour venu | À FAIRE (première signature) |

## Lot D — Juridique et fiscal (signalements, pas un avis)

| # | Constat | Gravité | Preuve (pages lues le 11/11/2026) | Correction | État |
|---|---|---|---|---|---|
| D1 | Appels de prospection à des professionnels : **autorisés** sans accord préalable (l'interdiction du 11/08/2026 vise le consommateur) ; conditions : objet lié au métier, dire d'où vient le numéro si on le demande, respecter le refus | CRITIQUE, sans blocage | code de la consommation, art. L223-1 (en vigueur le 11/08/2026) ; CNIL, « Prospection commerciale par téléphone », page du 10/06/2026 | Phrase prête sur l'origine du numéro ; liste privée « ne plus appeler » | À FAIRE (avec B1) |
| D2 | Mentions légales : « Aucun autre service ne les reçoit » (messages du formulaire), alors qu'un assistant d'intelligence artificielle (société américaine) les relit chaque jour | **CRITIQUE** | `site-dig/mentions-legales.html` § 4 ; `site-dig/functions/api/contact.js:5` ; service-public F37351 (vérifié le 13/10/2026) : destinataires et transferts à indiquer | Phrase à corriger après avis | AVOCAT puis OUI ATTENDU |
| D3 | Mentions légales : numéro de téléphone de l'hébergeur absent (nom, adresse et site présents) | **CRITIQUE**, correction facile | F37351 : « adresse et numéro de téléphone » de l'hébergeur ; numéro lu sur cloudflare.com/privacypolicy le 11/11 | Ajouter la ligne « Téléphone : +1 650 319 8930 » | OUI ATTENDU |
| D4 | Nature de l'activité toujours ouverte (commerciale ou libérale) : le taux de cotisations et la mention « RCS » en dépendent | **CRITIQUE** (argent) | `31-creation-entreprise.md` § 2 bis ; mail au SIE du 05/11 sans réponse | Suivi du 12/11, relance le 19/11 (déjà programmés) | en cours |
| D5 | URSSAF : la fiche écrivait « 05/01/2027 » ; c'est l'ouverture. Date limite : **30/04/2027**, deux déclarations | IMPORTANT | autoentrepreneur.urssaf.fr « Déclarer et payer mes cotisations » ; F23257 (vérifié le 01/01/2026) | `PLAN_ACTION_DIG16.md` § C corrigé | CORRIGÉ |
| D6 | Identifiants de tâches écrits dans les fiches : tous périmés depuis le 10/11 | IMPORTANT | `list_triggers` du 11/11 | Plan § C : noms des tâches ; règle « on écrit le nom, jamais l'identifiant » | CORRIGÉ (plan), À FAIRE (`64`) |
| D7 | Mesure d'audience : la preuve d'exemption du prestataire manque toujours ; la phrase « seules … sont transmises » oublie l'adresse IP et le navigateur, reçus par toute requête | IMPORTANT | CNIL, page du 04/07/2025 ; `site-dig/mentions-legales.html` § 5 | Corriger la phrase ; obtenir l'écrit ou passer au compteur interne | AVOCAT |
| D8 | Médiation de la consommation : « ne s'applique pas » ; douteux pour un client de 5 salariés au plus qui signe hors établissement | IMPORTANT | F33527 (vérifié le 01/07/2026) | Ne rien changer avant l'avocat | AVOCAT |
| D9 | Démos : 34 images ou films sans ligne de source (paysagiste : 10 sur 10 ; Prestige : 18 ; visite du menuisier : 6) ; 8 à 10 photos avec des personnes | IMPORTANT | comparaison `site-dig/demos/*/` et `supports/sources-photos-*.md` | Retrouver chaque source ; remplacer sinon ; regarder les visages | À FAIRE |
| D10 | Conservation « 3 ans » des messages : aucune purge prévue | IMPORTANT | `site-dig/mentions-legales.html` § 4 ; aucun outil | Étape au garde-fou mensuel | À FAIRE |
| D11 | CFE 2027-2028 à 0 € (seuil ramené à l'année) et délibération locale d'exonération : à confirmer par écrit | IMPORTANT | F23999 (vérifié le 26/03/2026) ; F31139 (vérifié le 21/02/2026) | Questions déjà posées au SIE ; ne cocher la ligne que si la délibération existe | en cours |
| D12 | Fiches 35 et 40 dépassées (pseudonyme, lien devenu la fiche « cookies », rien sur le téléphone) ; date des mentions légales différente dans le texte et dans les données structurées | MINEUR | `35:1`, `40:65-66`, `mentions-legales.html:75` et `:82` | Mise à jour | À FAIRE |

Conforme aux sources relues le 11/11 : seuils de franchise de TVA (37 500 € et 41 250 €), plafond micro (83 600 €),
pénalités de retard (12,40 % au 2e semestre 2026, 40 €), mentions de facture, calendrier de la facture électronique,
CFE avant le 31/12, régime micro admis en zone FRR+, courriel entre professionnels.

Questions pour l'avocat du 19/11 (à ajouter à sa liste) :
1. Client de 5 salariés au plus signant hors de nos locaux : faut-il désigner un médiateur de la consommation ?
2. Un artisan appelé sur son portable pour son activité est-il bien un « professionnel » ; que lui dire sur l'origine de son numéro ?
3. Acompte, suspension du site après impayé, plafond de responsabilité : valables face à un très petit professionnel ?
4. Faut-il citer l'assistant d'intelligence artificielle qui lit les messages du formulaire, et avec quelle garantie de transfert ?
5. Le compteur de visites sans cookie, confié à un prestataire, peut-il rester sans accord ni moyen de s'y opposer ?
6. La fonction « se rétracter en un clic » (19/06/2026) s'applique-t-elle à nos devis signés en ligne ?
7. Si l'activité est jugée libérale : faut-il corriger l'immatriculation et la mention « RCS » ?
8. Peut-on préparer en privé une démo avec les photos et le logo d'un prospect avant son accord écrit ?
9. Facture du premier mois : à émettre au paiement (avant la mise en ligne) ou à la mise en ligne ?

## Lot E — Sécurité et vie privée

| # | Constat | Gravité | Preuve | Correction | État |
|---|---|---|---|---|---|
| E1 | Noms de 5 prospects, d'un client et d'un contact dans des fiches du dépôt public | **CRITIQUE** | `connaissances/lecons.md` (03/11), `64`, `72`, `66`, archives, `lecons-detail.md`, `effets-prestige.md`, `46-registre-videos.md` | Remplacés par le métier ou le rôle dans 12 fichiers ; l'historique n'est pas réécrit (règle) | CORRIGÉ (recherche finale : 0 résultat) |
| E2 | Le crochet `noms_prives.py` lit les noms dans les fichiers privés de la machine : sur une machine neuve il ne bloque rien | IMPORTANT | `.claude/hooks/noms_prives.py` ; dossier privé vide le 11/11 | Garder dans le dépôt des empreintes salées des noms, jamais les noms | À FAIRE |
| E3 | L'adresse personnelle de l'utilisateur est dans 2 fichiers hérités de PokéDeals | connu | `scraper/config.yaml` (décision du 06/10 : laissé tel quel) et `scraper/notifications_perso.py` | Non reproposé (consigne) | — |
| E4 | Site : 100/100, en-têtes complets, `www` et l'ancienne adresse redirigent, certificat valable 52 jours (renouvellement automatique) | — | mesures du jour | — | propre |
| E5 | Dépôt : aucune clé ni jeton dans les fichiers DIG16 ni dans les 51 derniers commits ; tests GitHub verts | — | `detect-secrets` (2 faux positifs), recherche par motifs | Historique plus ancien non relu ici | À VÉRIFIER |
| E6 | Sauvegarde du journal privé : ajouts quotidiens présents ; jamais de reconstitution complète rejouée | IMPORTANT | Drive « Dig », 7 documents du 09 au 11/11 | Rejouer une restauration une fois (LA conversation) | À FAIRE |

## Lot F — Outils et automatisations

| # | Constat | Gravité | Preuve | Correction | État |
|---|---|---|---|---|---|
| F1 | Sur une machine neuve, le module `playwright` n'était toujours pas là 20 minutes après le démarrage : l'installation « en arrière-plan » du 10/11 est tuée à la fin du crochet | IMPORTANT | `ModuleNotFoundError` le 11/11 ; `.claude/settings.json` | Installation directe, limitée à 100 s, comme les autres modules | CORRIGÉ (à confirmer au prochain démarrage) |
| F2 | Le point du matin cite encore un chemin de navigateur daté qui n'existe plus | IMPORTANT | texte de la tâche lu le 11/11 | Remplacer par `/opt/pw-browsers/chromium` | proposé (tâche planifiée) |
| F3 | Short du jeudi 19/11 prévu par Zapier (100 sur 100) : il échouera | MINEUR | `videos/conseils/youtube-shorts.md:33` ; `quotas.json` | Calendrier annoté : vidIQ ou à la main | CORRIGÉ |
| F4 | Relais Vercel : point de panne unique (résumés, contrôle du son, contrôle des entreprises), réservé à l'usage non commercial, cookie à renouveler chaque jour par une tâche à part alors que le point du matin le fait déjà | IMPORTANT | `64` § 0 (10/11) ; 2 tâches lues le 11/11 | Désactiver la tâche du cookie ; remplacement prévu à la première signature | proposé |
| F5 | Environ 185 réveils automatiques par mois dans LA conversation ; la veille quotidienne suit encore une trentaine de chaînes de finance alors que la finance est arrêtée ; veille des outils chaque jour en plus du point du matin ; sauvegarde une heure après le contrôle du soir | IMPORTANT | `list_triggers` ; `outils/veille_sources.py:223-262` ; `veille/2026-11-11.md` | Limiter la veille aux 3 chaînes utiles ; veille des outils le lundi ; sauvegarde = dernière étape du contrôle du soir : environ 90 réveils par mois | proposé |
| F6 | Crochet `reprise_finance.sh` neutralisé mais encore lancé à chaque démarrage et à chaque message | MINEUR | `.claude/settings.json` | Retirer les 2 entrées | proposé |

| F7 | 4 modules du parcours client manquaient sur une machine neuve (PDF remplissables, QR code du kit avis, flyer, contrat) : la fiche d'appels et le kit avis ne tournaient pas | **CRITIQUE** | `kit_avis.py --help` et `pdf_remplissable.py --help` : `ModuleNotFoundError` (11/11) | `outils/requirements.txt` + crochet de démarrage direct | CORRIGÉ (installés et vérifiés ; `kit_avis.py --help` répond) |
| F8 | Garde-fou des quotas : visait des noms de connecteurs qui changent selon la session, et laissait passer sur une entrée illisible | IMPORTANT | `.claude/settings.json` ; essai avec entrée vide : erreur Python sans refus | Reconnaît l'outil par la fin de son nom ; refuse s'il est en panne | CORRIGÉ (3 essais : entrée vide refusée, Metricool plein refusé, DocuSeal compté) |
| F9 | Test automatique du site sur GitHub : 3 exécutions annulées depuis le 05/11 (blocage sur l'installation d'un paquet) ; les dernières mises en ligne n'ont pas été validées par ce filet | IMPORTANT | relevé du relecteur (API GitHub, 10 et 11/11) | Nouvelles tentatives et délai court sur cette étape | CORRIGÉ dans le fichier ; vert à confirmer à la prochaine exécution |
| F10 | Les crochets « secrets » et « noms » ne voient que `git commit` ; une écriture par le connecteur GitHub les contourne | IMPORTANT | `.claude/settings.json` | Interdire les 2 outils d'écriture directe du connecteur (réglage des permissions : décision de l'utilisateur) | proposé |
| F11 | Messages du formulaire : rangés dans la base seulement, sans notification ni export ; lus par les 2 passages de Claude | IMPORTANT | `site-dig/functions/api/contact.js` | Export hebdomadaire vers le Drive ; notification à étudier | À FAIRE |
| F12 | Inventaire : aucune licence notée pour les 77 outils ; environ 45 skills installés absents de l'inventaire ; 7 skills sans fichier de licence ; la phrase surveillée de la licence GSAP n'existe plus que dans un commentaire caché de la page | IMPORTANT | `connaissances/inventaire-outils.json` ; page gsap.com/community/standard-license lue le 11/11 (usage commercial gratuit confirmé) | Champ « licence » ; partie skills générée ; phrase surveillée à changer | À FAIRE |
| F13 | Le document « accord de réalisation gracieuse » décrit encore l'ancien formulaire | IMPORTANT | `outils/accord_gracieux.py:54-59` | Réécrire avec la solution retenue en C2 | À FAIRE (première signature) |
| F14 | `CARTE.md` ignorait 47 scripts des sous-dossiers | MINEUR | `outils/carte.py:81` | Parcours des sous-dossiers | CORRIGÉ (237 lignes) |
| F15 | Points de panne sans solution de secours écrite : GitHub (aucune copie ailleurs), Drive, base des messages, Indy, GoCardless, et Claude lui-même pour la relève des messages | IMPORTANT | relevé du relecteur | Une page « si X tombe » ; export mensuel du dépôt | À FAIRE |

Relevé des 117 scripts (relecteur « outils ») : tous compilent ; environ 45 servent au quotidien, 34 au premier client,
36 sont hérités de la chasse de septembre ou des vidéos finance (archivables) ; 1 seul est cassé par son code
(`prospects/etape0_doublons.py`, chemin d'une ancienne machine en dur), 3 autres par un fichier absent
(`lire_reel.py`, `prospects/publier_maquettes.py`, `prospects/vers_site.py`). Tests : compta 13 sur 13, repreneurs
5 sur 5, audit de migration 50 sur 50. 14 scripts citent encore le relais Vercel.

## Lot G — Référencement et visibilité

| # | Constat | Gravité | Preuve | Correction | État |
|---|---|---|---|---|---|
| G1 | Les 7 pages sont indexées, mais le site n'apparaît presque que sur son propre nom : 4 requêtes en 28 jours, dont « dig16 » | IMPORTANT | Search Console, 12/10 au 08/11 | Normal à un mois ; ce qui manque : des avis sur la fiche Google (0) et des liens locaux (l'article de presse ne cite pas l'adresse du site) | — |
| G2 | Page « création de site internet en Charente » : indexée le 05/11, 0 affichage | MINEUR | même source | Attendre la mesure du 07/12 ; ne rien construire de plus | — |
| G3 | 2e interview de presse : demander que l'adresse dig16.fr soit écrite (lien local le plus utile du moment) | IMPORTANT | article du 10/11 : adresse absente de la partie visible (`64` § 0) | Déjà dans la tâche du 24/11 | — |
| G4 | Le premier avis Google viendra du premier client ou du site offert : c'est le vrai levier de la carte locale (concurrents : 19 à 99 avis) | IMPORTANT | `67` § 7 (05/11) | Kit avis dès la première mise en ligne | première signature |
| G5 | Réseaux : beaucoup de publications, très peu de contacts (octobre : 17 visites venues de Google, 3 d'Instagram ; le seul prospect chaud est venu d'Instagram puis d'un appel) | IMPORTANT | `archives/64-liste-unique-terminees.md:14` | Pas de série 3 avant le premier client (déjà décidé) ; le temps gagné va aux appels | — |

Non mesuré ce soir (pour ne pas consommer de crédits) : positions dans la carte locale, cohérence nom-adresse-téléphone
relue sur chaque annuaire (dernière lecture : 11/11 pour la fiche Google, 18/10 pour PagesJaunes).

## Lot H — Organisation et mémoire

| # | Constat | Gravité | Preuve | Correction | État |
|---|---|---|---|---|---|
| H1 | La règle « une seule conversation » est contredite par 3 leçons du 10/11 et par la tâche du 24/11 (« dans une AUTRE conversation ») | IMPORTANT | `.claude/CLAUDE.md` ; `connaissances/lecons.md` (10/11) | Leçons annotées « remplacé le 11/11 » ; tâche : proposé | CORRIGÉ (leçons) |
| H2 | `64` § 0 : 44 000 caractères, dont la moitié dans 9 lignes de plus de 1 500 caractères, relus « en entier » par plusieurs tâches (environ 12 000 jetons à chaque fois) | IMPORTANT | mesure du relecteur | 10 réécritures courtes prêtes (rapport du relecteur) ; le texte long part aux archives | À FAIRE (accord : réécriture de la liste de l'utilisateur) |
| H3 | Horaires périmés encore écrits comme actifs (relevés du courrier 3 fois par jour, 17 h 52, 19 h 07, « 2 fois par jour ») ; « À lancer » pour les entretiens alors que les appels ont commencé ; dates passées présentées comme à venir | IMPORTANT | `64:79`, `:83`, `:55`, `:86`, `:89` ; `consignes-detaillees.md:134` | Nettoyage de `64` avec H2 | À FAIRE |
| H4 | `consignes-detaillees.md` « fait foi pour le détail », mais 14 règles de `CLAUDE.md` n'y sont pas ; veille des sources « en pause » ou « quotidienne » selon la ligne ; chaînes de finance encore « en priorité » | IMPORTANT | `consignes-detaillees.md:4`, `:137`, `:181-188` | Phrase « en cas d'écart, `CLAUDE.md` prime » + mise à jour | À FAIRE |
| H5 | Deux fichiers portent le numéro 64 ; CFE et SIE suivis dans 6 lignes différentes | MINEUR | `CARTE.md` ; `64:9`, `:10`, `:12`, `:37`, `:46`, `:64` | Renommer le plan SEO ; une seule ligne « Fiscal » | À FAIRE |
| H6 | 15 fiches de septembre et début octobre ne sont plus citées nulle part (audits externes, vidéos, intégrations) | MINEUR | recherche du relecteur | Les passer en « archives » dans `CARTE.md` | À FAIRE |
| H7 | Exception « flyer A5 » du 04/11 absente de `64`, `61` et `69`, qui disent encore « sans flyer papier » | MINEUR | `64:62`, `61:28`, `69:98` | Ajouter la mention | À FAIRE |

## Ce qui ne vaut pas la peine (dit franchement)

- Refaire des publications, des vidéos ou une série 3 avant le premier client : les chiffres d'octobre montrent que
  cela n'apporte presque aucun contact.
- Peaufiner encore le site : il est rapide, propre et sans alerte ; les seules corrections utiles sont les mentions
  légales (D2, D3) et le script Cloudflare (A1).
- Poursuivre la page « Charente » ou des pages en plus avant la mesure du 07/12.
- Le service « devis-factures » : rien avant un premier client de site.
- Réécrire toutes les fiches de septembre : les archiver suffit.

## Journal des corrections du 11/11 (toutes réversibles par l'historique git)

| Changement | Fichiers | Vérification |
|---|---|---|
| Noms remplacés par le métier ou le rôle | 12 fiches et 1 outil | recherche finale sans résultat |
| Kit client : contrôle des champs, exemples fictifs | `outils/kit_client.py`, `supports/kit-client/exemple-*.json`, skill `nouveau-client` | refus clair sur dossier incomplet ; kit complet sur l'exemple |
| Crochets de démarrage (`playwright`, modules du parcours client), garde-fou des quotas, test GitHub du site, carte | `.claude/settings.json`, `outils/requirements.txt`, `.claude/hooks/quota_publications.py`, `.github/workflows/test_site_dig.yml`, `outils/carte.py` | JSON valide, modules importés, 3 essais du garde-fou ; effet des crochets à confirmer au prochain démarrage |
| Échéances : URSSAF 30/04/2027, noms des tâches | `audit-2026-11/PLAN_ACTION_DIG16.md` | relu |
| Fiche impayés annotée ; rapport RGPD ; calendrier des Shorts | `45`, `CONFORMITE_RGPD_DIG16.md`, `videos/conseils/youtube-shorts.md` | relu |
| Leçons du 11/11 et tâches ouvertes | `connaissances/lecons.md`, `64` § 0 | relu |

Rien n'a été modifié sur le site public, dans les comptes, ni dans les tâches planifiées. Aucun mail envoyé.

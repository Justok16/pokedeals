# 73 — Audits externes Grok et Gemini du 11/11/2026 : vérifications et suites

Réponses collées par l'utilisateur le 11/11 au soir au prompt `supports/prompt-audit-total-ia-externes.md`.
Règle : chaque affirmation d'une autre IA est revérifiée à la source avant d'être retenue. Vérifications faites le
11/11/2026 dans les fichiers du site (`site-dig/`), sur le site en ligne (Playwright, téléphone 390 px) et dans la
Search Console. Aucune donnée personnelle ici. Rien n'est mis en ligne sans le « oui » de l'utilisateur, et rien avant
les appels du jeudi 12/11. Complète `audit-2026-11/AUDIT_TOTAL_2026-11-11.md`.

## 1. Grok : 23 constats

| # | Affirmation | Vérification | Verdict | Suite |
|---|---|---|---|---|
| 1 | Premier écran : ni prix, ni nom, ni bouton d'appel | Capture téléphone : le nom DIG16 est visible ; aucun prix ; la barre « Appeler / Démo gratuite » est cachée au premier écran et n'apparaît qu'après défilement (`index.html:666` et `:757`) | **Vrai en partie** | Proposition 1 |
| 2 | Aucune preuve d'un vrai client | Démos annoncées « entreprises fictives » | Vrai, connu | Premier client, site offert |
| 3 | Deux phrases sur la propriété | « à votre nom, dès le départ » et « Après les 6 premiers mois, vous partez… avec votre site » : la première parle du nom, la seconde du départ ; le kit dit que le code est cédé « au fur et à mesure des paiements et au plus tard à la fin de l'engagement » | **Vrai** (ambigu) | Proposition 2 |
| 4 | Aucune condition générale en ligne | Aucune page CGV dans `site-dig/` | **Vrai** | Après l'avocat du 19/11 |
| 5 | `llms.txt` : « 6 mois » sans l'exception Prestige | `site-dig/llms.txt`, ligne « Formules mensuelles : 6 mois d'engagement » ; l'accueil précise « 12 mois pour Prestige » | **Vrai** | Proposition 3 |
| 6 | « Réservation en ligne incluse » sous les formules courantes, sans démo qui la montre | Phrase présente sous les 3 cartes ; la démo Prestige a une réservation, pas les démos Essentiel et Visibilité | **Vrai** | À décider : la garder (et la prouver par une démo) ou la limiter à Prestige |
| 7 | « 7 j/7 joignable » et horaires 00:00-23:59 dans les données structurées | `index.html`, données `ProfessionalService` : tous les jours 00:00-23:59 ; la fiche Google est « sans horaires standards » (leçon du 27/10 : jamais un faux 24 h/24 chez Google) | **Vrai** | Proposition 4 |
| 8 | Démo « à partir des informations publiques » contre « avec vos textes et vos photos » | La première phrase parle de la démo, la seconde du site final | **Faux** (pas de contradiction) | Rien |
| 9 | Test du pouce : « Rien n'est enregistré » alors que le compteur de visites est chargé | Phrase et `mesure.js` présents sur la page | **Vrai** (phrase trop large) | Proposition 5 |
| 10 | Mentions : base légale pour le formulaire seulement | 1 seule « Base légale » dans la page ; rien pour la mesure d'audience | **Vrai** | Avocat (question 5 de l'audit) |
| 11 | « Le projet » : aucun nom de personne | Exact ; le nom est dans les mentions légales | Vrai | Décision de l'utilisateur ; non proposé |
| 12 | Nom et comptes différents | Connu (`64` § 0) | Vrai, connu | 2e interview : « DIG16 » sans espace |
| 13 | X : très peu de vues | Non mesuré ce soir | À vérifier | Point du lundi ; arrêt = décision de l'utilisateur |
| 14 | Absent sur « création site internet Charente » | Search Console, 28 jours : page Charente 0 affichage | Vrai, connu | Mesure du 07/12 |
| 16 | Facture « conforme… y compris la facturation électronique » | Phrase en ligne ; l'émission électronique n'est obligatoire pour une micro-entreprise qu'au 01/09/2027 (service-public F31808, vérifié le 11/08/2026) ; seule la réception est en place | **Vrai** (promesse en avance) | Proposition 6 |
| 17 | « C'est une obligation légale pour les contrats signés chez vous » | Vrai seulement pour un client de 5 salariés au plus, hors de son activité principale (art. L221-3) | **Vrai en partie** | Avocat (question 1) ; proposition 7 |
| 18 | Franchise de TVA cohérente | Seuils relus (F21746) | Vrai | Rien |
| 19 | Prix bas face aux concurrents | Prix des concurrents non relus | À vérifier | Aucun usage sans relecture |
| 20 | « Le projet » ne cite que 2 formules | Essentiel et Visibilité seulement ; règle du 21/10 : Prestige toujours cité avec les autres | **Vrai** | Proposition 8 |
| 21 | Technique correcte ; promesse « moins de deux secondes » | Phrase introuvable sur l'accueil ; mesuré : 0,8 s sur téléphone | Faux pour la promesse | Rien |
| 22 | « Aucune fiche PagesJaunes » | Fiche en ligne depuis le 18/10 (`64` § 0) | **Faux** | Rien |
| 23 | « Qui écrit les textes ? Moi » alors qu'un assistant aide | Phrase en ligne | Vrai | Décision de l'utilisateur ; avis : « Moi, avec mes outils, à partir de notre échange » suffit |
| — | Prestige : « Rencontre. Chez vous » contre « partout en France à distance » | `prestige.html`, étape 1 | **Vrai** | Proposition 9 |

## 2. Gemini

| Affirmation | Vérification | Verdict |
|---|---|---|
| Page Charente inaccessible | 200, indexée (Search Console, 05/11) | **Faux** |
| Pas de données structurées d'entreprise locale | `Organization` + `ProfessionalService`, FAQ, offres | **Faux** |
| En-têtes de sécurité incomplets | 100/100, 6 en-têtes | **Faux** |
| Médiation et article L221-3 | Point réel | Avocat (question 1) |
| Pas de CGV en ligne | Vrai | Après l'avocat |
| Mention sous le formulaire du test du pouce ; « Rien n'est enregistré » | Vrai | Proposition 5 |
| Conseils : mettre en avant Visibilité, 2 sites offerts contre des avis, arrêter TikTok, YouTube et X, démo par SMS | « Contre des avis » : **refusé** (règle `67` : jamais d'avis en échange d'un avantage) ; démo par SMS : contraire à la règle « montrée en direct » ; arrêt de réseaux : décision de l'utilisateur après les chiffres du lundi | — |
| Pied de page « DIG 16 © » | Le texte réel est « DIG16 » (logo en deux morceaux collés, sans espace) | **Faux** |

## 3. Avant / après proposés (site : attend un « oui », après jeudi)

1. **Premier écran sur téléphone** : sous les boutons, ajouter une ligne « Dès 49 € par mois, 0 € de création » ; afficher la
   barre « Appeler / Démo gratuite » dès l'arrivée (aujourd'hui cachée tant qu'on n'a pas défilé).
2. **Propriété** : avant « Après les 6 premiers mois, vous partez quand vous voulez, avec votre site. » → après
   « Site et nom de domaine à votre nom dès le départ. Après les 6 premiers mois, vous pouvez partir quand vous voulez, et vous gardez tout. »
3. **`llms.txt`** : avant « Formules mensuelles : 6 mois d'engagement, puis sans engagement. » → après
   « Formules mensuelles : 6 mois d'engagement (12 mois pour Prestige et pour 12 mois payés d'avance), puis sans engagement. »
4. **Horaires dans les données structurées** : retirer le bloc « 00:00-23:59 tous les jours » (comme la fiche Google,
   sans horaires) ; « 7 j/7 joignable » reste dans le texte (décision du 24/10).
5. **Test du pouce** : avant « Rien n'est enregistré. » → après « L'adresse testée et son résultat ne sont pas enregistrés. »
6. **Facture** : avant « conforme aux obligations en vigueur (y compris la facturation électronique entre professionnels) »
   → après « conforme aux obligations en vigueur ».
7. **Rétractation** : avant « C'est une obligation légale pour les contrats signés chez vous, et je l'applique à tout le monde. »
   → après « Je l'applique à tous mes clients, par écrit sur le devis. » (texte définitif après l'avocat).
8. **« Le projet »** : citer les 4 formules (Essentiel, Visibilité, Achat, Prestige).
9. **Prestige, étape 1** : avant « Chez vous, pour sentir le lieu… » → après « Chez vous en Charente, en visio ailleurs en France, pour… ».

Chaque changement passe par `pages_markdown.py`, puis `test_pages.py` sans alerte, puis IndexNow.

## Complément : audit de ChatGPT (collé par l'utilisateur le 11/11 au soir, 37 constats)

Vérifié par Claude le 11/11 (site lu en direct, PagesJaunes et concurrents lus par Firecrawl).

| Constat de ChatGPT | Vérification | Suite |
|---|---|---|
| PagesJaunes : la présentation dit encore « en ligne en 7 jours » | **CONFIRMÉ** (fiche lue le 11/11, présentation mise à jour le 30/10) : promesse retirée partout ailleurs le 24/10 | À corriger par l'utilisateur dans Solocal Manager (texte fourni) |
| PagesJaunes : horaires « 24h/24 », adresse sans numéro | Confirmé, mais ce sont deux décisions de l'utilisateur (13/10 et 24/10) | Rien |
| Mentions légales : la liste des données reçues (nom, entreprise, téléphone ou email, message) oublie la commune et le site actuel, demandés par le formulaire | **CONFIRMÉ** (champs du formulaire : nom, entreprise, commune, contact, site, message) | Ajouté aux retouches « oui site » |
| Mentions légales : « Destinataires : DIG16 uniquement » puis « notre messagerie » non nommée et Cloudflare | Confirmé (formulation) | Avocat du 19/11 (avec le point « assistant IA ») |
| Téléphone de l'hébergeur absent, facturation électronique, rétractation (L. 221-3), CGV non publiées, premier écran sans prix ni appel | Déjà confirmés (Grok, audit du 11/11) ; nuance utile : l'article L. 441-1 du Code de commerce impose de communiquer les CGV au professionnel qui les demande, pas de les publier (à faire confirmer par l'avocat) | Retouches « oui site » et avocat |
| Démos : notes et avis d'exemple (« 4,9, 38 avis »), mention « fictif » seulement en bas | **À vérifier** (pages de démo non relues ce soir) | À contrôler avant les retouches du site |
| Concurrents : Munus 25 € par mois sans engagement, domaine compris ; VeryXL 30 € TTC par mois sans engagement | **CONFIRMÉ** pour ces deux-là (munus.fr et veryxl.fr lus le 11/11) ; ID16, C-Agence, SiteW, siteartisan.fr : non relus | Voir ci-dessous |
| Écrire le coût minimal (« 6 mois, soit 294 € ») sur le premier écran ; vendre Essentiel d'abord ; ouvrir l'appel sur un problème précis observé chez le prospect ; liste d'opposition | Conseils, pas des faits | Repris dans la proposition de fiche d'appels |

Enseignement pour l'offre (à ne pas trancher avant les premiers appels) : au moins deux offres nationales lues le 11/11 sont
moins chères que l'Essentiel (49 € par mois, 6 mois minimum, domaine en plus) et sans engagement. Ce qui distingue DIG16 et se
vérifie : interlocuteur local, démonstration de la vraie page d'accueil avant tout paiement, site et domaine au nom du client.

# Protection des données — site dig16.fr et outils DIG16

Vérifié le **04/11/2026** sur le site en ligne (dig16.fr) et dans les fichiers du dépôt (`site-dig/`).

Sources :
- CNIL, « Cookies : solutions pour les outils de mesure d'audience », page datée du 04/07/2025, lue le 04/11/2026 ;
- mentions légales en ligne, lues le 04/11/2026.

## 1. Ce qui est en place (FAIT ET VÉRIFIÉ)

| Point | Constat | Preuve |
|---|---|---|
| Mentions légales et politique de données | Six parties : éditeur, hébergeur, propriété intellectuelle, données personnelles, cookies, médiation | `site-dig/mentions-legales.html` |
| Base légale et durée de conservation | « mesures précontractuelles » (art. 6.1.b) ; prospects : 3 ans après le dernier échange ; clients : contrat puis durées comptables | mentions § 4 |
| Droits et réclamation à la CNIL | Cités, avec l'adresse de contact | mentions § 4 |
| Cookies | « aucun cookie publicitaire ni de mesure d'audience » (formule des mentions), donc pas de bandeau ; polices hébergées sur le site (aucun appel à Google) | mentions § 5, `_headers` |
| En-têtes de sécurité | HSTS, CSP, X-Frame-Options, nosniff, Referrer-Policy, Permissions-Policy | `outils/audit_securite.py` : 100/100 (04/11/2026) |
| Formulaire | Envoi chiffré (HTTPS) ; champ piège anti-spam `_honey` ; CSP qui n'autorise que formsubmit.co | `test_formulaire.py` : OK, aucun refus CSP (04/11/2026) |
| Adresse personnelle | Seule l'adresse légale de l'EI figure (déjà publique au registre) ; pas de nouvelle adresse publiée | mentions § 1 |
| Données de prospects | Jamais dans le dépôt public (scratchpad privé ou Drive « Dig ») | contrôles du 04/11 : aucun courriel personnel ni numéro de prospect dans le dépôt ; les numéros repérés étaient des identifiants de publications X |

## 2. Correction faite pendant l'audit (FAIT ET VÉRIFIÉ)

**CSP resserrée.** La politique de sécurité autorisait encore Cloudflare Web Analytics (`static.cloudflareinsights.com`
et `cloudflareinsights.com`). Or aucune balise Cloudflare n'est servie (page en ligne vérifiée le 04/11) et les mentions
légales ne citent que Metricool. Ces deux domaines ont été retirés de `site-dig/_headers` : moins de domaines autorisés,
c'est moins de surface d'attaque. Résultats :
- `test_pages.py` : « Toutes les pages sont propres » ;
- `test_formulaire.py` : OK ;
- retour arrière : annuler ce changement dans l'historique git (commit 65b3b6dba), ou rétablir les deux domaines dans la
  ligne CSP.

## 3. Écarts et risques (par ordre de priorité)

| # | Écart | Risque | Statut | Action proposée |
|---|---|---|---|---|
| 1 | **Mesure d'audience Metricool sans consentement.** L'exemption CNIL exige une finalité limitée à la mesure, « pour le compte exclusif de l'éditeur », des statistiques anonymes seulement, et aucune réutilisation par le fournisseur. Metricool est un outil de réseaux sociaux : rien ne prouve aujourd'hui qu'il remplit ces conditions (pas d'auto-évaluation CNIL trouvée). | Moyen | **Décidé le 04/11 : on garde Metricool pendant la vérification** (plan A3). DPA disponible chez Metricool ; manque un moyen de s'opposer au comptage (fiche CNIL n° 16) : à proposer | Demander à Metricool son auto-évaluation CNIL et ses conditions (DPA). Sinon, remplacer par un compteur sans tiers. Alternative gratuite sans aucune donnée transmise : un compteur de pages fait par une fonction Cloudflare Pages déjà présente (`functions/`), qui ne garde aucune adresse IP. **Décision de l'utilisateur** (il perd les statistiques Metricool du site). |
| 2 | **Transferts hors UE non décrits** : FormSubmit (Devro LABS, États-Unis) et Cloudflare (États-Unis) sont nommés, mais l'encadrement du transfert ne l'est pas (adhésion au Data Privacy Framework UE–États-Unis ou clauses types) | Moyen | **À FAIRE** (plan A4) | Vérifier sur dataprivacyframework.gov l'adhésion de Cloudflare et de Devro LABS (site non lisible depuis le conteneur le 04/11). Puis ajouter une phrase aux mentions, **seulement avec la preuve** (consigne : pas de modification juridique sans preuve). Si FormSubmit n'est pas couvert : alternatives UE gratuites à comparer (fonction Cloudflare Pages + courriel, ou un formulaire hébergé en UE). |
| 3 | **Liste des sous-traitants incomplète** pour les clients : Indy (factures), GoCardless (prélèvement), DocuSeal (signature), Google (Drive, Gmail) ne sont pas cités | Faible (aucun client à ce jour) | **RECOMMANDATION** | Ajouter un paragraphe « Clients » aux mentions et aux CGV au premier client, avec chaque sous-traitant, son pays et sa garantie, vérifiés le jour même. Le skill `nouveau-client` est le bon endroit. |
| 4 | **Registre des traitements absent.** Il n'est pas obligatoire pour une très petite structure si les traitements sont occasionnels, mais la CNIL recommande de le tenir. | Faible | **RECOMMANDATION** | Modèle CNIL simplifié à remplir au premier client : prospection, clients, contact du site. Fichier privé, Drive « Dig ». |
| 5 | **Contrats de sous-traitance (art. 28 RGPD)** : FormSubmit, Metricool, Cloudflare | Faible à moyen | **À FAIRE au premier client** (plan B4) | Télécharger le DPA de chaque prestataire et le ranger dans le Drive « Dig ». Aucun compte à créer, ce sont des pages publiques. |
| 6 | Le message de succès du formulaire propose encore « le test du pouce » | Faible (page outil maintenue, décision du 19/10) | **FAIT** (conforme aux consignes) | Rien |

## 4. Prospection

Le démarchage B2B par courriel suit le cadre CNIL déjà documenté (`35-demarchage-cadre-legal.md`) :
- professionnels seulement ;
- en rapport avec leur métier ;
- possibilité de s'opposer à chaque message ;
- pas de particuliers.

Rien de nouveau à signaler.

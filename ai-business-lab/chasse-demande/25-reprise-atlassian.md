# Reprise d'apps Atlassian abandonnées — dossier (24/09)

Décision de l'utilisateur (24/09) : « préparer la reprise, tout en continuant
à chercher ailleurs avec le radar ». Contexte : `24-atlassian-fin-connect.md`.

## Principe

Des éditeurs n'ont migré **aucune** app vers Forge alors que Connect n'est
plus supporté après le **31/01/2027**. Leurs clients payants vont perdre
l'app. Proposition : l'éditeur nous **transfère ses fiches** (procédure
officielle : ticket « Transfer your app to another Marketplace Partner »,
approuvé par l'administrateur de l'éditeur d'origine — developer.atlassian.com,
« Transfer apps between Atlassian Marketplace Partners »), nous portons le code
sur Forge, les clients restent servis, et l'éditeur touche une part des
revenus **sans rien faire**. Commission Atlassian sur Forge : 0 % jusqu'à
1 M$ de revenus cumulés.

## Cibles retenues (visionneuses : les plus simples à porter)

| Éditeur | Apps figées (installations) | Contact public |
|---|---|---|
| **Toshihiro Sato** (vendeur 1215814, individuel) | Open API (Swagger) Integration 2 897 ; Mermaid Integration 591 ; Flowchart & PlantUML 544 ; Figma Viewer ; JSON Viewer ; OpenAPI pour Jira ; CSS ; Page Redirect — 10 apps, **aucune migrée** | portail d'assistance `toshihiro.atlassian.net/servicedesk/customer/portal/1` |
| **Tech Labs** (vendeur 1216949) | Swagger UI for Confluence 659 ; Mermaid for Confluence 791 ; Figma File Integration ; HTML Content Macro — 4 apps, **aucune migrée** | portail d'assistance `technologylabs.atlassian.net/servicedesk/customer/portal/3` |

(Le 3e éditeur envisagé — Open API Editor, Q&A, JSON Viewer, 15 apps — a été
identifié : **EliteSoft**, voir cibles de second rang ci-dessous.)

## Proposition (partage de revenu, sans achat)

- Transfert des fiches cloud et du code existant.
- Portage sur Forge par nous, avant le 31/01/2027 ; nous assurons ensuite
  maintenance et support.
- **L'éditeur d'origine reçoit 30 % du revenu net de ces apps pendant
  24 mois**, puis rien. Aucun paiement de notre part au départ (budget 0 €).
- Si l'éditeur préfère migrer lui-même : pas de problème, nous nous retirons.

## Message à envoyer (anglais, via le portail d'assistance de chaque éditeur)

> **Subject: Your Confluence apps and the Connect end of support (31 Jan 2027)**
>
> Hello,
>
> I noticed that your cloud apps ([nom des apps]) are still on Connect and
> have not had an update since Atlassian froze Connect releases on 31 March
> 2026. With Connect end of support on 31 January 2027, your customers may
> lose these apps.
>
> If migrating to Forge is not in your plans, I would like to offer to take
> them over: you transfer the listings through Atlassian's standard app
> transfer process, I port them to Forge before the deadline and handle
> support and maintenance from then on. Your customers keep a working app.
>
> In return, you would receive 30% of the net revenue of these apps for
> 24 months, with no work on your side. If you do plan to migrate them
> yourself, no problem at all — just let me know and I will not pursue this.
>
> Would you be open to a short exchange about it?
>
> Best regards,
> [nom commercial]

## Ce que l'utilisateur devra faire (et seulement si un éditeur répond oui)

1. Aujourd'hui : **aucune démarche administrative**. Envoyer les deux
   messages depuis un compte Atlassian (le portail d'assistance l'exige),
   sous un nom commercial.
2. Si un éditeur accepte : créer une **micro-entreprise** (gratuit, en ligne),
   passer la vérification partenaire Atlassian, prendre un nom de domaine
   (~10 €/an) pour l'adresse email exigée par le portail partenaire.
3. Claude : portage Forge, tests, fiche, support documenté.

## Risques (grille)

- Point 5 ✓ (clients payants déjà là) ; 8 ✓ pour Swagger (pas d'alternative
  migrée bien notée) ; 18 ✓ (4 mois avant la date).
- Point 20 : support de ~5 000 installations — surtout des visionneuses,
  peu de tickets attendus, mais à mesurer (historique d'avis).
- Point 21 : l'éditeur doit faire confiance à un inconnu — d'où le partage
  de revenu et la porte de sortie proposée.
- Point 25 (destruction) : **les éditeurs ne répondent pas**, ou migrent
  eux-mêmes au dernier moment. Coût d'un échec : deux messages.

## Cibles de second rang (éditeurs sans AUCUNE app migrée, relevé du 24/09 18:40 UTC)

| Éditeur | Apps figées (installations) | Contact public | Remarque |
|---|---|---|---|
| **EliteSoft** | Open API (Swagger) Editor 615 ; Questions & Answers 657 ; JSON Viewer & Editor 450 (15 apps) | `elitesoftware.atlassian.net/servicedesk/customer/portal/10` | visionneuses/éditeurs simples → **3e cible naturelle** |
| Colined | Pivot Report 914 ; Worklogs Report 392 | `colined.atlassian.net/servicedesk/customer/portal/1` | rapports Jira, alternatives nombreuses |
| Sourcesprout | Simple PDF Export for Jira 202 | portail Sourcesprout | petit |
| Bilith (4 comptes) | Google Drive & Docs 4 132 ; OneDrive & SharePoint 1 496 ; Asana 1 081 ; Box 253 | portail Bilith | **gros volume**, mais connecteurs OAuth Google/Microsoft lourds ; vérifier d'abord si Bilith a publié des versions Forge sous un autre compte |
| WISOFT | Slack Connector 1 379 ; Gantt Cloud 924 | wisoft.zendesk.com | Slack : 4 alternatives migrées bien notées |
| Addteq | Excellentable 1 312 | portail Addteq | tableurs : 40 alternatives |
| Magic Apps | Magic Estimations 1 443 | portail Magic Apps | planning poker : 9 alternatives |

Priorité d'envoi : Toshihiro Sato → Tech Labs → EliteSoft (les trois ont des
visionneuses Swagger/Mermaid/JSON, portage simple, peu d'alternatives).

## Journal des envois

| Date | Éditeur | Canal | Statut |
|---|---|---|---|
| 24/09/2026 | Toshihiro Sato | portail d'assistance, « Other questions » | **envoyé** par l'utilisateur ; réponse attendue sur l'email du pseudonyme |
| 24/09/2026 | Tech Labs | portail d'assistance | **envoyé** par l'utilisateur ; réponse attendue sur l'email du pseudonyme |
| 24/09/2026 | EliteSoft | portail d'assistance (portal/10) | **envoyé** par l'utilisateur ; réponse attendue sur l'email du pseudonyme |

## Calendrier et plan B (24/09, soir)

- **Délai de réponse accordé : jusqu'au 08/10/2026** (2 semaines). Pas de
  relance multiple : une seule relance polie le 08/10 si silence.
- **Plan B si aucun éditeur n'accepte** : publier notre propre visionneuse
  OpenAPI/Swagger sur Forge (le seul trou sans alternative migrée bien notée,
  voir `24-atlassian-fin-connect.md`). Moins bon que la reprise (les clients
  devront nous trouver), mais daté : les ~5 400 installations figées devront
  changer d'outil avant le 31/01/2027. À repasser dans la grille avant de
  coder : les éditeurs actifs (Stepashka) et les concurrents migrés peuvent
  capter ces clients avant nous.
- **Portage technique** (reprise ou plan B) : macro Confluence Forge (UI
  Kit ou Custom UI) qui affiche une spécification OpenAPI collée ou
  jointe ; pas de serveur externe (hébergement Atlassian, 0 €) ; modules
  récents uniquement (les modules `jira:dashboardGadget` disparaissent le
  17/05/2027). Aucun code écrit tant qu'aucun éditeur n'a répondu ou que le
  plan B n'est pas décidé (règle n° 1).

# Radar des fermetures + fin de couverture des boutiques (24/09, soir)

## Couverture des boutiques

Mesurées : Shopify, BigCommerce, WordPress, Atlassian, Apify, Wix, Google
Workspace, HubSpot, Chrome, Zoom (3 851), Salesforce AppExchange (5 976),
monday.com (1 258). Non mesurables : PrestaShop Addons et Figma
(**protection anti-robots, respectée — pas de contournement**), Microsoft
AppSource (page d'erreur), Squarespace (petite sélection sans notes), Zapier
et Slack (aucune note publique). **Couverture considérée complète.**

## Radar des fermetures (nouvel outil)

`outils/radar_fermetures.py` lit les journaux officiels des développeurs
(Shopify, HubSpot, Xero, Intuit, Zoom, Slack, Meta, Google Workspace, Square,
Stripe, eBay) et garde les phrases annonçant un retrait daté. Premier relevé :
`radar-2026-09-24.md` (26 annonces). À relancer chaque semaine.

Annonces à suivre (source primaire : journaux officiels) :

| Plateforme | Retrait | Date | Qui est touché |
|---|---|---|---|
| Xero | API Xero Practice Manager v3.0 | février 2027 | éditeurs d'intégrations pour cabinets comptables |
| Xero | portées larges de l'API comptable | 6 mai 2027 | toutes les apps connectées à Xero |
| Xero | fonctions « prospects, fournisseurs, bons de commande » de Practice Manager | retirées le 10/08/2026 | cabinets comptables (fonction « peu utilisée ») |
| HubSpot | API Pipelines v1 | 4 décembre 2026 | intégrations anciennes |
| Shopify | `scriptTagCreate` / `scriptTagUpdate` | 1er octobre 2026 | apps qui injectent des scripts |
| Slack | vue « assistant » | février 2027 | apps d'assistant |

Lecture : ces retraits touchent surtout des **développeurs**, qui migrent
eux-mêmes. L'occasion de type Invoice Stack apparaît quand un retrait
supprime une **fonction utilisée par des clients non techniques** sans
remplaçant officiel. Aucune de ces annonces ne le fait clairement aujourd'hui ;
le radar sert à la repérer dès qu'elle paraît.

## Relevé du 24/09 au soir (`radar-2026-09-24-soir.md`)

Nouveautés par rapport au relevé du matin :
- **Forge : modules `jira:dashboardGadget` et `jira:dashboardBackgroundScript`
  retirés le 17/05/2027** (remplacés par `dashboards:widget`). Conséquence
  pratique : tout portage Forge doit utiliser les nouveaux modules. Ce n'est
  pas une opportunité : les éditeurs actifs migreront eux-mêmes.
- **Azure AI Content Moderator retiré le 31/03/2027** : Microsoft fournit
  son propre remplaçant (Azure AI Content Safety) → absorption (point 14),
  écarté.
- Une date « 17/05/2027, complete your migration » sans produit identifiable
  dans la ligne : à relire à la source au prochain relevé avant toute
  conclusion.

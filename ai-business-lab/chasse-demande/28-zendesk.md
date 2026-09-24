# Zendesk : quatre fermetures datées — mesure (24/09, soir)

Trouvées par le radar élargi (11 nouvelles sources ajoutées ce soir :
Zendesk, Miro, Pipedrive, monday.com, Webflow, Asana, Trello, Intercom,
GitHub, Dropbox, Calendly). Source primaire commune : journal des
développeurs Zendesk (developer.zendesk.com/api-reference/changelog/changelog/).

| Fermeture | Date | Lecture | Verdict |
|---|---|---|---|
| Apps « Built-by-Zendesk » (Print Ticket History, Project Management, Sidebar Search, Assignment Control, iFrame, Attachment Manager, Proactive Tickets) | inutilisables le 21/10/2026 | Zendesk : « capabilities incorporated into Agent Workspace » et « low usage » ; remplaçants natifs listés (support.zendesk.com, 07/04/2026) | écarté (absorption, point 14) |
| **Zendesk Sell** (CRM commercial) | retiré le **31/08/2027** ; données supprimées | Annoncé le 09/09/2025. Zendesk a **signé avec Pipedrive** (outils de migration fournis) ; Salesforce, Zoho, ClonePartner, Sanka publient déjà des guides de migration | écarté (points 8 et 14 : canal pris par un partenaire officiel, un an d'avance) |
| Thèmes Help Center, Templating API v1-v3 | import bloqué 01/03/2027 ; **mise à niveau automatique vers v4 le 03/08/2027** | Zendesk migre lui-même les thèmes restants | écarté (absorption) |
| **Jetons d'API (API tokens)** | désactivés le **30/04/2027** | Toute app ou script qui s'authentifie par jeton cessera de fonctionner | mesuré ci-dessous |

## Mesure « jetons d'API » (catalogue public)

L'adresse `marketplace.zendesk.com/api/v2/apps.json` (publique, JSON) donne
les 1 745 apps publiées : installations, prix, note, paramètres demandés,
instructions d'installation.

- Apps dont les instructions demandent un **jeton d'API Zendesk** : **71**,
  soit **3 234 installations au total** ; presque toutes gratuites (plus
  grosse : GIPHY, 1 218 installations).
- Les apps payantes concernées ont de 6 à 35 installations chacune.

**Verdict : écarté** (point 4 : taille). Les scripts « maison » des
entreprises qui utilisent des jetons ne sont pas mesurables de l'extérieur,
et y répondre demanderait du démarchage (interdit).

Note : ce catalogue public (474 apps payantes, installations, notes) peut
servir à une analyse de trous du même type que Shopify/Atlassian ; la
méthode a montré jusqu'ici qu'un marché mûr n'a pas de niche vide
(`19-synthese-24-09.md`).

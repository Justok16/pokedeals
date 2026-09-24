# Atlassian : fin de Connect le 31/01/2027 — la fenêtre « Invoice Stack » à venir

Repérée par le radar (`radar-2026-09-24.md`) puis vérifiée.

## Faits

- **Connect, l'ancienne plateforme d'apps Jira/Confluence, n'est plus
  supporté après le 31 janvier 2027** ; les apps Connect « peuvent cesser de
  fonctionner » (atlassian.com, blog officiel « Announcing Connect End of
  Support » ; secondaire concordant : forge-apps.com). Depuis le
  **31/03/2026**, une app Connect ne peut plus publier de mise à jour.
- Atlassian affirme que **plus de 95 % des postes payants** ont migré.
- Retrait séparé : modules Forge `jira:dashboardGadget` supprimés le
  **17/05/2027** (journal des développeurs Atlassian).

## Mesure (source primaire : API publique de la boutique, dernière version cloud de chaque app ≥ 200 installations)

`outils/atlassian_connect.py` : 1 177 apps examinées, 1 021 lues.

- **188 apps cloud encore déclarées « Connect »**, 270 795 installations
  cumulées ; 109 gratuites, **78 payantes (47 830 installations)**, dont
  **51 sans version depuis octobre 2025**.
- Exemples payants sans mise à jour récente : Open API (Swagger) Integration
  (2 897 inst., 2024-09) ; Magic Estimations (1 443) ; Status Time Reports
  (1 331, 4,79) ; Slack Connector for Jira (1 165, **2021**) ; Manage Users
  for Jira Cloud (931) ; Gantt Cloud (924, **2021**) ; Restore Deleted Issues
  (922) ; Outlook Connector for Jira (736) ; CRM for Jira (646, 102 avis) ;
  Gantt-Chart for Jira (483, **2022**, 129 avis).
- Gratuites très installées et figées : Microsoft Teams for Jira DC (2021),
  Google Chat for Jira (2021), Render Markdown (2021), Harvest (2021), Todoist
  (2020), Zoom Notifications (2019).

## Pourquoi c'est la piste la plus prometteuse depuis le début

C'est exactement le schéma qui a enrichi Invoice Stack : **une fermeture
datée, des clients qui PAIENT déjà (point 5 ✓), et des éditeurs qui ne
migreront pas**. Leurs clients devront trouver un remplaçant avant le
31/01/2027 — dans 4 mois : fenêtre ouverte, pas encore passée (point 18 ✓).
Distribution : la boutique Atlassian elle-même (point 10 ✓).

## Hypothèses à vérifier AVANT toute construction (règle n° 1)

1. **Le drapeau `connect` signifie-t-il « pas migré » ?** Une app hybride
   « Connect sur Forge » pourrait le garder. À trancher dans la documentation
   officielle d'Atlassian — tant que ce n'est pas fait, les chiffres ci-dessus
   sont des **majorants**.
2. Pour les 10 premières payantes : l'éditeur a-t-il annoncé une migration,
   une fin de vie ou une nouvelle fiche Forge ?
3. Pour chacune : les alternatives Forge déjà présentes (nombre, notes).
4. Conditions éditeur Atlassian (partage de revenu, validation Forge,
   identité).
5. Variante à étudier : **reprendre** une app abandonnée (transfert de fiche
   autorisé par la boutique) plutôt que la recréer.

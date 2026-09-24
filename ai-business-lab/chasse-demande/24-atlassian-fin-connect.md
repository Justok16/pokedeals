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

## Vérifications faites le 24/09 au soir

**Hypothèse 1 — tranchée empiriquement** : aucune des 188 apps « Connect »
n'a de version postérieure au 31/03/2026 (date du gel), alors que 742 des 833
apps migrées en ont publié une. Le drapeau désigne bien des apps **figées,
non migrées**.

**Hypothèse 3 — alternatives migrées bien notées (≥ 4★, ≥ 10 avis)** pour
les apps payantes figées : planning poker 9, temps par statut 9, Gantt 12,
Slack 4, gestion d'utilisateurs 4, Outlook 3, CRM 5, Mermaid 2 — **déjà
couverts**. Deux trous : **Swagger / OpenAPI** et **restauration de tickets
supprimés** (0 alternative migrée bien notée).

### Le cas Swagger / OpenAPI (documentation d'API dans Confluence et Jira)

- Apps payantes figées : Open API (Swagger) Integration 2 897 installations
  (4,4) ; Visualize OpenAPI 1 213 (4,35) ; Swagger UI for Confluence 659
  (4,53) ; Open API Editor 615 (4,58) — **≈ 5 400 installations payantes qui
  cesseront peut-être de fonctionner après le 31/01/2027**.
- Alternatives migrées : « PlantUML, Swagger, drawio… » 3,96 (3 221, payant) ;
  Open API Documentation for Confluence 3,68 (1 829, payant) ; OpenAPI
  (Swagger) for Confluence (gratuit, 5,0 sur 3 avis, 380) ; ZenUML Lite
  (gratuit) ; Swagger UI+ Embed (payant, 0 avis). Concurrence présente mais
  moyenne.
- **Prix constatés** (API officielle de tarification) : les apps figées
  coûtent ~**1 $ par utilisateur et par an** (10 utilisateurs : 10 $/an ;
  100 : 100 $/an ; 300 : ~200 $/an). Le concurrent migré le plus installé est
  plus cher (100 utilisateurs : 250 $/an).
- **Chiffrage honnête** : ~5 400 installations × quelques dollars par mois ≈
  un marché total de l'ordre de **10 à 20 000 $/mois** pour les apps figées ;
  en capter 20 % donnerait **~2 000 à 4 000 $/mois**. Réel, daté, faisable
  techniquement (afficher une spécification OpenAPI dans une macro Forge),
  mais **pas un projet en or**.

**Statut** : meilleure piste concrète et datée à ce jour ; à compléter par
les points 2, 4 et 5 avant toute décision.

## Point 4 — conditions éditeur (vérifié le 24/09)

- **Commission Atlassian sur les apps Forge : 0 % jusqu'à 1 M$ de revenus
  cumulés** (depuis le 01/01/2026), puis 17 % ; Connect : 25 % depuis le
  01/07/2026 (atlassian.com, « Updates to Marketplace Revenue Share: 2026 »,
  source primaire). Hébergement Forge fourni par Atlassian.
- **Identité** : vérification « Partner Verification » obligatoire avant de
  publier. Témoignages contradictoires sur le forum officiel des développeurs
  (community.developer.atlassian.com) : réponse relayée « entité enregistrée
  requise » ; mais un **travailleur indépendant (Portugal) validé en
  août 2026** pour une app payante. Équivalent français : **micro-entreprise**
  (création gratuite en ligne). Conforme à la décision de l'utilisateur du
  23/09 : identité donnée aux organismes qui paient, jamais sur le site.
- **Profil public** : au nom de la personne ou de l'entreprise — à vérifier
  si un nom commercial suffit (anonymat public).
- **Adresse email à nom de domaine privé** exigée pour l'accès au portail
  partenaire (pas de Gmail) : ~10 €/an de domaine, cohérent avec le budget
  accepté le 23/09 (« dès le premier euro » — ici avant : décision à
  demander le moment venu).

# 09 — Outils et budget

## Principe

Budget de départ : **0 €**. Aucun outil payant n'est recommandé tant qu'il n'y a
pas de revenu, et même après, seulement si la version gratuite bloque réellement
quelque chose de mesurable.

Avant toute recommandation d'abonnement, cinq questions doivent être répondues :
**prix**, **ce qu'il apporte**, **pourquoi il est nécessaire**, **l'alternative
gratuite**, **à quel moment il devient pertinent**.

## Phase 1 — Stack à 0 €/mois

| Besoin | Outil | Pourquoi celui-là | Limite à surveiller |
|---|---|---|---|
| Automatisation/cron | **GitHub Actions** | Déjà en production ici, ~20 workflows, sans serveur | Quotas de minutes sur dépôt privé |
| Données/scraping | **Moteur PokéDeals existant** | Déjà écrit, testé, avec coupe-circuits | Dépend de la stabilité des sites scannés |
| Base de données | **Fichiers JSON versionnés + Supabase (offre gratuite)** | Déjà en place, coût nul | Limites de l'offre gratuite Supabase |
| Newsletter | **beehiiv** | Gratuit jusqu'à **2 500 abonnés**, **0 %** de commission sur les abonnements payants, réseau publicitaire intégré | Abonnements payants = plan supérieur |
| Site/comparateur | **Pages statiques + hébergement gratuit** | Zéro coût, zéro maintenance, très rapide | Pas de rendu dynamique |
| Rédaction/scripts | **ChatGPT (déjà payé)** | Aucun coût supplémentaire | Ne jamais lui faire inventer un chiffre |
| Voix IA | **Voix de synthèse des outils de montage** | Gratuit, suffisant pour tester | Qualité moyenne |
| Montage court | **CapCut ou équivalent gratuit** | Suffisant pour le format testé | Watermark selon les options |
| Mesure | **Search Console + statistiques natives + tableau CSV** | Gratuit et suffisant à ce stade | Saisie partiellement manuelle au début |
| Notifications | **Telegram (déjà branché)** | Déjà en production | — |

**Alternative newsletter** : **Kit** (gratuit jusqu'à 10 000 abonnés, vente de
produits intégrée) devient meilleur si la liste dépasse 2 500 abonnés avant
toute monétisation. **Substack** est à éviter à terme : gratuit sans limite,
mais **10 % de commission à vie** sur les abonnements payants — c'est le revenu
récurrent, précisément ce qu'on cherche à construire, qui serait taxé.

## Phase 2 — Premiers réinvestissements (seulement après revenu)

| Dépense | Prix indicatif | Quand elle devient justifiée | Alternative gratuite d'ici là |
|---|---|---|---|
| Nom de domaine | ~10 €/an | Dès que le comparateur reçoit du trafic organique | Sous-domaine d'hébergement gratuit |
| beehiiv payant | selon palier | À 2 500 abonnés **ou** au lancement de l'offre premium | Kit gratuit jusqu'à 10 000 |
| Outil de montage payant | ~10-20 €/mois | Si le montage dépasse 1 h/jour et que le format est **déjà validé** | Outils gratuits |
| Voix IA premium | ~5-20 €/mois | Si la voix est identifiée comme cause mesurée de faible rétention | Voix intégrées |
| Stripe | ~1,5 % + 0,25 €/transaction | Dès la première vente | — (indispensable) |
| Micro-entreprise | ~0 € à la création, cotisations sur le CA | **Dès le premier revenu régulier** | Aucune : obligation légale |

## Phase 3 — Automatisation avancée

À n'engager que si l'équation est vérifiée : **heures économisées × valeur de
l'heure > coût de l'outil**, sur au moins 3 mois de recul.

## Comparatif des choix structurants

### Newsletter

| Critère | beehiiv | Kit | Substack |
|---|---|---|---|
| Gratuit jusqu'à | 2 500 abonnés | 10 000 abonnés | illimité |
| Commission sur abonnements | **0 %** | 0 % | **10 %** |
| Vente de produits | limitée | **intégrée** | intégrée |
| Publicité intégrée | **oui** | non | non |
| Risque de dépendance | moyen (export possible) | moyen | **élevé** (audience liée à la plateforme) |
| **Verdict** | **Choix phase 1** | Bascule si > 2 500 sans revenu | À éviter à terme |

### Où héberger la donnée

| Option | Coût | Avantage | Inconvénient |
|---|---|---|---|
| JSON versionnés (actuel) | 0 € | Simple, déjà en place, historisé par git | Ne tient pas à grande échelle |
| Supabase (gratuit) | 0 € | Déjà branché, requêtable | Limites de l'offre gratuite |
| Base payante | > 20 €/mois | Performance | **Injustifié aujourd'hui** |

## Ce qu'il ne faut pas acheter

- Aucune **formation** sur le contenu IA / business en ligne : tout ce qui est
  nécessaire est dans ce dossier et dans les sources citées.
- Aucun **outil de publication multi-plateforme** payant avant d'avoir prouvé
  qu'un format fonctionne — publier plus vite un contenu qui ne marche pas ne
  sert à rien.
- Aucun **outil d'analyse de tendances** payant : le Niche Radar utilise des
  sources gratuites, et la meilleure source de tendance du projet est sa propre
  donnée.
- Aucun **nom de domaine acheté « pour réserver »** sur des concepts non testés.

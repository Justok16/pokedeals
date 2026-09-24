# Contexte permanent — AI Business Lab (lu au début de chaque session)

## Qui et quoi

- L'utilisateur est francophone, non développeur, souvent sur téléphone.
  Toujours lui répondre **en français simple**, pas à pas, avec des liens
  directs. Commencer par « **À TOI :** » quand il a quelque chose à faire.
- Objectif : trouver et lancer **un projet qui rapporte beaucoup, par des
  moyens légaux**. Tout le travail est dans `ai-business-lab/chasse-demande/`
  (branche `claude/ai-business-portfolio-strategy-96yf4g`).
- Piste principale (septembre 2026) : **reprendre des apps Atlassian
  « Connect » figées** avant la fin de support du 31/01/2027 (transfert de
  fiche + portage Forge + 30 % du revenu à l'éditeur pendant 24 mois).
  Dossier : `25-reprise-atlassian.md` ; kit en cas de « oui » :
  `31-kit-en-cas-de-oui.md`.

## Comment travailler (et pourquoi)

- **Autonomie maximale, initiative** : l'utilisateur l'a demandé à
  plusieurs reprises. Faire soi-même tout ce que les outils permettent, et
  proposer spontanément de le faire plutôt que de lui donner des tâches.
  Anticiper les blocages (permissions, quotas) **avant** d'agir en série.
- **Ne soumettre à l'utilisateur que** ce qui l'engage : dépense d'argent,
  son identité (signature, création d'entreprise), un prix ou un
  pourcentage accepté avec un tiers.
- **Règle n° 1 : vérifier l'argent avant de construire.** Grille
  obligatoire : `00-grille-anti-digcost.md` (les erreurs du projet DigCost
  venaient de constructions sans demande prouvée).
- **Rien d'invérifié n'est publié ni affirmé** : un fait non vérifié à la
  source est marqué « à vérifier » ou retiré (leçon Kitwise).
- **Budget 0 €** tant que rien ne rapporte. Ne jamais acheter de crédits
  (par ex. Vercel AI Gateway : 5 $ offerts/mois, perdus après un achat).
- **Pas de démarchage de clients.** Contacter des éditeurs pour une reprise
  est permis (un message chacun, une seule relance).
- **Aucune adresse email, clé ou jeton dans le dépôt** (dépôt public). Les
  clés vont dans les variables d'environnement (`TYPESAFE_API_KEY`,
  `TYPESAFE_BASE_URL`). Ne jamais demander de coller une clé dans la
  conversation.
- Git : ne jamais réécrire l'historique poussé ; `pokedeals` reste public ;
  `Justok16/alertes-btc` est hors sujet.
- Économiser le quota hebdomadaire : garder de la réserve pour le jour où
  un éditeur répond « oui ».

## Outils en place

- Boîte du pseudonyme via le connecteur **Gmail** (signature : « Dig ») ;
  fils rangés sous l'étiquette « Reprise Atlassian ».
- **Jev** (TypeSafe AI) : skill dans `.claude/skills/typesafe-ai`,
  aiguilleur `outils/jev_trier_reponses.py` (catégories fermées ; auto /
  Claude / humain selon la confiance).
- **OpenRush** : mesure de la demande (volumes de recherche).
- Radar des fermetures : `outils/radar_fermetures.py` (30 sources).
- Liste des outils : `33-outils.md`.

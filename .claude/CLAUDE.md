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
- **Creuser avant de conclure** (demande du 25/09) : ne jamais répondre
  « impossible » ni confier une tâche à l'utilisateur avant d'avoir épuisé
  les voies possibles — connecteurs disponibles (Vercel, GitHub, Gmail…),
  déploiement d'un petit programme, jeton OIDC, services alternatifs,
  documentation officielle. Exemple : les vidéos et Jev semblaient exiger
  une clé ; un relais Vercel sans clé a suffi. Si un blocage reste réel,
  dire précisément lequel et ce qui a été essayé.
- **Ne soumettre à l'utilisateur que** ce qui l'engage : dépense d'argent,
  son identité (signature, création d'entreprise), un prix ou un
  pourcentage accepté avec un tiers.
- **Règle n° 1 : vérifier l'argent avant de construire.** Grille
  obligatoire : `00-grille-anti-digcost.md` (les erreurs du projet DigCost
  venaient de constructions sans demande prouvée).
- **Rien d'invérifié n'est publié ni affirmé** : un fait non vérifié à la
  source est marqué « à vérifier » ou retiré (leçon Kitwise).
- **Chiffres** : uniquement tirés de la page officielle **datée**, lue
  directement (jamais d'un résumé de moteur de recherche), avec la citation
  exacte et la date. Leçon du 25/09 : aide Agefiph annoncée à 6 300 € (article
  de 2022) au lieu de 3 000 € ; taux de l'Adie (8,4 %) oublié.
- **Budget 0 €** tant que rien ne rapporte. Ne jamais acheter de crédits
  (par ex. Vercel AI Gateway : 5 $ offerts/mois, perdus après un achat).
- **Démarchage B2B par email autorisé** (révision du 24/09) dans le cadre
  légal CNIL : ciblé, en rapport avec l'activité du destinataire,
  expéditeur identifiable, désinscription simple. Pas de particuliers.
- **Tous les domaines légaux sont ouverts** ; identité : pseudonyme « Dig »
  seulement. Détails : fin de `00-grille-anti-digcost.md`.
- **Aucune adresse email, clé ou jeton dans le dépôt** (dépôt public). Les
  clés vont dans les variables d'environnement (`TYPESAFE_API_KEY`,
  `TYPESAFE_BASE_URL`). Ne jamais demander de coller une clé dans la
  conversation.
- Git : ne jamais réécrire l'historique poussé ; `pokedeals` reste public ;
  `Justok16/alertes-btc` est hors sujet.
- **Si création d'entreprise** : tout doit être juridiquement parfait et
  la fiscalité optimisée (demande forte de l'utilisateur, 25/09). Suivre la
  section 2 bis de `31-kit-en-cas-de-oui.md` ; nom commercial « Dig » validé.
  Chercher **toutes** les aides, financières et en nature (`36-aides-creation.md`).
  Situation sociale personnelle : ne jamais l'écrire dans le dépôt public.
- **Tout enregistrer** (demande du 26/09) : chaque document, démo, visuel ou
  prompt créé est sauvegardé. Public (sans données personnelles ni région de
  l'utilisateur) → ce dépôt. Privé (listes de prospects, données clients,
  région) → dossier « Dig » du Google Drive de l'utilisateur, jamais ici.
- **PDF toujours à jour** (demande du 26/09) : à chaque modification d'une
  liste ou d'un document déjà remis (prospect retiré, vérifié, ajouté…),
  régénérer le PDF correspondant et le renvoyer à l'utilisateur, en gardant
  les mêmes numéros de prospects.
- **Documents irréprochables, fond ET forme** (exigence ferme du 26/09,
  répétée plusieurs fois) : AUCUN document, visuel, démo ou PDF n'est
  envoyé avant le contrôle complet de `ai-business-lab/chasse-demande/44-controle-qualite.md`
  (mesures au pixel, alignements, chevauchements, liens et QR testés,
  cohérence des chiffres entre documents, orthographe, rendu téléphone
  et ordinateur). Ne jamais envoyer une version « à moitié finie ».
- Économiser le quota hebdomadaire : garder de la réserve pour le jour où
  un éditeur répond « oui ».

## Rappels promis à l'utilisateur

- **Paiement client : FAIT le 27/09.** Antisèche n° 12 : franchise en base
  (« TVA non applicable, article 293 B du CGI », vérifié sur Service Public) ;
  n° 15 : prélèvement automatique mensuel (choix de l'utilisateur, cohérent
  avec le site et le plan). Si le statut choisi à la création sort de la
  franchise, revoir la n° 12 et renvoyer le PDF.

## Outils en place

- Boîte du pseudonyme via le connecteur **Gmail** (signature : « Dig ») ;
  fils rangés sous l'étiquette « Reprise Atlassian ». **Archiver chaque
  fil après traitement** (demande du 25/09) : étiquette + retrait de la
  boîte de réception et du « non lu » ; ne jamais supprimer ; ne laisser
  en boîte de réception que ce qui attend une décision de l'utilisateur.
- Démarchage B2B : pas de campagne en série sous le seul pseudonyme (voir
  `35-demarchage-cadre-legal.md`).
- **Jev** (TypeSafe AI) : skill dans `.claude/skills/typesafe-ai`,
  aiguilleur `outils/jev_trier_reponses.py` (catégories fermées ; auto /
  Claude / humain selon la confiance).
- **OpenRush** : mesure de la demande (volumes de recherche).
- Radar des fermetures : `outils/radar_fermetures.py` (30 sources).
- Liste des outils : `33-outils.md`.
- **Base de connaissances vidéo** (demande du 26/09) : résumés Gemini des
  vidéos YouTube dans `connaissances/` (chaîne Finary : finances
  personnelles, 965 vidéos, traitées avec `outils/resumer_chaine.py` qui
  alterne 7 modèles Gemini gratuits : ~20 vidéos/jour/modèle, soit ~1 semaine). À consulter avant de répondre sur ces sujets ;
  toute règle fiscale ou chiffre qui en est tiré est revérifié à la source
  officielle avant d'être affirmé.

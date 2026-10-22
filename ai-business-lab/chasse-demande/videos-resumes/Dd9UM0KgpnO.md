Reel Instagram Dd9UM0KgpnO (danyltn, 48 s, résumé le 18/10/2026)
« Cet agent IA meurt s'il ne gagne pas d'argent » : expérience d'un développeur de 20 ans (projet non nommé dans la vidéo, ressources envoyées seulement en message privé) : un agent IA reçoit un portefeuille crypto, paie chaque action (réflexion, serveur, emails), doit vendre seul des services (sites, logos) pour survivre, et finance de nouveaux agents s'il est rentable.

| Élément | Pour DIG16 |
|---|---|
| Agent autonome avec portefeuille crypto, qui vend et démarche seul | 📦 **Réserve « veille d'idées », non applicable** : budget 0 € ; démarchage sans humain contraire à notre cadre (`35-demarchage-cadre-legal.md` : expéditeur identifiable, envois ciblés, pas de campagne en série) ; aucun outil nommé ni vérifiable. À ressortir seulement si un projet publié et vérifié propose un agent avec plafond de dépense et validation humaine |
| Leçon « coût de chaque action IA face à la marge » | ✅ Déjà appliquée : DIG16 tourne sur des outils gratuits (relais Vercel, Gemini gratuit, Cloudflare gratuit) ; coût IA par client = 0 € aujourd'hui. À recalculer si un outil payant est un jour ajouté |

## Projet identifié le 18/10 (lien envoyé par l'utilisateur) : Conway-Research/automaton

README lu le 18/10/2026 sur GitHub (https://github.com/Conway-Research/automaton) : licence MIT ; agent « souverain » en boucle continue (penser, agir, observer) qui crée au démarrage un portefeuille Ethereum, paie son calcul en cryptomonnaie stable sur Conway Cloud (service payant), a accès à un serveur Linux, au shell, aux noms de domaine et aux transactions, **modifie son propre code** et **se reproduit** (crée et finance des agents enfants). Une « constitution » de 3 lois (ne pas nuire, ne pas spammer, ne pas tromper) est intégrée. Installation proposée par `curl … | sh`.

| Pour DIG16 | Décision |
|---|---|
| Faire tourner un automaton pour vendre des sites | 📦 **Réserve, ne pas installer** : (1) il faut l'alimenter en argent (portefeuille crypto + calcul payant Conway) alors que le budget est à 0 € ; (2) il agit seul dans le monde réel (domaines, emails, paiements) sans validation humaine, ce qui est contraire à notre cadre de démarchage (expéditeur identifiable, envois ciblés, brouillons validés par l'utilisateur pour tout prix ou rendez-vous) et engage l'identité de l'utilisateur ; (3) installation par script distant (`curl … | sh`) et code auto-modifiable : interdit par nos règles (jamais de binaire ou de script chargé à distance sans relecture complète) |
| Idées à retenir | ✅ Déjà en place chez nous sous une forme sûre : boucle « penser, agir, observer » = points automatiques 2 fois par jour ; journal de chaque action (`ETAT.md`, commits) ; « niveaux de survie » = budget 0 € et coût IA nul ; garde-fous écrits (`.claude/CLAUDE.md`, section sécurité) |
| Quand le ressortir | Seulement si : un client paie, l'agent peut être bridé (plafond de dépense, aucun envoi sans validation humaine, pas de reproduction), et le code a été relu en entier |

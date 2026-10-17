# SKILLS: La révolution que tu attendais dans l'Agent Coding

Vidéo : https://youtu.be/PW1UuREIkkg · durée 10:44 · résumé Gemini (gemini-3.5-flash-lite, lot de 8) du 2026-10-08
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Présentation des *skills* (compétences réutilisables pour agents IA) et de la commande `npx skill add <owner/repo>` pour installer des guides de bonnes pratiques, notamment sur Vercel React/Next.js, afin d'aider des outils comme Claude Code à coder plus efficacement et sans lire l'intégralité d'un projet.

2) **Outils, sites ou dépôts GitHub cités** :
- **Skills (dépôt GitHub `vercel-labs/agent-skills`)** : Gratuit (Open Agent Skills Ecosystem). Permet d'installer des compétences pour agents IA sous forme de fichiers de bonnes pratiques.
- **Claude Code** : Éditeur/outil de code (payant selon l'abonnement Claude).
- **Subfast** : Mentionné comme exemple d'application / outil (non précisé).
- **Remotion (`remotion-best-practices`)** : Skill pour créer des vidéos Remotion (gratuit).
- **SaveIt.now** : Application présentée comme exemple de projet réalisé avec l'aide d'un skill (non précisé).
- **Convex (`convex-best-practices`)** : Skill pour Convex (gratuit).
- **Convex Seven Skills** : Autre outil/plateforme pour trouver des skills (non précisé).
- **MLV.sh/FC** : Lien personnel de l'auteur pour retrouver sa configuration et ses liens (gratuit/payant selon accès, non précisé).

3) **Astuces concrètes et réutilisables** :
- Installer un skill dans son projet ou en global (ou en symlink) avec `npx skill add <owner/repo>`.
- Utiliser la mention du skill dans un agent IA (ex: `@vercel-react-best-practices`) pour lui faire respecter les bonnes pratiques sans charger tous les fichiers du projet.
- Créer ses propres skills ou workflows automatisés dans Claude Code / Apex (avec l'option de revue par agent) pour forcer l'IA à vérifier le code par rapport aux règles définies.
- Utiliser l'option *Context Fork* pour exécuter un skill en isolation dans un sous-agent sans lui donner accès à toute l'historique de conversation.

4) **Chiffres de revenus annoncés** :
- *Affirmé par l'auteur* : 105 € de revenus par mois via les abonnements de sa chaîne (membres Club/Pro).

---

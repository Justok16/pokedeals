# « Les 5 skills qui rendent Claude autonome — install et liens » (guide Loucash, envoyé le 02/10/2026)

Source : page Obsidian Publish « guides.0xloucash.xyz » (guide DM daté du 15/07/2026 dans ses métadonnées), lue le 02/10/2026 ; chaque dépôt vérifié ensuite sur GitHub le même jour (README, et pour Task Observer : SKILL.md, USER-GUIDE.md et la liste complète des fichiers). La page renvoie vers une consultation payante (visio 1 h) et vers « gratos.app » (alternatives gratuites).

Idée de la page : cinq skills forment une chaîne — Claude **trouve** ses outils (Skills CLI), **planifie** (Superpowers), **se souvient** (Claude Mem), a du **goût** (Impeccable), **s'améliore** en fond (Task Observer). Tous open source et gratuits selon la page (vérifié : licences MIT, CC BY 4.0, Apache 2.0 ; Claude Mem a une option cloud payante après 14 jours d'essai).

| # | Skill (dépôt vérifié) | Ce que ça fait | Vérifié le 02/10 | Verdict Dig |
|---|---|---|---|---|
| 1 | Skills CLI `vercel-labs/skills` (`npx skills find / add`) | Cherche et installe des skills depuis GitHub pour 70+ agents | MIT ; programme npm (code non relisible en entier avant exécution) | **Pas installé** : mêmes fonctions déjà couvertes (outil SearchSkills du poste, `outils/chercher_skills.py`, lecture manuelle des SKILL.md avant toute installation, règle du 28/09) |
| 2 | Superpowers `obra/superpowers` | Méthode de travail : plan, conception, tests, relecture | Marketplace officielle | **Déjà installé** (24/09, voir `33-outils.md`) |
| 3 | Claude Mem `thedotmack/claude-mem` | Mémoire entre sessions (5 hooks, service Bun, SQLite + Chroma) | Apache 2.0 ; `npx claude-mem install` demande une connexion « CMEM Pro » (essai 14 jours), fournisseur local possible | **Pas installé** (déjà tranché le 02/10 avec la page Notion « 5 repos ») : service permanent impossible dans un conteneur qui redémarre ; notre mémoire est dans le dépôt (CLAUDE.md, `46`, texte de la routine) |
| 4 | Impeccable `pbakaus/impeccable` | Goût design : `/impeccable shape / polish / audit / critique` | — | **Déjà installé** en texte seul (01/10, `.claude/skills/impeccable`) |
| 5 | Task Observer `rebelytics/one-skill-to-rule-them-all` | Méta-skill : observe les sessions, journalise les corrections et propose des améliorations de skills | CC BY 4.0 ; bundle texte (SKILL.md 47 Ko + 7 références ≈ 370 Ko + 2 scripts) ; conçu pour Cowork, « confirmé par des utilisateurs » sur Claude Code | **Évalué, non installé pour l'instant** (voir ci-dessous) |

## Pourquoi Task Observer n'est pas installé aujourd'hui

- Le skill demande d'être chargé **avant le premier appel d'outil de chaque session** (≈ 730 lignes de cœur, puis des références de 11 à 100 Ko selon l'épisode), un point de contrôle écrit toutes les 3 tâches et un journal d'observations par fichier : un surcoût de quota à chaque passage automatique (toutes les 3 h), alors que la consigne est d'**économiser le quota hebdomadaire**.
- Son propre README prévient : « si vous avez une petite installation avec une poignée de skills, la mémoire intégrée de votre système couvre l'essentiel avec moins de surcharge, et éditer un skill directement est rapide ». C'est notre cas : les corrections sont appliquées directement dans `46-apprentissage-continu.md`, `44-controle-qualite.md`, les outils et le texte de la routine, à chaque passage.
- Le journal d'observations devrait vivre dans un dossier stable ; ici, seul le dépôt (public) est durable, ce qui imposerait de filtrer chaque observation (aucune donnée de prospect ni d'utilisateur).
- **À reconsidérer** si la bibliothèque de skills du projet grossit (plus d'une vingtaine) ou si l'utilisateur travaille un jour dans Claude Cowork avec un dossier partagé, l'environnement pour lequel il est conçu. Les fichiers lus sont conservés hors dépôt (scratchpad) pour une installation rapide le cas échéant.

Conseils de la page repris : installer les skills dans un ordre (chercheur → méthode → mémoire → goût → amélioration continue) ; Superpowers ralentit volontairement le démarrage ; un skill ne modifie pas le modèle, il guide le comportement.
